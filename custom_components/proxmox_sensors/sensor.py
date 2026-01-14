from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up all Proxmox sensors."""

    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    features = data["features"]

    entities = []

    # ---------------------------------------------------------
    # HARDWARE SENSORS
    # ---------------------------------------------------------
    if features.get("enable_hardware"):
        for sensor_id in data["hardware_sensors"]:
            entities.append(
                ProxmoxHardwareSensor(
                    coordinator,
                    sensor_id,
                    data["node"],
                )
            )

    # ---------------------------------------------------------
    # NODE SENSORS
    # ---------------------------------------------------------
    if features.get("enable_node"):
        for sensor_id in data["node_sensors"]:
            info = data["node_sensors"][sensor_id]
            entities.append(
                ProxmoxNodeSensor(
                    coordinator,
                    sensor_id,
                    info["name"],
                    info["unit"],
                    data["node"],
                )
            )

    # ---------------------------------------------------------
    # DISKS
    # ---------------------------------------------------------
    if features.get("enable_disks"):
        for disk_id in data["disks"]:
            entities.append(
                ProxmoxDiskSensor(
                    coordinator,
                    disk_id,
                    data["node"],
                )
            )

    # ---------------------------------------------------------
    # VMs
    # ---------------------------------------------------------
    if features.get("enable_vms"):
        vm_mode = data["vm_mode"]
        vms_selected = data["vms"]

        if vm_mode == "auto":
            # All VMs will be created dynamically in sensor
            pass
        else:
            for vm_id in vms_selected:
                entities.append(
                    ProxmoxVMSensor(
                        coordinator,
                        vm_id,
                        data["node"],
                    )
                )

    # ---------------------------------------------------------
    # CONTAINERS
    # ---------------------------------------------------------
    if features.get("enable_cts"):
        ct_mode = data["ct_mode"]
        cts_selected = data["cts"]

        if ct_mode == "auto":
            pass
        else:
            for ct_id in cts_selected:
                entities.append(
                    ProxmoxContainerSensor(
                        coordinator,
                        ct_id,
                        data["node"],
                    )
                )

    # ---------------------------------------------------------
    # PBS DATASTORES
    # ---------------------------------------------------------
    if data["server_type"] == "PBS" and features.get("enable_pbs_datastores"):
        for store in data["datastores"]:
            entities.append(
                ProxmoxPBSDatastoreSensor(
                    coordinator,
                    store,
                )
            )

    # ---------------------------------------------------------
    # PBS TASKS
    # ---------------------------------------------------------
    if data["server_type"] == "PBS" and features.get("enable_pbs_tasks"):
        entities.append(
            ProxmoxPBSTaskSensor(
                coordinator,
            )
        )

    async_add_entities(entities)


# ============================================================
# BASE CLASS
# ============================================================

class ProxmoxBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for all Proxmox sensors."""

    def __init__(self, coordinator, sensor_id, name, unit, unique_id):
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = unique_id

    @property
    def native_value(self):
        """Return the sensor value."""
        return self._get_value()

    def _get_value(self):
        raise NotImplementedError


# ============================================================
# HARDWARE SENSOR
# ============================================================

class ProxmoxHardwareSensor(ProxmoxBaseSensor):
    """Hardware sensor (temperatures, fans, voltages)."""

    def __init__(self, coordinator, sensor_id, node):
        name = f"{sensor_id} ({node})"
        unit = None  # unit comes from coordinator data
        unique_id = f"proxmox_hw_{node}_{sensor_id}"
        super().__init__(coordinator, sensor_id, name, unit, unique_id)

    def _get_value(self):
        return self.coordinator.data.get("hardware", {}).get(self._sensor_id)

    @property
    def icon(self):
        sid = self._sensor_id.lower()
        if "temp" in sid:
            return "mdi:thermometer"
        if "fan" in sid:
            return "mdi:fan"
        if "volt" in sid or "v" in sid:
            return "mdi:flash"
        return "mdi:chip"


