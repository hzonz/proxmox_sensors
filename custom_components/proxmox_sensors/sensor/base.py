"""Base classes for Proxmox and PBS sensors."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..const import DOMAIN

# ============================================================
#  BASE SENSOR FOR PVE (Proxmox Virtual Environment)
# ============================================================
class ProxmoxBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for all Proxmox sensors with safe data handling."""
    
    _attr_has_entity_name = True
    
    def __init__(self, coordinator, sensor_id, name, unit, unique_id, node=None):
        """Initialize the PVE base sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        
        # Normalize node name to lowercase for consistent internal tracking
        self._node = node.lower() if node else "proxmox_server"
        
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        
        # Unique ID must always be lowercase and consistent to avoid duplicate entities
        self._attr_unique_id = unique_id.lower().replace(" ", "_")

    @property
    def native_value(self):
        """Return the state of the sensor using the specific child logic."""
        try:
            return self._get_value()
        except Exception:
            return None

    def _get_value(self):
        """Method to be overridden by child classes."""
        raise NotImplementedError

    @property
    def device_info(self):
        """Node device information (The parent in the PVE hierarchy)."""
        node_id = self._node.lower()
        display_node = self._node.capitalize()
        
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{node_id}")},
            "name": f"1. Node: {display_node}",
            "manufacturer": "Proxmox",
            "model": "Physical Node",
        }


# ============================================================
#  BASE SENSOR FOR PBS (Proxmox Backup Server)
# ============================================================
class ProxmoxPbsBaseSensor(CoordinatorEntity, SensorEntity):
    """
    Base class for all PBS sensors.
    PBS follows a different hierarchy than PVE as it doesn't use 'nodes' 
    in the same API structure. Each server instance uses a server_id.
    """

    _attr_has_entity_name = True

    def __init__(self, coordinator, server_id: str, sensor_id: str, name: str, unit=None):
        """Initialize the PBS base sensor."""
        super().__init__(coordinator)

        self._server_id = server_id          # e.g., pbs_1, pbs_2...
        self._sensor_id = sensor_id          # e.g., version, last_task, datastore_used...
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit

        # Exclusive Unique ID per PBS instance
        self._attr_unique_id = f"pbs_{self._server_id}_{self._sensor_id}".lower()

    @property
    def device_info(self):
        """Group entities under the specific PBS server device."""
        return {
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id.upper()}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }

    @property
    def native_value(self):
        """Return the state of the sensor using the specific child logic."""
        try:
            return self._get_value()
        except Exception:
            return None

    def _get_value(self):
        """Method to be overridden by child classes."""
        raise NotImplementedError