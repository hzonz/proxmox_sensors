import logging

_LOGGER = logging.getLogger(__name__)

BASE = "admin/datastore"


async def run_gc(client, hass, datastore: str):
    _LOGGER.info("PBS: Ejecutando GC en %s", datastore)
    endpoint = f"{BASE}/{datastore}/gc"
    return await client.pbs_post(hass, endpoint)


async def run_prune(client, hass, datastore: str):
    _LOGGER.info("PBS: Ejecutando PRUNE automático en %s", datastore)

    snapshots = await client.pbs_get(hass, f"{BASE}/{datastore}/snapshots")
    if not snapshots:
        _LOGGER.warning("PBS: No hay snapshots en %s", datastore)
        return None

    grupos = set()
    for snap in snapshots:
        btype = snap.get("backup-type")
        bid = snap.get("backup-id")
        if btype and bid:
            grupos.add((btype, bid))

    resultados = []
    for btype, bid in grupos:
        endpoint = f"{BASE}/{datastore}/prune"
        data = {
            "backup-type": btype,
            "backup-id": bid,
            "keep-last": 1
        }
        res = await client.pbs_post(hass, endpoint, data)
        resultados.append(res)

    return resultados


async def run_verify(client, hass, datastore: str):
    _LOGGER.info("PBS: Ejecutando VERIFY automático en %s", datastore)

    snapshots = await client.pbs_get(hass, f"{BASE}/{datastore}/snapshots")
    if not snapshots:
        _LOGGER.warning("PBS: No hay snapshots en %s", datastore)
        return None

    grupos = set()
    for snap in snapshots:
        btype = snap.get("backup-type")
        bid = snap.get("backup-id")
        if btype and bid:
            grupos.add((btype, bid))

    resultados = []
    for btype, bid in grupos:
        endpoint = f"{BASE}/{datastore}/verify"
        data = {
            "backup-type": btype,
            "backup-id": bid,
            "backup-time": 0
        }
        res = await client.pbs_post(hass, endpoint, data)
        resultados.append(res)

    return resultados


async def run_sync(client, hass, datastore: str):
    _LOGGER.info("PBS: Ejecutando SYNC automático en %s", datastore)

    remotes = await client.pbs_get(hass, "remote")
    if not remotes:
        _LOGGER.warning("PBS: No hay remotes configurados en PBS")
        return None

    resultados = []

    for remote in remotes:
        name = remote.get("name")
        stores = remote.get("store", [])

        for store in stores:
            endpoint = f"{BASE}/{datastore}/sync"
            data = {
                "remote": name,
                "remote-store": store
            }
            res = await client.pbs_post(hass, endpoint, data)
            resultados.append(res)

    return resultados
