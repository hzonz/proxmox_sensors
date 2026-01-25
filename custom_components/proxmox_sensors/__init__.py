from __future__ import annotations
import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import Platform

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_USER,
    CONF_PASSWORD,
    CONF_TOKEN_ID,
    CONF_TOKEN_SECRET,
    CONF_NODE,
    CONF_PLATFORM_TYPE,
)

from .api import ProxmoxClient
from .coordinator import create_proxmox_coordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = entry.data

    client = ProxmoxClient(
        host=data[CONF_HOST],
        user=data[CONF_USER],
        password=data.get(CONF_PASSWORD),
        token_id=data.get(CONF_TOKEN_ID),
        token_secret=data.get(CONF_TOKEN_SECRET),
        server_type=data[CONF_PLATFORM_TYPE],
        verify_ssl=False,
    )

    coordinator = await create_proxmox_coordinator(hass, entry, client)

    try:
        async with asyncio.timeout(20):
            await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(
            f"No se pudo conectar con Proxmox en {data[CONF_HOST]}"
        ) from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "node": data[CONF_NODE],
        "server_type": client._server_type,  
        "features": data.get("features", {}),
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok

