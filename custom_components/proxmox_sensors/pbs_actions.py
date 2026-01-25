import logging

_LOGGER = logging.getLogger(__name__)

BASE = "admin/datastore"

async def run_gc(client, hass, datastore: str):
    """Ejecuta Garbage Collection en el datastore indicado."""
    _LOGGER.info("PBS: Ejecutando GC en %s", datastore)
    return await client.post(hass, f"{BASE}/{datastore}/gc")

async def run_prune(client, hass, datastore: str):
    """Ejecuta Prune en el datastore indicado."""
    _LOGGER.info("PBS: Ejecutando Prune en %s", datastore)
    return await client.post(hass, f"{BASE}/{datastore}/prune")

async def run_verify(client, hass, datastore: str):
    """Ejecuta Verify en el datastore indicado."""
    _LOGGER.info("PBS: Ejecutando Verify en %s", datastore)
    return await client.post(hass, f"{BASE}/{datastore}/verify")

async def run_sync(client, hass, datastore: str):
    """Ejecuta Sync en el datastore indicado."""
    _LOGGER.info("PBS: Ejecutando Sync en %s", datastore)
    return await client.post(hass, f"{BASE}/{datastore}/sync")
