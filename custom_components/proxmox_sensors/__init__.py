from __future__ import annotations
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

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

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = entry.data

    host = data[CONF_HOST]
    user = data[CONF_USER]
    node = data[CONF_NODE]
    server_type = data[CONF_PLATFORM_TYPE]

    features = data.get("features", {})

    vm_mode = data.get("vm_mode", "auto")
    vms_selected = data.get("vms", [])
    ct_mode = data.get("ct_mode", "auto")
    cts_selected = data.get("cts", [])
    datastores_selected = data.get("datastores", [])

    password = data.get(CONF_PASSWORD)
    token_id = data.get(CONF_TOKEN_ID)
    token_secret = data.get(CONF_TOKEN_SECRET)

    client = ProxmoxClient(
        host=host,
        user=user,
        password=password,
        token_id=token_id,
        token_secret=token_secret,
        server_type=server_type,
        verify_ssl=False,
    )

    async def async_update_data():
        result = {}
        try:
            _LOGGER.debug("FEATURES: %s", features)

            sensors = await client.get_sensors(hass, node)
            node_status = await client.get_node_status(hass, node)
            disks = await client.get_disks(hass, node)
            vms = await client.get_vms(hass, node)
            cts = await client.get_containers(hass, node)

            local_temps = await client.get_local_temperatures()

            # HARDWARE
            if features.get("enable_hardware", True):
                result["hardware"] = {s["id"]: s["value"] for s in sensors}
                for name, value in local_temps.items():
                    result["hardware"][name] = value

            # NODE
            if features.get("enable_node", True):
                clean_node_status = {k: v for k, v in node_status.items() if k != "cpuinfo"}
                cpuinfo = node_status.get("cpuinfo", {})
                cpuinfo_clean = {k: v for k, v in cpuinfo.items() if k != "flags"}
                clean_node_status["cpuinfo"] = cpuinfo_clean
                result["node"] = clean_node_status

            # DISKS — CORREGIDO
            if features.get("enable_disks", True):
                result["disks"] = {}
                for i, d in enumerate(disks):
                    disk_id = d.get("devpath") or d.get("path") or f"disk_{i}"

                    total = d.get("size") or 0
                    used = 0  # Proxmox no da uso real en este endpoint

                    result["disks"][disk_id] = {
                        "disk_total": total,
                        "disk_used": used,
                        "disk_read": None,
                        "disk_write": None,

                        # Información extendida útil
                        "model": d.get("model"),
                        "serial": d.get("serial"),
                        "type": d.get("type"),
                        "size": d.get("size"),
                        "health": d.get("health"),
                        "wearout": d.get("wearout"),
                        "temperature": d.get("temperature"),
                        "rpm": d.get("rpm"),
                        "devpath": d.get("devpath"),

                        "raw": d,
                    }

            # VMs
            if features.get("enable_vms", True):
                if vm_mode == "auto":
                    result["vms"] = {vm["vmid"]: vm for vm in vms}
                else:
                    result["vms"] = {
                        vm["vmid"]: vm for vm in vms if vm["vmid"] in vms_selected
                    }

            # CTs
            if features.get("enable_cts", True):
                if ct_mode == "auto":
                    result["cts"] = {ct["vmid"]: ct for ct in cts}
                else:
                    result["cts"] = {
                        ct["vmid"]: ct for ct in cts if ct["vmid"] in cts_selected
                    }

            # PBS DATASTORES
            if server_type == "PBS" and features.get("enable_pbs_datastores", True):
                stores = {}
                for store in datastores_selected:
                    stores[store] = await client.get_pbs_datastore_status(hass, store)
                result["pbs_datastores"] = stores

            # PBS TASKS
            if server_type == "PBS" and features.get("enable_pbs_tasks", True):
                last_task = await client.get_pbs_tasks(hass)
                result["pbs_tasks"] = last_task

        except Exception as err:
            _LOGGER.error("Error fetching data from Proxmox: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err

        return result

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="proxmox_sensors",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
        "node": node,
        "server_type": server_type,
        "features": features,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
