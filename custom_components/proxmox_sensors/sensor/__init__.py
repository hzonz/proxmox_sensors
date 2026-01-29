"""Sensor platform for Proxmox Sensors Extended."""
from __future__ import annotations
import logging

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr

from .sensor_last_action import PBSLastActionSensor
from ..const import DOMAIN, CONF_NODE, CONF_PLATFORM_TYPE

# Node Sensors
from .node import (
    ProxmoxNodeSensor,
    ProxmoxCPUInfoSensor,
    ProxmoxKSMSensor,
    ProxmoxMemorySensor,
    ProxmoxSwapSensor,
    ProxmoxRootFSSensor,
    ProxmoxClusterTasksSensor,
)

# Hardware Sensors (lm-sensors)
from .hardware import ProxmoxHardwareSensor

# Physical Disks
from .disks import ProxmoxDiskSensor

# Storage
from .storage import ProxmoxStorageSensor, ProxmoxStorageAttributeSensor

# Virtual Machines
from .vm import ProxmoxVMSensor, ProxmoxVMAttributeSensor

# Containers
from .ct import ProxmoxContainerSensor, ProxmoxContainerAttributeSensor

# PBS Sensors
from .pbs import (
    ProxmoxPBSDatastoreUsageSensor,
    ProxmoxPBSDatastoreSizeSensor,
    ProxmoxPBSDedupSensor,
    ProxmoxPBSMaintenanceSensor,
    ProxmoxPBSCpuSensor,
    ProxmoxPBSRamSensor,
    ProxmoxPBSBackupCountSensor,
    ProxmoxPBSLastBackupTimeSensor,
    ProxmoxPBSLastBackupSizeSensor,
    ProxmoxPBSLastBackupStatusSensor,
    ProxmoxPBSBackupErrorsSensor,
    ProxmoxPBSBackupsListSensor,
    ProxmoxPBSTaskSensor,
    ProxmoxPBSTaskTypeSensor,
    ProxmoxPBSTaskStatusSensor,
    ProxmoxPBSTaskMessageSensor,
    ProxmoxPBSTaskDurationSensor,
    ProxmoxPBSAuthStatusSensor,
    ProxmoxPBSVersionSensor,
    ProxmoxPBSReleaseSensor,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up all Proxmox sensors with user-selected filtering."""

    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    selected_vms = entry.data.get("selected_vms", [])
    selected_cts = entry.data.get("selected_cts", [])
    selected_storage = entry.data.get("selected_storage", [])
    enable_physical_disks = entry.data.get("enable_physical_disks", True)
    enable_lm_sensors = entry.data.get("enable_lm_sensors", True)

    node = entry.data.get(CONF_NODE, "Proxmox")
    server_type = entry.data.get(CONF_PLATFORM_TYPE, "PVE")

    entities = []
    c_data = coordinator.data

    if not c_data:
        _LOGGER.warning("No data found in coordinator for %s", node)
        return

    # =================PVE SECTION===================
    if server_type == "PVE":

        # Hardware monitoring (lm-sensors)
        if enable_lm_sensors:
            hardware_data = c_data.get("hardware", {})

            cpu_sensors = []
            pch_sensors = []
            nvme_sensors = []
            sata_sensors = []
            other_sensors = []

            for sensor_id in hardware_data:
                sid = sensor_id.lower()
                
                # CPU: (Intel + AMD + Generics)
                if any(x in sid for x in ["coretemp", "package", "cpu", "k10temp", "zenpower", "tctl", "tdie", "tccd"]):
                    cpu_sensors.append(sensor_id)
                
                # Chipset / Motherboard
                elif any(x in sid for x in ["pch", "acpitz", "it87", "nct67"]):
                    pch_sensors.append(sensor_id)
                
                # NVMe:
                elif any(x in sid for x in ["nvme", "composite"]):
                    nvme_sensors.append(sensor_id)
                
                # Disks SATA / SSD
                elif any(x in sid for x in ["drivetemp", "scsi", "sda", "sdb", "sdc", "sdd", "sde"]):
                    sata_sensors.append(sensor_id)
                
                else:
                    other_sensors.append(sensor_id)

            ordered_sensors = cpu_sensors + pch_sensors + nvme_sensors + sata_sensors + other_sensors

            for sensor_id in ordered_sensors:
                sensor = ProxmoxHardwareSensor(coordinator, sensor_id, node)
                if sensor.is_valid():
                    entities.append(sensor)

        # Node & Cluster monitoring
        node_data = c_data.get("node", {})
        if node_data:
            entities.append(ProxmoxClusterTasksSensor(coordinator, node))

            mapping = {
                "cpuinfo": ProxmoxCPUInfoSensor,
                "ksm": ProxmoxKSMSensor,
                "memory": ProxmoxMemorySensor,
                "swap": ProxmoxSwapSensor,
                "rootfs": ProxmoxRootFSSensor,
            }

            for key, cls in mapping.items():
                if key in node_data:
                    entities.append(cls(coordinator, node))

            for key in node_data:
                if key not in mapping and key not in ("kversion", "boot-info", "last_task"):
                    entities.append(ProxmoxNodeSensor(coordinator, key, node))

        # Physical Disks
        if enable_physical_disks:
            for d_id, d_info in c_data.get("disks", {}).items():
                d_model = str(d_info.get("model", "")).lower()
                if d_model and "boot" not in d_model:
                    entities.append(
                        ProxmoxDiskSensor(coordinator, d_id, node, d_info.get("model") or d_id)
                    )

        # Storage pools
        storage_map = c_data.get("storage", {})
        for st_name, st in storage_map.items():
            if st_name in selected_storage:
                entities.append(ProxmoxStorageSensor(coordinator, st_name, st, node))
                for label, key in [
                    ("Used Space", "used"),
                    ("Free Space", "avail"),
                    ("Total Capacity", "total"),
                    ("Type", "type"),
                    ("Path", "path"),
                ]:
                    entities.append(ProxmoxStorageAttributeSensor(coordinator, st_name, st, label, key, node))

        # Virtual Machines
        vm_map = c_data.get("vms", {})
        for vm_id, vm_data in vm_map.items():
            if str(vm_id) in selected_vms:
                label = vm_data.get("name", vm_id)
                entities.append(ProxmoxVMSensor(coordinator, vm_id, node, label))
                for attr, unit, icon in [
                    ("cpu_usage", "%", "mdi:cpu-64-bit"),
                    ("memory_used", "GB", "mdi:memory"),
                    ("memory_total", "GB", "mdi:memory"),
                    ("disk_total", "GB", "mdi:harddisk-plus"),
                    ("uptime", "h", "mdi:timer-sand"),
                    ("network_rx", "MB", "mdi:download-network"),
                    ("network_tx", "MB", "mdi:upload-network"),
                ]:
                    entities.append(ProxmoxVMAttributeSensor(coordinator, vm_id, node, label, attr, unit, icon))

        # Containers (LXC)
        ct_map = c_data.get("cts", {})
        for ct_id, ct_data in ct_map.items():
            if str(ct_id) in selected_cts:
                label = ct_data.get("name", ct_id)
                entities.append(ProxmoxContainerSensor(coordinator, ct_id, node, label))
                for attr, unit, icon in [
                    ("cpu_usage", "%", "mdi:cpu-64-bit"),
                    ("memory_used", "GB", "mdi:memory"),
                    ("memory_total", "GB", "mdi:memory"),
                    ("disk_total", "GB", "mdi:harddisk-plus"),
                    ("disk_used", "GB", "mdi:harddisk"),
                    ("uptime", "h", "mdi:timer-outline"),
                    ("network_rx", "MB", "mdi:download-network"),
                    ("network_tx", "MB", "mdi:upload-network"),
                ]:
                    entities.append(
                        ProxmoxContainerAttributeSensor(
                            coordinator, ct_id, node, label, attr, unit, icon
                        )
                    )

    # ===================PBS SECTION====================
    elif server_type == "PBS":

        server_id = entry.data["server_id"]

        # Node Hardware Status
        if c_data.get("pbs_node_status"):
            entities.append(ProxmoxPBSCpuSensor(coordinator, server_id))
            entities.append(ProxmoxPBSRamSensor(coordinator, server_id))

        # Datastores
        for store_id in c_data.get("pbs_datastores", {}):

            # NEW SENSOR: Last Action
            entities.append(PBSLastActionSensor(coordinator, store_id))

            entities.append(ProxmoxPBSDatastoreUsageSensor(coordinator, server_id, store_id))

            for key, lbl, icon in [
                ("total", "Total", "mdi:harddisk"),
                ("used", "Used", "mdi:harddisk-remove"),
                ("avail", "Free", "mdi:harddisk-plus"),
            ]:
                entities.append(
                    ProxmoxPBSDatastoreSizeSensor(
                        coordinator, server_id, store_id, key, lbl, icon
                    )
                )

            entities.append(ProxmoxPBSDedupSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSMaintenanceSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSBackupCountSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSLastBackupTimeSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSLastBackupSizeSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSLastBackupStatusSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSBackupErrorsSensor(coordinator, server_id, store_id))
            entities.append(ProxmoxPBSBackupsListSensor(coordinator, server_id, store_id))

        # Global PBS Status
        entities.append(ProxmoxPBSTaskSensor(coordinator, server_id))
        entities.append(ProxmoxPBSTaskTypeSensor(coordinator, server_id))
        entities.append(ProxmoxPBSTaskStatusSensor(coordinator, server_id))
        entities.append(ProxmoxPBSTaskMessageSensor(coordinator, server_id))
        entities.append(ProxmoxPBSTaskDurationSensor(coordinator, server_id))
        entities.append(ProxmoxPBSAuthStatusSensor(coordinator, server_id))
        entities.append(ProxmoxPBSVersionSensor(coordinator, server_id))
        entities.append(ProxmoxPBSReleaseSensor(coordinator, server_id))

    # =========ENTITY AND DEVICE CLEANUP============
    ent_reg = er.async_get(hass)
    existing_entries = er.async_entries_for_config_entry(ent_reg, entry.entry_id)
    new_unique_ids = {entity.unique_id for entity in entities}

    for entity_entry in existing_entries:
        if entity_entry.unique_id not in new_unique_ids:
            _LOGGER.info("Removing obsolete entity: %s", entity_entry.entity_id)
            ent_reg.async_remove(entity_entry.entity_id)

    dev_reg = dr.async_get(hass)
    devices = dr.async_entries_for_config_entry(dev_reg, entry.entry_id)
    for device in devices:
        if not er.async_entries_for_device(ent_reg, device.id):
            _LOGGER.info("Removing orphan device: %s", device.name)
            dev_reg.async_remove_device(device.id)

    if entities:
        async_add_entities(entities)
