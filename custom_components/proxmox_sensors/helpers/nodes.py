from .const import DOMAIN

def get_node_name(hass):
    entry_id = next(iter(hass.data[DOMAIN].keys()))
    return hass.data[DOMAIN][entry_id]["node"]
