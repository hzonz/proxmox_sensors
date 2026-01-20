from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
import logging

_LOGGER = logging.getLogger(__name__)

async def get_entities_for_node(hass, node_name: str):
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)

    device = next(
        (
            d for d in device_registry.devices.values()
            if any(
                node_name.lower() in str(part).lower()
                for ident in d.identifiers
                for part in ident
            )
        ),
        None
    )

    if not device:
        _LOGGER.error("No se encontró un dispositivo asociado al nodo: %s", node_name)
        return []

    return [
        entity
        for entity in entity_registry.entities.values()
        if entity.device_id == device.id
    ]
