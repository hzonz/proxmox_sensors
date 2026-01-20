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
from .helpers.frontend import async_download_panel_if_needed, async_register_panel

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura la integración Proxmox Sensors Extended."""
    data = entry.data

    # 1. Preparar el cliente API
    client = ProxmoxClient(
        host=data[CONF_HOST],
        user=data[CONF_USER],
        password=data.get(CONF_PASSWORD),
        token_id=data.get(CONF_TOKEN_ID),
        token_secret=data.get(CONF_TOKEN_SECRET),
        server_type=data[CONF_PLATFORM_TYPE],
        verify_ssl=False,
    )

    # 2. Crear el coordinador
    coordinator = await create_proxmox_coordinator(hass, entry, client)

    try:
        # 3. Intento de carga inicial
        async with asyncio.timeout(20):
            await coordinator.async_config_entry_first_refresh()

    except Exception as err:
        _LOGGER.warning(
            "Proxmox (%s) no responde: %s. Reintentando...",
            data[CONF_HOST],
            err
        )
        raise ConfigEntryNotReady(
            f"No se pudo conectar con Proxmox en {data[CONF_HOST]}"
        ) from err

    # 4. Guardar datos de la instancia
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "node": data[CONF_NODE],
        "server_type": data[CONF_PLATFORM_TYPE],
        "features": data.get("features", {}),
    }

    # 4.5 Registrar o actualizar el panel personalizado Proxmox
    version = await async_download_panel_if_needed(hass)
    await async_register_panel(hass, version)

    # 5. Crear entidades
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarga limpia de la integración."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok
