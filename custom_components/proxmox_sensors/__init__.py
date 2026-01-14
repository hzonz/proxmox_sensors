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
    CONF_NODE,
)

from .api import ProxmoxClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Proxmox Sensors from a config entry."""

    data = entry.data

    host = data[CONF_HOST]
    user = data[CONF_USER]
    password = data[CONF_PASSWORD]
    node = data[CONF_NODE]
    server_type = data["server_type"]

    features = data["features"]

    # User selections
    hardware_selected = data.get("hardware_sensors")
    node_selected = data.get("node_sensors")
    disks_selected = data.get("disks")
    vm_mode = data.get("vm_mode")
    vms_selected = data.get("vms")
    ct_mode = data.get("ct_mode")
    cts_selected = data.get("cts")
    datastores_selected = data.get("datastores")

    client = ProxmoxClient(
        host,
        user,
        password,
        server_type=server_type,
    )

    async def async_update_data():
        """Fetch all enabled sensor data from Proxmox/PBS."""
        result = {}

        try:
            # ---------------------------------------------------------
            # HARDWARE SENSORS
            # ---------------------------------------------------------
            if features.get("enable_hardware"):
                sensors = await client.get_sensors(node)
                result["hardware"] = {
                    s["id"]: s["value"]
                    for s in sensors
                    if s["id"] in hardware_selected
                }

            # ---------------------------------------------------------
            # NODE SENSORS
            # ---------------------------------------------------------
            if features.get("enable_node"):
                node_status = await client.get_node_status(node)
                result["node"] = {
                    key: node_status.get(key)
                    for key in node_selected
                }

            # ---------------------------------------------------------
            # DISKS
            # ---------------------------------------------------------
            if features.get("enable_disks"):
                disks = await client.get_disks(node)
                result["disks"] = {
                    d["id"]: d
                    for d in disks
                    if d["id"] in disks_selected
                }

            # ---------------------------------------------------------
            # VMs
            # ---------------------------------------------------------
            if features.get("enable_vms"):
                vms = await client.get_vms(node)

                if vm_mode == "auto":
                    result["vms"] = {vm["id"]: vm for vm in vms}
                else:
                    result["vms"] = {
                        vm["id"]: vm
                        for vm in vms
                        if vm["id"] in vms_selected
                    }

            # ---------------------------------------------------------
            # CONTAINERS
            # ---------------------------------------------------------
            if features.get("enable_cts"):
                cts = await client.get_containers(node)

                if ct_mode == "auto":
                    result["cts"] = {ct["id"]: ct for ct in cts}
                else:
                    result["cts"] = {
                        ct["id"]: ct
                        for ct in cts
                        if ct["id"] in cts_selected
                    }

            # ---------------------------------------------------------
            # PBS DATASTORES
            # ---------------------------------------------------------
            if server_type == "PBS" and features.get("enable_pbs_datastores"):
                stores = {}
                for store in datastores_selected:
                    stores[store] = await client.get_pbs_datastore_status(store)
                result["pbs_datastores"] = stores

            # ---------------------------------------------------------
            # PBS TASKS (always automatic)
            # ---------------------------------------------------------
            if server_type == "PBS" and features.get("enable_pbs_tasks"):
                last_task = await client.get_pbs_tasks()
                result["pbs_tasks"] = last_task

        except Exception as err:
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
        "hardware_sensors": hardware_selected,
        "node_sensors": node_selected,
        "disks": disks_selected,
        "vm_mode": vm_mode,
        "vms": vms_selected,
        "ct_mode": ct_mode,
        "cts": cts_selected,
        "datastores": datastores_selected,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
