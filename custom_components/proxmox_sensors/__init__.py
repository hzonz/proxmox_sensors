from __future__ import annotations
import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
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
    CONF_VERIFY_SSL,
)

from .api import ProxmoxClient
from .coordinator import create_proxmox_coordinator

# Logger global
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
        verify_ssl=data.get(CONF_VERIFY_SSL, False),
    )

    coordinator = await create_proxmox_coordinator(hass, entry, client)

    try:
        async with asyncio.timeout(20):
            await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady(
            f"Unable to connect to Proxmox {data[CONF_HOST]}"
        ) from err

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "node": data[CONF_NODE],
        "server_type": client._server_type,  
        "features": data.get("features", {}),
    }

    # ==========================================================
    # RECORD OF BACKUP ACTION (vzdump)
    # ==========================================================
    async def handle_vzdump_backup(call: ServiceCall):
        """Handler for the backup action (vzdump) with fixed label."""
        node = call.data.get("node")
        vmid = call.data.get("vmid")
        storage = call.data.get("storage")
        
        logger = logging.getLogger("custom_components.proxmox_sensors")

        notes = f"{vmid} | HA Backup"
        
        try:
            logger.info("Sending manual backup command from HA for VM/CT %s", vmid)
            result = await client.start_vzdump(hass, node, vmid, storage, notes=notes)
            if result:
                logger.info("Backup started successfully: %s", result)
            else:
                logger.warning("Proxmox did not return a response for the backup of %s", vmid)
                
        except Exception as e:
            logger.error("Error running backup from HA: %s", str(e))

    
    hass.services.async_register(
        DOMAIN, "create_vzdump_backup", handle_vzdump_backup
    )
    # ==========================================================

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unload_ok