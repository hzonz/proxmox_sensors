"""Virtual Machine sensors for Proxmox."""
from .base import ProxmoxBaseSensor
from ..const import DOMAIN

class ProxmoxVMSensor(ProxmoxBaseSensor):
    """Main status sensor for Virtual Machines (VM)."""
    
    def __init__(self, coordinator, vm_id, node, label):
        """Initialize the VM status sensor."""
        # Clean name: "Status" (HA will display it as "VM: Name Status")
        name = "Status"
        uid = f"proxmox_vm_{node}_{vm_id}_status_v3"
        self._label = label
        super().__init__(coordinator, vm_id, name, None, uid, node)
        self._attr_icon = "mdi:monitor"

    @property
    def device_info(self):
        """Define the VM device linked to the Node."""
        node_id = self._node.lower()
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._sensor_id}")},
            "name": f"4. VM: {self._label}",
            "via_device": (DOMAIN, f"proxmox_node_{node_id}"),
            "manufacturer": "Proxmox",
            "model": "QEMU Virtual Machine",
        }

    def _get_value(self):
        """Return the current status of the VM."""
        vm_data = self.coordinator.data.get("vms", {}).get(self._sensor_id, {})
        return str(vm_data.get("status", "unknown")).capitalize()

class ProxmoxVMAttributeSensor(ProxmoxBaseSensor):
    """Attribute sensors for VMs (CPU, Memory, Disk, Uptime)."""
    
    def __init__(self, coordinator, vm_id, node, label, attr_name, unit, icon):
        """Initialize the VM attribute sensor."""
        display_name = attr_name.replace("_", " ").title()
        uid = f"proxmox_vm_{node}_{vm_id}_{attr_name.lower()}_v3"
        
        self._label = label
        self._attr_key = attr_name
        
        super().__init__(coordinator, vm_id, display_name, unit, uid, node)
        self._attr_icon = icon

    @property
    def device_info(self):
        """Link these sensors to the same VM device as the main status sensor."""
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._sensor_id}")},
            "name": f"4. VM: {self._label}",
        }

    def _get_value(self):
        """Calculate the value based on the attribute key."""
        vm_data = self.coordinator.data.get("vms", {}).get(self._sensor_id, {})
        if not vm_data:
            return None
        
        try:
            # CPU Usage calculation (0.0 - 1.0 to percentage)
            if self._attr_key == "cpu_usage":
                val = vm_data.get("cpu")
                return round(float(val) * 100, 2) if val is not None else None

            # Mapping for Proxmox API keys
            keys = {
                "memory_used": "mem",
                "memory_total": "maxmem",
                "disk_used": "disk",
                "disk_total": "maxdisk",
                "uptime": "uptime"
            }
            
            api_key = keys.get(self._attr_key)
            val = vm_data.get(api_key)
            
            if val is None:
                return None
            
            # Uptime conversion from seconds to hours
            if self._attr_key == "uptime":
                return round(float(val) / 3600, 1)
            
            # Conversion from Bytes to GB
            return round(float(val) / (1024**3), 2)
            
        except (ValueError, TypeError):
            return None