# ============================================================
# NODE SENSOR
# ============================================================

class ProxmoxNodeSensor(ProxmoxBaseSensor):
    """Node-level sensor (CPU, RAM, uptime)."""

    def __init__(self, coordinator, sensor_id, name, unit, node):
        unique_id = f"proxmox_node_{node}_{sensor_id}"
        super().__init__(coordinator, sensor_id, name, unit, unique_id)

    def _get_value(self):
        return self.coordinator.data.get("node", {}).get(self._sensor_id)

    @property
    def icon(self):
        if "cpu" in self._sensor_id:
            return "mdi:cpu-64-bit"
        if "ram" in self._sensor_id:
            return "mdi:memory"
        if "uptime" in self._sensor_id:
            return "mdi:timer-outline"
        return "mdi:server"


# ============================================================
# DISK SENSOR
# ============================================================

class ProxmoxDiskSensor(ProxmoxBaseSensor):
    """Disk sensor (usage, wear-level)."""

    def __init__(self, coordinator, disk_id, node):
        name = f"Disk {disk_id}"
        unit = "%"
        unique_id = f"proxmox_disk_{node}_{disk_id}"
        super().__init__(coordinator, disk_id, name, unit, unique_id)

    def _get_value(self):
        disk = self.coordinator.data.get("disks", {}).get(self._sensor_id)
        if disk:
            return disk.get("usage_pct")
        return None

    @property
    def icon(self):
        return "mdi:harddisk"


# ============================================================
# VM SENSOR
# ============================================================

class ProxmoxVMSensor(ProxmoxBaseSensor):
    """VM sensor (CPU %, RAM %, status)."""

    def __init__(self, coordinator, vm_id, node):
        name = f"VM {vm_id}"
        unit = "%"
        unique_id = f"proxmox_vm_{node}_{vm_id}"
        super().__init__(coordinator, vm_id, name, unit, unique_id)

    def _get_value(self):
        vm = self.coordinator.data.get("vms", {}).get(self._sensor_id)
        if vm:
            return vm.get("cpu_pct")
        return None

    @property
    def icon(self):
        return "mdi:monitor"


# ============================================================
# CONTAINER SENSOR
# ============================================================

class ProxmoxContainerSensor(ProxmoxBaseSensor):
    """Container sensor (CPU %, RAM %, status)."""

    def __init__(self, coordinator, ct_id, node):
        name = f"CT {ct_id}"
        unit = "%"
        unique_id = f"proxmox_ct_{node}_{ct_id}"
        super().__init__(coordinator, ct_id, name, unit, unique_id)

    def _get_value(self):
        ct = self.coordinator.data.get("cts", {}).get(self._sensor_id)
        if ct:
            return ct.get("cpu_pct")
        return None

    @property
    def icon(self):
        return "mdi:docker"


# ============================================================
# PBS DATASTORE SENSOR
# ============================================================

class ProxmoxPBSDatastoreSensor(ProxmoxBaseSensor):
    """PBS datastore usage sensor."""

    def __init__(self, coordinator, store):
        name = f"PBS Datastore {store}"
        unit = "%"
        unique_id = f"proxmox_pbs_store_{store}"
        super().__init__(coordinator, store, name, unit, unique_id)

    def _get_value(self):
        store = self.coordinator.data.get("pbs_datastores", {}).get(self._sensor_id)
        if store:
            return store.get("usage_pct")
        return None

    @property
    def icon(self):
        return "mdi:database"


# ============================================================
# PBS TASK SENSOR
# ============================================================

class ProxmoxPBSTaskSensor(ProxmoxBaseSensor):
    """PBS last task status."""

    def __init__(self, coordinator):
        name = "PBS Last Backup Task"
        unit = None
        unique_id = "proxmox_pbs_last_task"
        super().__init__(coordinator, "last_task", name, unit, unique_id)

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        if task:
            return task.get("status")
        return None

    @property
    def icon(self):
        return "mdi:clipboard-check"
