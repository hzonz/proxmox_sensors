"""Storage sensors for Proxmox storage pools."""
from .base import ProxmoxBaseSensor
from ..const import DOMAIN

class ProxmoxStorageSensor(ProxmoxBaseSensor):

    def __init__(self, coordinator, storage_name, st, node=None):
        uid = f"proxmox_storage_{node}_{storage_name}_percent_v3"
        super().__init__(coordinator, storage_name, "Usage", "%", uid, node)
        
        self._storage_name = storage_name
        self._attr_icon = "mdi:database"
        self._attr_state_class = "measurement"

    @property
    def device_info(self):
        node_id = self._node.lower()
        return {
            "identifiers": {(DOMAIN, f"proxmox_storage_{node_id}_{self._storage_name}")},
            "name": f"5. Storage: {self._storage_name}",
            "via_device": (DOMAIN, f"proxmox_node_{node_id}"),
            "manufacturer": "Proxmox",
            "model": "Storage Resource",
        }

    def _get_value(self):
        storage_data = self.coordinator.data.get("storage", {}).get(self._storage_name, {})
        used = storage_data.get("used") or 0
        total = storage_data.get("total") or 0
        if total == 0:
            return 0
        return round((used / total) * 100, 2)

class ProxmoxStorageAttributeSensor(ProxmoxBaseSensor):

    def __init__(self, coordinator, storage_name, st, label, key, node=None):
        uid = f"proxmox_storage_{node}_{storage_name}_{key}_v3"
        unit = "GB" if key in ("used", "avail", "total") else None
        
        super().__init__(coordinator, storage_name, label, unit, uid, node)

        self._storage_name = storage_name
        self._key = key

        icon_map = {
            "used": "mdi:database-arrow-up",
            "avail": "mdi:database-arrow-down",
            "total": "mdi:database",
            "type": "mdi:format-list-bulleted-type",
            "path": "mdi:folder-network",
        }
        self._attr_icon = icon_map.get(key, "mdi:information-outline")

        if key in ("used", "avail", "total"):
            self._attr_device_class = "data_size"
            self._attr_state_class = "measurement"

    @property
    def device_info(self):
        node_id = self._node.lower()
        return {
            "identifiers": {(DOMAIN, f"proxmox_storage_{node_id}_{self._storage_name}")},
            "name": f"5. Storage: {self._storage_name}",
        }

    def _get_value(self):
        storage_data = self.coordinator.data.get("storage", {}).get(self._storage_name, {})
        
        if self._key == "path":
            return storage_data.get("content") or storage_data.get("storage") or "N/A"
            
        value = storage_data.get(self._key)
        
        if value is None or value == "":
            return "Unknown" if not self.unit_of_measurement else 0

        if self._key in ("used", "avail", "total"):
            try:
                return round(float(value) / (1024**3), 2)
            except (ValueError, TypeError):
                return 0

        return str(value).capitalize() if self._key == "type" else value