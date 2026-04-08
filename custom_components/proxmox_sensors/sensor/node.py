"""Node sensors for Proxmox (CPU, Memory, Tasks, and System)."""

from .base import ProxmoxBaseSensor
from ..const import DOMAIN
from ..logic.node_metrics import (
    build_cluster_task_attributes,
    build_cpu_sensor_attributes,
    build_iowait_attributes,
    build_node_load_attributes,
    build_node_overview_attributes,
    build_storage_summary_attributes,
    calculate_node_score,
    calculate_percentage_usage,
    classify_node_score,
    format_node_sensor_value,
    parse_load_average,
    bytes_to_gb,
)

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity, SensorStateClass
import logging

_LOGGER = logging.getLogger(__name__)


class ProxmoxNodeSensor(ProxmoxBaseSensor):
    """General node sensors."""

    def __init__(self, coordinator, sensor_id, node):
        unit = None
        icon = "mdi:information-outline"
        state_class = None
        name = sensor_id.replace("_", " ").title()

        if sensor_id == "cpu":
            name = "CPU Usage"
            unit = "%"
            icon = "mdi:cpu-64-bit"
            state_class = "measurement"

        elif sensor_id == "wait":
            name = "CPU Wait"
            unit = "%"
            icon = "mdi:timer-sand"
            state_class = "measurement"

        elif sensor_id == "uptime":
            name = "Uptime"
            icon = "mdi:clock-outline"

        elif sensor_id == "kversion":
            name = "Kernel Version"
            icon = "mdi:linux"

        elif sensor_id == "pveversion":
            name = "PVE Version"
            icon = "mdi:numeric"

        elif sensor_id == "loadavg":
            name = "Load Average"
            icon = "mdi:chart-line"

        elif sensor_id == "network_rx":
            name = "Network RX"
            unit = "bytes"
            icon = "mdi:download-network"
            state_class = "measurement"

        elif sensor_id == "network_tx":
            name = "Network TX"
            unit = "bytes"
            icon = "mdi:upload-network"
            state_class = "measurement"

        name = f"{name} ({node})"

        unique_id = f"proxmox_node_{node}_{sensor_id}"
        super().__init__(coordinator, sensor_id, name, unit, unique_id, node)

        self._attr_icon = icon
        self._attr_state_class = state_class

    def _get_value(self):
        value = self.coordinator.data.get("node", {}).get(self._sensor_id)
        return format_node_sensor_value(self._sensor_id, value)

    @property
    def extra_state_attributes(self):
        # Apply only to CPU sensor
        if self._sensor_id != "cpu":
            return {}

        node_data = self.coordinator.data.get("node", {})
        return build_cpu_sensor_attributes(node_data)


class ProxmoxClusterTasksSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        uid = f"proxmox_{node}_cluster_tasks"
        super().__init__(coordinator, "last_task", "Last Task", None, uid, node)

    def _get_value(self):
        task = self.coordinator.data.get("node", {}).get("last_task")
        if not task:
            return "No Tasks"
        return f"{task.get('type', 'unknown')}: {task.get('status', 'unknown')}"

    @property
    def extra_state_attributes(self):
        task = self.coordinator.data.get("node", {}).get("last_task", {})
        tasks_list = self.coordinator.data.get("tasks", [])
        return build_cluster_task_attributes(task, tasks_list)


class ProxmoxCPUInfoSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "cpuinfo", "CPU Info", None, f"p_node_cpu_{node}", node
        )
        self._attr_icon = "mdi:cpu-64-bit"

    def _get_value(self):
        info = self.coordinator.data.get("node", {}).get("cpuinfo", {})
        return info.get("model") or f"{info.get('cores', '?')} cores"


class ProxmoxKSMSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "ksm", "KSM Shared", "GB", f"p_node_ksm_{node}", node
        )
        self._attr_icon = "mdi:memory-arrow-down"

    def _get_value(self):
        val = self.coordinator.data.get("node", {}).get("ksm", {}).get("shared", 0)
        return bytes_to_gb(val)


class ProxmoxMemorySensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "memory", "Memory Usage", "%", f"p_node_mem_{node}", node
        )
        self._attr_icon = "mdi:memory"

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("memory", {})
        return calculate_percentage_usage(data.get("used", 0), data.get("total", 1))


class ProxmoxSwapSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "swap", "Swap Usage", "%", f"p_node_swap_{node}", node
        )
        self._attr_icon = "mdi:swap-horizontal"

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("swap", {})
        return calculate_percentage_usage(
            data.get("used", 0), data.get("total", 0), zero_total_value=0
        )


class ProxmoxRootFSSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "rootfs",
            "Root FS Usage",
            "%",
            f"p_node_rootfs_{node}",
            node,
        )
        self._attr_icon = "mdi:folder"

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("rootfs", {})
        return calculate_percentage_usage(data.get("used", 0), data.get("total", 1))


class ProxmoxNodeUpdatesSensor(ProxmoxBaseSensor):
    """Sensor for node updates."""

    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "node_updates",
            "Node Updates",
            None,
            f"p_node_updates_{node}",
            node,
        )
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def _get_value(self):
        data = self.coordinator.data.get("node_updates", {})

        if data.get("error"):
            return None

        return data.get("count", 0)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("node_updates", {})

        if data.get("error"):
            return {
                "error": True,
                "message": "Failed to fetch updates",
            }

        packages = data.get("packages", [])

        return {
            "available": data.get("available", False),
            "count": data.get("count", 0),
            "packages": [
                f"{p.get('Package')} ({p.get('OldVersion')} → {p.get('Version')})"
                for p in packages
                if isinstance(p, dict) and p.get("Package")
            ],
        }

    @property
    def icon(self):
        data = self.coordinator.data.get("node_updates", {})

        if data.get("error"):
            return "mdi:alert-circle"

        if data.get("count", 0) > 0:
            return "mdi:package-up"

        return "mdi:package-check"


class ProxmoxClusterNotificationsSensor(ProxmoxBaseSensor):
    """Sensor exposing parsed cluster notification settings."""

    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "cluster_notifications",
            "Cluster Notifications",
            None,
            f"p_cluster_notifications_{node}",
            node,
        )

    def _get_value(self):
        data = self.coordinator.data.get("cluster_notifications", {})
        value = data.get("package_updates")

        if not value or value in ("unknown", "not_configured"):
            return "Not configured"

        return value

    @property
    def icon(self):
        value = self._get_value()

        if value == "Not configured":
            return "mdi:bell-off"
        if value == "always":
            return "mdi:bell-ring"
        if value == "auto":
            return "mdi:bell-cog"
        if value == "never":
            return "mdi:bell-off"

        return "mdi:bell"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("cluster_notifications", {})
        return {
            "package_updates": data.get("package_updates"),
            "replication": data.get("replication"),
            "fencing": data.get("fencing"),
            "target_package_updates": data.get("target_package_updates"),
            "target_package_updates_type": data.get("target_package_updates_type"),
            "target_package_updates_server": data.get("target_package_updates_server"),
            "target_package_updates_origin": data.get("target_package_updates_origin"),
        }


class ProxmoxPackageUpdatesModeSensor(ProxmoxBaseSensor):
    """Sensor exposing the configured package update notification mode."""

    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "package_updates_mode",
            "Package Updates Mode",
            None,
            f"p_package_updates_mode_{node}",
            node,
        )

    def _get_value(self):
        data = self.coordinator.data.get("cluster_notifications", {})
        value = data.get("package_updates")

        if not value or value in ("unknown", "not_configured"):
            return "Not configured"

        return value

    @property
    def icon(self):
        value = self._get_value()

        if value == "Not configured":
            return "mdi:package-variant-remove"
        if value == "always":
            return "mdi:package-variant-closed-check"
        if value == "auto":
            return "mdi:package-variant"
        if value == "never":
            return "mdi:package-variant-closed-remove"

        return "mdi:package-variant-closed-alert"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("cluster_notifications", {})
        return {
            "target_package_updates": data.get("target_package_updates"),
            "target_package_updates_type": data.get("target_package_updates_type"),
            "target_package_updates_server": data.get("target_package_updates_server"),
            "target_package_updates_origin": data.get("target_package_updates_origin"),
        }


class ProxmoxNodesSensor(CoordinatorEntity, SensorEntity):
    """Sensor that shows configured node and its statistics."""

    def __init__(self, coordinator, entry_id, node):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._node = node
        self._attr_name = f"Proxmox Node: {node}"
        self._attr_unique_id = f"{entry_id}_node_info"
        self._attr_icon = "mdi:server"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
            "name": f"1. Node: {self._node}",
        }

    @property
    def native_value(self):
        data = self.coordinator.data

        node_status = data.get("node_status_map", {}).get(self._node, "unknown")

        if node_status != "online":
            return "offline"

        return classify_node_score(calculate_node_score(data.get("node", {})))

    @property
    def extra_state_attributes(self):
        return build_node_overview_attributes(self.coordinator.data, self._node)


