from .base import ProxmoxBaseSensor
from ..const import DOMAIN

class ProxmoxContainerSensor(ProxmoxBaseSensor):
    """Main status sensor for LXC."""
    def __init__(self, coordinator, ct_id, node, label):
        name = "Status"
        # Mantenemos v4 para forzar limpieza total
        uid = f"proxmox_ct_{node}_{ct_id}_status_v4"
        self._label = label
        super().__init__(coordinator, ct_id, name, None, uid, node)
        self._attr_icon = "mdi:label-outline"

    @property
    def device_info(self):
        # Normalizamos el node_id a minúsculas para el match del identificador
        node_id = self._node.lower()
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._sensor_id}_v4")},
            "name": f"3. CT: {self._label}",
            "via_device": (DOMAIN, f"proxmox_node_{node_id}"),
            "manufacturer": "Proxmox",
            "model": "LXC Container",
        }

    def _get_value(self):
        ct_data = self.coordinator.data.get("cts", {}).get(self._sensor_id, {})
        return str(ct_data.get("status", "unknown")).capitalize()

class ProxmoxContainerAttributeSensor(ProxmoxBaseSensor):
    """Attribute sensors for LXC (CPU, RAM, Disk, Uptime)."""
    def __init__(self, coordinator, ct_id, node, label, attr_name, unit, icon):
        display_name = attr_name.replace("_", " ").title()
        uid = f"proxmox_ct_{node}_{ct_id}_{attr_name}_v4"
        
        self._label = label
        self._attr_key = attr_name
        
        super().__init__(coordinator, ct_id, display_name, unit, uid, node)
        self._attr_icon = icon

    @property
    def device_info(self):
        # Identificador exacto para agrupar bajo el mismo dispositivo
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._sensor_id}_v4")},
            "name": f"3. CT: {self._label}",
        }

    def _get_value(self):
        ct_data = self.coordinator.data.get("cts", {}).get(self._sensor_id, {})
        if not ct_data: return None
        
        try:
            if self._attr_key == "cpu_usage":
                val = ct_data.get("cpu")
                return round(float(val) * 100, 2) if val is not None else None

            keys = {
                "memory_used": "mem",
                "memory_total": "maxmem",
                "disk_used": "disk",
                "disk_total": "maxdisk",
                "uptime": "uptime"
            }
            
            val = ct_data.get(keys.get(self._attr_key))
            if val is None: return None
            
            if self._attr_key == "uptime":
                return round(float(val) / 3600, 1)
            
            return round(float(val) / (1024**3), 2)
            
        except (ValueError, TypeError):
            return None