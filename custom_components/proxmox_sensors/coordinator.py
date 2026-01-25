# ======COORDINATOR — PROXMOX SENSORS EXTENDED===========

import logging
import asyncio
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_NODE, CONF_PLATFORM_TYPE

_LOGGER = logging.getLogger(__name__)


async def create_proxmox_coordinator(hass, entry, client):

    data = entry.data
    node = data.get(CONF_NODE, "Proxmox")
    server_type = data.get(CONF_PLATFORM_TYPE, "PVE")

    selected_vms = data.get("selected_vms", [])
    selected_cts = data.get("selected_cts", [])
    selected_storage = data.get("selected_storage", [])
    enable_physical_disks = data.get("enable_physical_disks", True)
    enable_lm_sensors = data.get("enable_lm_sensors", True)
    enable_pbs_tasks = data.get("enable_pbs_tasks", True)

    async def async_update_data():

        result = {"server_type": server_type}

        try:
            async with asyncio.timeout(30):

                # =======PBS===========

                if server_type == "PBS":

                    result["pbs_datastores"] = {}
                    result["pbs_snapshots"] = {}
                    result["pbs_gc"] = {}

                    selected = data.get("selected_storage")
                    if not selected:
                        actual_stores = await client.get_pbs_datastores(hass)
                    else:
                        actual_stores = selected

                    for store in actual_stores or []:

                        status = await client.get_pbs_datastore_status(hass, store) or {}
                        usage = await client.get_pbs_datastore_usage(hass, store) or {}
                        backups = await client.get_pbs_backup_list(hass, store) or []

                        backups_sorted = sorted(
                            backups,
                            key=lambda x: x.get("backup-time", 0),
                            reverse=True
                        )

                        last_backup = backups_sorted[0] if backups_sorted else None

                        backup_errors = [
                            b for b in backups_sorted
                            if b.get("verification", {}).get("state") == "failed"
                        ]

                        try:
                            gc_info = await client.get_pbs_gc(hass, store) or {}
                            result["pbs_gc"][store] = gc_info
                        except Exception as e:
                            _LOGGER.error("Error fetching PBS GC info for %s: %s", store, e)
                            result["pbs_gc"][store] = {}

                        try:
                            snapshots = await client.get_pbs_snapshots(hass, store) or []
                            result["pbs_snapshots"][store] = snapshots
                        except Exception as e:
                            _LOGGER.error("Error fetching PBS snapshots for %s: %s", store, e)
                            result["pbs_snapshots"][store] = []

                        result["pbs_datastores"][store] = {
                            **status,
                            **usage,
                            "backup_count": len(backups_sorted),
                            "backups": backups_sorted,
                            "last_backup": last_backup,
                            "backup_errors": backup_errors,
                        }

                    node_status = await client.get_pbs_node_status(hass)
                    result["pbs_node_status"] = node_status if isinstance(node_status, dict) else {}

                    version_info = await client.get_pbs_version(hass) or {}
                    result["pbs_version"] = version_info.get("version")
                    result["pbs_release"] = version_info.get("release")
                    result["pbs_auth_status"] = "OK" if version_info else "ERROR"

                    if enable_pbs_tasks:
                        tasks = await client.get_pbs_tasks(hass) or []
                        result["pbs_tasks"] = tasks if isinstance(tasks, list) else []
                    else:
                        result["pbs_tasks"] = []

                    return result

                # =======PVE===========

                elif server_type == "PVE":

                    node_status = await client.get_node_status(hass, node)
                    result["node"] = node_status if isinstance(node_status, dict) else {}

                    try:
                        interfaces = await client.get_node_network(hass, node)
                        if isinstance(interfaces, list):
                            rx = sum(i.get("rx_bytes", 0) for i in interfaces)
                            tx = sum(i.get("tx_bytes", 0) for i in interfaces)
                            result["node"]["network_rx"] = rx
                            result["node"]["network_tx"] = tx
                    except Exception as e:
                        _LOGGER.error("Error fetching node network traffic: %s", e)

                    result["hardware"] = {}

                    if enable_lm_sensors:
                        lm = await client.get_lm_sensors_http(hass, node)
                        if isinstance(lm, dict):
                            for chip, values in lm.items():
                                if isinstance(values, dict):
                                    for k, v in values.items():
                                        result["hardware"][f"{chip}_{k}".lower()] = v

                    resource_tasks = []
                    resource_keys = []

                    resource_tasks.append(client.get_cluster_tasks(hass))
                    resource_keys.append("cluster_tasks")

                    resource_tasks.append(client.get_vms(hass, node))
                    resource_keys.append("vms")

                    resource_tasks.append(client.get_containers(hass, node))
                    resource_keys.append("cts")

                    resource_tasks.append(client.get_storages(hass, node))
                    resource_keys.append("storage")

                    if enable_physical_disks:
                        resource_tasks.append(client.get_disks(hass, node))
                        resource_keys.append("disks")

                    results = await asyncio.gather(*resource_tasks, return_exceptions=True)

                    for key, res in zip(resource_keys, results):
                        if isinstance(res, Exception):
                            _LOGGER.error("Error fetching %s: %s", key, res)
                            result[key] = {} if key != "cluster_tasks" else []
                            continue

                        # ----CLUSTER TASKS--------

                        if key == "cluster_tasks":
                            result["tasks"] = res if isinstance(res, list) else []
                            if isinstance(res, list) and len(res) > 0:
                                last = res[0]
                                result["node"]["last_task"] = {
                                    "status": last.get("status") or "running",
                                    "type": last.get("type", "unknown"),
                                    "user": last.get("user", "unknown"),
                                    "id": last.get("id", "node"),
                                    "endtime": last.get("endtime")
                                }
                            else:
                                result["node"]["last_task"] = None

                        # -----VMs--------

                        elif key == "vms":
                            vms_dict = {}
                            for vm in res or []:
                                vmid = vm.get("vmid")
                                if vmid is None or str(vmid) not in selected_vms:
                                    continue

                                base = dict(vm)

                                try:
                                    status_raw = await client.get_vm_status(hass, node, vmid)
                                    detailed = None

                                    if isinstance(status_raw, list) and status_raw:
                                        detailed = status_raw[0]
                                    elif isinstance(status_raw, dict):
                                        detailed = status_raw.get("data") if isinstance(status_raw.get("data"), dict) else status_raw

                                    if isinstance(detailed, dict):
                                        base.update({k: v for k, v in detailed.items() if v is not None})

                                except Exception as e:
                                    _LOGGER.error("Error fetching VM status %s: %s", vmid, e)

                                for field in ["cpu", "mem", "maxmem", "disk", "maxdisk", "uptime", "netin", "netout"]:
                                    base.setdefault(field, 0)

                                base.setdefault("status", "unknown")
                                vms_dict[vmid] = base

                            result["vms"] = vms_dict

                        # -----CTs---------

                        elif key == "cts":
                            cts_dict = {}
                            for ct in res or []:
                                vmid = ct.get("vmid")
                                if vmid is None or str(vmid) not in selected_cts:
                                    continue

                                base = dict(ct)

                                try:
                                    status_raw = await client.get_container_status(hass, node, vmid)

                                    detailed = None
                                    if isinstance(status_raw, list) and status_raw:
                                        detailed = status_raw[0]
                                    elif isinstance(status_raw, dict):
                                        detailed = status_raw.get("data") if isinstance(status_raw.get("data"), dict) else status_raw

                                    if isinstance(detailed, dict):
                                        base.update({k: v for k, v in detailed.items() if v is not None})

                                except Exception as e:
                                    _LOGGER.error("Error fetching CT status %s: %s", vmid, e)

                                for field in ["cpu", "mem", "maxmem", "disk", "maxdisk", "uptime", "netin", "netout"]:
                                    base.setdefault(field, 0)

                                base.setdefault("status", "unknown")
                                cts_dict[vmid] = base

                            result["cts"] = cts_dict

                        # -----STORAGE----------

                        elif key == "storage":
                            result["storage"] = {
                                st["storage"]: st for st in res
                                if isinstance(st, dict) and "storage" in st and st["storage"] in selected_storage
                            }

                        # ----DISKS-----------

                        elif key == "disks":
                            result["disks"] = {
                                d.get("devpath", f"disk_{i}"): d for i, d in enumerate(res or [])
                            }

        except Exception as err:
            _LOGGER.exception("Coordinator update failure")
            raise UpdateFailed(f"Update error: {err}")

        return result

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"proxmox_{server_type}_{node}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),
    )

    coordinator.client = client
    coordinator.api = client
    return coordinator