class ProxmoxStoragesSensor(CoordinatorEntity, SensorEntity):
    """Sensor listing all available storages in configured node."""

    def __init__(self, coordinator, entry_id, node):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._node = node
        self._attr_name = f"Proxmox Storages ({node})"
        self._attr_unique_id = f"{entry_id}_storages_{node}"
        self._attr_icon = "mdi:database"

    def _get_storage_data(self):
        """Get storage data from coordinator, checking multiple possible structures."""
        data = self.coordinator.data

        if "storages_by_node" in data:
            node_storages = data["storages_by_node"].get(self._node, {})
            if node_storages:
                return node_storages

        if "storage" in data and data["storage"]:
            return data["storage"]

        if "all_storages" in data and self._node in data["all_storages"]:
            if "storage" in data:
                return data["storage"]

        return {}

    @property
    def native_value(self):
        storage_data = self._get_storage_data()
        return len(storage_data)

    @property
    def extra_state_attributes(self):
        storage_data = self._get_storage_data()
        return build_storage_summary_attributes(
            storage_data,
            self._node,
            self.coordinator.data.get("last_update", "unknown"),
        )

    @property
    def device_info(self):
        node_id = self._node.lower()
        display_node = self._node.capitalize()

        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{node_id}")},
            "name": f"1. Node: {display_node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }


class ProxmoxNodeIOWaitSensor(ProxmoxBaseSensor):
    """Sensor for node IO wait (disk pressure)."""

    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "wait",
            "IO Wait",
            "%",
            f"p_node_iowait_{node}",
            node,
        )
        self._attr_icon = "mdi:harddisk"
        self._attr_state_class = "measurement"

    def _get_value(self):
        value = self.coordinator.data.get("node", {}).get("wait", 0)
        return format_node_sensor_value("wait", value) or 0

    @property
    def extra_state_attributes(self):
        value = self.coordinator.data.get("node", {}).get("wait", 0)
        return build_iowait_attributes(value)


class ProxmoxNodeLoadAverageSensor(ProxmoxBaseSensor):
    """Sensor for node load average (1 min)."""

    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "loadavg_1m",
            "Load Average (1m)",
            None,
            f"p_node_load1_{node}",
            node,
        )
        self._attr_icon = "mdi:chart-line"

    def _get_value(self):
        load = self.coordinator.data.get("node", {}).get("loadavg", [])
        if isinstance(load, list) and len(load) >= 1:
            load1 = parse_load_average(load, 0, None)
            return round(load1, 2) if load1 is not None else None
        return None

    @property
    def extra_state_attributes(self):
        node_data = self.coordinator.data.get("node", {})
        return build_node_load_attributes(node_data)


class ProxmoxNodeScoreSensor(ProxmoxBaseSensor):
    """Overall node performance score (lower is better)."""

    def __init__(self, coordinator, node):
        super().__init__(
            coordinator,
            "node_score",
            "Node Score",
            None,
            f"p_node_score_{node}",
            node,
        )
        self._attr_icon = "mdi:speedometer"

    def _get_value(self):
        return calculate_node_score(self.coordinator.data.get("node", {}))

    @property
    def extra_state_attributes(self):
        score = self.native_value or 0

        return {
            "interpretation": "Lower is better",
            "state": classify_node_score(score),
        }


