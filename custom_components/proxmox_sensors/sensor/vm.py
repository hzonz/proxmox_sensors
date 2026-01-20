from .base import ProxmoxBaseSensor
from ..const import DOMAIN

class ProxmoxVMSensor(ProxmoxBaseSensor):
    """Sensor principal de estado para Máquinas Virtuales (VM)."""
    def __init__(self, coordinator, vm_id, node, label):
        # Nombre limpio: "Status" (HA lo mostrará como "VM: Nombre Status")
        name = "Status"
        uid = f"proxmox_vm_{node}_{vm_id}_status_v3"
        self._label = label
        super().__init__(coordinator, vm_id, name, None, uid, node)
        self._attr_icon = "mdi:monitor"

    @property
    def device_info(self):
        """Define el dispositivo de la VM vinculado al Nodo."""
        node_id = self._node.lower()
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._sensor_id}")},
            "name": f"4. VM: {self._label}",
            "via_device": (DOMAIN, f"proxmox_node_{node_id}"),
            "manufacturer": "Proxmox",
            "model": "QEMU Virtual Machine",
        }

    def _get_value(self):
        vm_data = self.coordinator.data.get("vms", {}).get(self._sensor_id, {})
        return str(vm_data.get("status", "unknown")).capitalize()

class ProxmoxVMAttributeSensor(ProxmoxBaseSensor):
    """Sensores de atributos para VMs (CPU, Memoria, Disco, Uptime)."""
    def __init__(self, coordinator, vm_id, node, label, attr_name, unit, icon):
        display_name = attr_name.replace("_", " ").title()
        uid = f"proxmox_vm_{node}_{vm_id}_{attr_name.lower()}_v3"
        
        self._label = label
        self._attr_key = attr_name
        
        super().__init__(coordinator, vm_id, display_name, unit, uid, node)
        self._attr_icon = icon

    @property
    def device_info(self):
        """Mismo identificador que la clase principal para agrupar sensores."""
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._sensor_id}")},
            "name": f"VM: {self._label}",
        }

    def _get_value(self):
        vm_data = self.coordinator.data.get("vms", {}).get(self._sensor_id, {})
        if not vm_data: return None
        
        try:
            if self._attr_key == "cpu_usage":
                val = vm_data.get("cpu")
                return round(float(val) * 100, 2) if val is not None else None

            keys = {
                "memory_used": "mem",
                "memory_total": "maxmem",
                "disk_used": "disk",
                "disk_total": "maxdisk",
                "uptime": "uptime"
            }
            
            api_key = keys.get(self._attr_key)
            val = vm_data.get(api_key)
            
            if val is None: return None
            
            if self._attr_key == "uptime":
                return round(float(val) / 3600, 1)
            
            # Conversión de Bytes a GB
            return round(float(val) / (1024**3), 2)
            
        except (ValueError, TypeError):
            return None