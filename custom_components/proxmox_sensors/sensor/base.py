from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..const import DOMAIN

# ============================================================
#  BASE SENSOR FOR PVE
# ============================================================
class ProxmoxBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for all Proxmox sensors with safe handling."""
    
    _attr_has_entity_name = True
    
    def __init__(self, coordinator, sensor_id, name, unit, unique_id, node=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        
        # Normalizamos el nombre del nodo para evitar fallos de ID
        self._node = node.lower() if node else "proxmox_server"
        
        # Atributos nativos de SensorEntity
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        
        # El unique_id debe ser siempre minúsculas y consistente
        self._attr_unique_id = unique_id.lower().replace(" ", "_")

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            return self._get_value()
        except Exception:
            return None

    def _get_value(self):
        """Method to be overridden by child classes."""
        raise NotImplementedError

    @property
    def device_info(self):
        """Información del dispositivo Nodo (padre de la jerarquía)."""
        node_id = self._node.lower()
        display_node = self._node.capitalize()
        
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{node_id}")},
            "name": f"1. Node: {display_node}",
            "manufacturer": "Proxmox",
            "model": "Physical Node",
        }


# ============================================================
#  BASE SENSOR FOR PBS
#  Purpose:
#     - PBS no tiene nodo → no puede usar ProxmoxBaseSensor
#     - Cada PBS usa server_id (pbs_1, pbs_2...)
#     - Unique_id y device_info exclusivos por servidor PBS
# ============================================================
class ProxmoxPbsBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for all PBS sensors."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, server_id: str, sensor_id: str, name: str, unit=None):
        super().__init__(coordinator)

        self._server_id = server_id          # pbs_1, pbs_2, pbs_3...
        self._sensor_id = sensor_id          # version, last_task, datastore_used...
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit

        # Unique ID exclusivo por PBS
        self._attr_unique_id = f"pbs_{self._server_id}_{self._sensor_id}".lower()

    @property
    def device_info(self):
        """Agrupación por servidor PBS."""
        return {
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id.upper()}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            return self._get_value()
        except Exception:
            return None

    def _get_value(self):
        """Method to be overridden by child classes."""
        raise NotImplementedError