class PVEBackupProgressSensor(ProxmoxBaseSensor):
    """Sensor for backup progress in PVE using available tasks data."""

    def __init__(self, coordinator, node, entry_id):
        name = "Backup Progress"
        uid = f"proxmox_backup_progress_{node}"

        super().__init__(
            coordinator,
            node,
            name,
            None,
            uid,
            node,
        )

        self._attr_icon = "mdi:backup-restore"

    def _get_backup_tasks(self):
        data = self.coordinator.data
        backup_tasks = []

        if "tasks" in data:
            for task in data["tasks"]:
                if (
                    "vzdump" in str(task.get("type", "")).lower()
                    or "backup" in str(task.get("id", "")).lower()
                    or "vzdump" in str(task.get("upid", "")).lower()
                ) and task.get("node") == self._node:
                    backup_tasks.append(
                        {
                            "id": task.get("id", task.get("upid", "unknown")),
                            "vmid": self._extract_vmid(task),
                            "type": task.get("type", "unknown"),
                            "status": task.get("status", "unknown"),
                            "upid": task.get("upid", ""),
                            "starttime": task.get("starttime", 0),
                            "endtime": task.get("endtime", 0),
                            "user": task.get("user", "unknown"),
                            "storage": "unknown",
                            "node": task.get("node", "unknown"),
                        }
                    )
        return backup_tasks

    def _extract_vmid(self, task):
        upid = str(task.get("upid", ""))

        try:
            if "vm/" in upid:
                return upid.split("vm/")[1].split(":")[0]
            if "ct/" in upid:
                return upid.split("ct/")[1].split(":")[0]
        except Exception:
            pass

        return "unknown"

    @property
    def native_value(self):
        backup_tasks = self._get_backup_tasks()

        if not backup_tasks:
            return "idle"

        from time import time

        current_time = time()
        recent_tasks = [
            t for t in backup_tasks if t.get("starttime", 0) > (current_time - 86400)
        ]

        if not recent_tasks:
            return "idle"

        running = [t for t in recent_tasks if t.get("status") == "running"]
        failed = [t for t in recent_tasks if t.get("status") in ["error", "failed"]]
        completed = [t for t in recent_tasks if t.get("status") == "OK"]

        if running:
            return "running"
        elif failed:
            return "error"
        elif completed:
            return "ok"
        else:
            return "idle"

    @property
    def extra_state_attributes(self):
        backup_tasks = self._get_backup_tasks()

        if not backup_tasks:
            return {
                "status": "no_backups",
                "node": self._node,
                "message": "No backup tasks found in last 24 hours",
            }

        from time import time

        current_time = time()
        recent_tasks = [
            t for t in backup_tasks if t.get("starttime", 0) > (current_time - 86400)
        ]

        if not recent_tasks:
            return {
                "status": "no_recent_backups",
                "node": self._node,
                "message": "No backup tasks in last 24 hours",
            }

        running_tasks = [t for t in recent_tasks if t.get("status") == "running"]
        completed_tasks = [t for t in recent_tasks if t.get("status") == "OK"]
        failed_tasks = [
            t for t in recent_tasks if t.get("status") in ["error", "failed"]
        ]
        other_tasks = [
            t
            for t in recent_tasks
            if t.get("status") not in ["running", "OK", "error", "failed"]
        ]

        recent_backups_list = []
        for task in sorted(
            recent_tasks, key=lambda x: x.get("starttime", 0), reverse=True
        )[:10]:
            duration = None
            if task.get("starttime") and task.get("endtime"):
                duration = task.get("endtime") - task.get("starttime")

            recent_backups_list.append(
                {
                    "vmid": task.get("vmid"),
                    "status": task.get("status"),
                    "user": task.get("user"),
                    "starttime": task.get("starttime"),
                    "endtime": task.get("endtime"),
                    "duration": duration,
                }
            )

        current_task = running_tasks[0] if running_tasks else None

        total = len(recent_tasks)
        completed = len([t for t in recent_tasks if t.get("status") == "OK"])

        percentage = round((completed / total) * 100, 1) if total > 0 else 0

        return {
            "node": self._node,
            "total_backups_last_24h": len(recent_tasks),
            "running": len(running_tasks),
            "completed": len(completed_tasks),
            "percentage": percentage,
            "failed": len(failed_tasks),
            "other": len(other_tasks),
            "last_update": self.coordinator.data.get("last_update", "unknown"),
            "current_task": (
                {
                    "vmid": self._extract_vmid(current_task),
                    "user": current_task.get("user"),
                    "starttime": current_task.get("starttime"),
                    "upid": current_task.get("upid"),
                }
                if current_task
                else "idle"
            ),
            "recent_backups": recent_backups_list,
            "all_backups_count": len(backup_tasks),
        }

    @property
    def icon(self):
        state = self.native_value

        if state == "running":
            return "mdi:backup-restore"
        elif state == "error":
            return "mdi:alert"
        elif state == "ok":
            return "mdi:check-circle"
        else:
            return "mdi:sleep"
