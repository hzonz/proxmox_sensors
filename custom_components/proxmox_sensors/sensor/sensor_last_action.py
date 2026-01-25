from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN

class PBSLastActionSensor(SensorEntity):
    """Local sensor that stores the last PBS maintenance action."""

    def __init__(self, coordinator, datastore):
        self._datastore = datastore
        self._attr_name = "Last Action"
        self._attr_unique_id = f"{datastore.lower()}_last_action"
        self._state = "Waiting"

        self._attr_should_poll = False

        # Device grouping
        self._attr_device_info = {
            "identifiers": {("proxmox_sensors", f"maintenance_{datastore}")},
            "name": f"Maintenance: {datastore}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Backup Server",
        }

    @property
    def state(self):
        return self._state

    def set_action(self, message: str):
        """Update the sensor state."""
        self._state = message
        self.async_write_ha_state()
