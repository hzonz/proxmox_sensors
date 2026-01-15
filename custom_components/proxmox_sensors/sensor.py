from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    features = data["features"]
    node = data["node"]
    server_type = data["server_type"]

    entities = []

    # HARDWARE
    if features.get("enable_hardware", True):
        for sensor_id in coordinator.data.get("hardware", {}):
            entities.append(ProxmoxHardwareSensor(coordinator, sensor_id, node))

    # NODE
    if features.get("enable_node", True):
        node_data = coordinator.data.get("node", {})

        if "cpuinfo" in node_data:
            entities.append(ProxmoxCPUInfoSensor(coordinator, node))
        if "ksm" in node_data:
            entities.append(ProxmoxKSMSensor(coordinator, node))
        if "memory" in node_data:
            entities.append(ProxmoxMemorySensor(coordinator, node))
        if "swap" in node_data:
            entities.append(ProxmoxSwapSensor(coordinator, node))
        if "rootfs" in node_data:
            entities.append(ProxmoxRootFSSensor(coordinator, node))

        for key in node_data:
            if key in ("cpuinfo", "ksm", "memory", "swap", "rootfs"):
                continue
            entities.append(ProxmoxNodeSensor(coordinator, key, node))

    # DISKS (CORREGIDO + SENSORES POR ATRIBUTO)
    if features.get("enable_disks", True):
        for disk_id, disk in coordinator.data.get("disks", {}).items():
            label = disk.get("model") or disk_id

            # Sensor principal del disco
            entities.append(ProxmoxDiskSensor(coordinator, disk_id, node, label))

            # Sensores individuales por atributo
            attribute_map = {
                "temperature": ("Temperatura", "°C"),
                "wearout": ("Wearout", "%"),
                "health": ("Health", None),
                "rpm": ("RPM", "RPM"),
                "model": ("Modelo", None),
                "devpath": ("Path", None),
            }

            for attr_key, (attr_label, unit) in attribute_map.items():
                value = disk.get(attr_key)
                if value not in (None, "N/A", ""):
                    entities.append(
                        ProxmoxDiskAttributeSensor(
                            coordinator,
                            disk_id,
                            node,
                            label,
                            attr_key,
                            attr_label,
                            unit,
                        )
                    )

    # VMs
    if features.get("enable_vms", True):
        for vmid, vm in coordinator.data.get("vms", {}).items():
            label = vm.get("name", f"VM {vmid}")
            entities.append(ProxmoxVMSensor(coordinator, vmid, node, label))

    # CTs
    if features.get("enable_cts", True):
        for ctid, ct in coordinator.data.get("cts", {}).items():
            label = ct.get("name", f"CT {ctid}")
            entities.append(ProxmoxContainerSensor(coordinator, ctid, node, label))

    # PBS DATASTORES
    if server_type == "PBS" and features.get("enable_pbs_datastores", True):
        for store in coordinator.data.get("pbs_datastores", {}):
            entities.append(ProxmoxPBSDatastoreSensor(coordinator, store))

    # PBS TASKS
    if server_type == "PBS" and features.get("enable_pbs_tasks", True):
        entities.append(ProxmoxPBSTaskSensor(coordinator))

    async_add_entities(entities)


# BASE CLASS

class ProxmoxBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, sensor_id, name, unit, unique_id):
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = unique_id

    @property
    def native_value(self):
        return self._get_value()

    def _get_value(self):
        raise NotImplementedError


# HARDWARE

class ProxmoxHardwareSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, sensor_id, node):
        name = f"{sensor_id} ({node})"
        unique_id = f"proxmox_hw_{node}_{sensor_id}"
        super().__init__(coordinator, sensor_id, name, None, unique_id)

    def _get_value(self):
        return self.coordinator.data.get("hardware", {}).get(self._sensor_id)


# NODE SIMPLE

class ProxmoxNodeSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, sensor_id, node):
        name = f"Node {sensor_id} ({node})"
        unique_id = f"proxmox_node_{node}_{sensor_id}"
        super().__init__(coordinator, sensor_id, name, None, unique_id)

    def _get_value(self):
        return self.coordinator.data.get("node", {}).get(self._sensor_id)


# NODE EXTENDIDOS

class ProxmoxCPUInfoSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        name = f"Node cpuinfo ({node})"
        unique_id = f"proxmox_node_cpuinfo_{node}"
        super().__init__(coordinator, "cpuinfo", name, None, unique_id)

    def _get_value(self):
        return None

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("node", {}).get("cpuinfo", {})


class ProxmoxKSMSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        name = f"Node ksm ({node})"
        unique_id = f"proxmox_node_ksm_{node}"
        super().__init__(coordinator, "ksm", name, "bytes", unique_id)

    def _get_value(self):
        ksm = self.coordinator.data.get("node", {}).get("ksm", {})
        return ksm.get("shared")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("node", {}).get("ksm", {})


class ProxmoxMemorySensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        name = f"Node memory ({node})"
        unique_id = f"proxmox_node_memory_{node}"
        super().__init__(coordinator, "memory", name, "bytes", unique_id)

    def _get_value(self):
        mem = self.coordinator.data.get("node", {}).get("memory", {})
        return mem.get("used")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("node", {}).get("memory", {})


class ProxmoxSwapSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        name = f"Node swap ({node})"
        unique_id = f"proxmox_node_swap_{node}"
        super().__init__(coordinator, "swap", name, "bytes", unique_id)

    def _get_value(self):
        swap = self.coordinator.data.get("node", {}).get("swap", {})
        return swap.get("used")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("node", {}).get("swap", {})


class ProxmoxRootFSSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        name = f"Node rootfs ({node})"
        unique_id = f"proxmox_node_rootfs_{node}"
        super().__init__(coordinator, "rootfs", name, "bytes", unique_id)

    def _get_value(self):
        rootfs = self.coordinator.data.get("node", {}).get("rootfs", {})
        return rootfs.get("used")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("node", {}).get("rootfs", {})


# DISKS (CORREGIDO + SENSORES POR ATRIBUTO)

class ProxmoxDiskSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, disk_id, node, label):
        name = f"{label} (Disk)"
        unique_id = f"proxmox_disk_{node}_{disk_id}"
        super().__init__(coordinator, disk_id, name, "%", unique_id)

    def _get_value(self):
        disk = self.coordinator.data.get("disks", {}).get(self._sensor_id)
        if disk:
            total = disk.get("disk_total") or 0
            used = disk.get("disk_used") or 0
            if total == 0:
                return 0
            return round((used / total) * 100, 2)
        return 0

    @staticmethod
    def _format_gb(bytes_value):
        return round(bytes_value / (1024**3), 2) if bytes_value else 0

    @property
    def extra_state_attributes(self):
        disk = self.coordinator.data.get("disks", {}).get(self._sensor_id) or {}
        total = disk.get("disk_total") or 0
        used = disk.get("disk_used") or 0
        free = total - used if total else 0

        return {
            "Capacidad total (GB)": self._format_gb(total),
            "Espacio usado (GB)": self._format_gb(used),
            "Espacio libre (GB)": self._format_gb(free),
            "Modelo": disk.get("model"),
            "Serial": disk.get("serial"),
            "Tipo": disk.get("type"),
            "Tamaño (bytes)": disk.get("size"),
            "Temperatura (°C)": disk.get("temperature"),
            "Health": disk.get("health"),
            "Wearout (%)": disk.get("wearout"),
            "RPM": disk.get("rpm"),
            "Path": disk.get("devpath"),
        }


class ProxmoxDiskAttributeSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, disk_id, node, label, attr_key, attr_label, unit):
        name = f"{label} - {attr_label}"
        unique_id = f"proxmox_disk_attr_{node}_{disk_id}_{attr_key}"
        super().__init__(coordinator, disk_id, name, unit, unique_id)
        self._attr_key = attr_key

    def _get_value(self):
        disk = self.coordinator.data.get("disks", {}).get(self._sensor_id)
        if not disk:
            return None
        value = disk.get(self._attr_key)
        if value == "N/A":
            return None
        return value


# VMs

class ProxmoxVMSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, vm_id, node, label):
        name = f"{label} (VM {vm_id})"
        unique_id = f"proxmox_vm_{node}_{vm_id}"
        super().__init__(coordinator, vm_id, name, "%", unique_id)

    def _get_value(self):
        vm = self.coordinator.data.get("vms", {}).get(self._sensor_id)
        if vm:
            return round(vm.get("cpu", 0) * 100, 2)
        return None


# CTs

class ProxmoxContainerSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, ct_id, node, label):
        name = f"{label} (CT {ct_id})"
        unique_id = f"proxmox_ct_{node}_{ct_id}"
        super().__init__(coordinator, ct_id, name, "%", unique_id)

    def _get_value(self):
        ct = self.coordinator.data.get("cts", {}).get(self._sensor_id)
        if ct:
            return round(ct.get("cpu", 0) * 100, 2)
        return None


# PBS DATASTORE

class ProxmoxPBSDatastoreSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, store):
        name = f"PBS Datastore {store}"
        unique_id = f"proxmox_pbs_store_{store}"
        super().__init__(coordinator, store, name, "%", unique_id)

    def _get_value(self):
        store = self.coordinator.data.get("pbs_datastores", {}).get(self._sensor_id)
        if store:
            used = store.get("used")
            total = store.get("total")
            if used and total:
                return round((used / total) * 100, 2)
        return None


# PBS TASK

class ProxmoxPBSTaskSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "last_task", "PBS Last Task", None, "proxmox_pbs_last_task")

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        if task:
            return task.get("status")
        return None
