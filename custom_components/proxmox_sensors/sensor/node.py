"""Node sensors for Proxmox (CPU, Memory, Tasks, and System)."""

from .base import ProxmoxBaseSensor
from ..const import DOMAIN

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

        if sensor_id == "cpu":
            self._attr_translation_key = "cpu_usage"
            unit = "%"
            icon = "mdi:cpu-64-bit"
            state_class = "measurement"

        elif sensor_id == "wait":
            self._attr_translation_key = "cpu_wait"
            unit = "%"
            icon = "mdi:timer-sand"
            state_class = "measurement"

        elif sensor_id == "uptime":
            self._attr_translation_key = "uptime"
            icon = "mdi:clock-outline"

        elif sensor_id == "kversion":
            self._attr_translation_key = "kernel_version"
            icon = "mdi:linux"

        elif sensor_id == "pveversion":
            self._attr_translation_key = "pve_version"
            icon = "mdi:numeric"

        elif sensor_id == "loadavg":
            self._attr_translation_key = "load_average"
            icon = "mdi:chart-line"

        elif sensor_id == "network_rx":
            self._attr_translation_key = "network_rx"
            unit = "bytes"
            icon = "mdi:download-network"
            state_class = "measurement"

        elif sensor_id == "network_tx":
            self._attr_translation_key = "network_tx"
            unit = "bytes"
            icon = "mdi:upload-network"
            state_class = "measurement"

        else:
            self._attr_translation_key = sensor_id.lower()

        unique_id = f"proxmox_node_{node}_{sensor_id}"
        super().__init__(
            coordinator, sensor_id, self._attr_translation_key, unit, unique_id, node
        )

        self._attr_icon = icon
        self._attr_state_class = state_class

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        value = self.coordinator.data.get("node", {}).get(self._sensor_id)

        if self._sensor_id == "pveversion" and isinstance(value, str):
            parts = value.split("/")
            if len(parts) >= 2:
                return parts[1]

        if self._sensor_id in ["cpu", "wait"] and isinstance(value, (int, float)):
            return round(value * 100, 2)

        if self._sensor_id == "uptime" and isinstance(value, (int, float)):
            days = int(value // 86400)
            hours = int((value % 86400) // 3600)
            minutes = int((value % 3600) // 60)
            return f"{days}d {hours}h {minutes}m"

        if isinstance(value, dict):
            return (
                value.get("release") or value.get("version", "").split("\n")[0] or None
            )

        if isinstance(value, str):
            return value.split("\n")[0]

        return value


class ProxmoxClusterTasksSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        uid = f"proxmox_{node}_cluster_tasks"
        super().__init__(coordinator, "last_task", "Last Task", None, uid, node)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        task = self.coordinator.data.get("node", {}).get("last_task")
        if not task:
            return "No Tasks"
        return f"{task.get('type', 'unknown')}: {task.get('status', 'unknown')}"

    @property
    def extra_state_attributes(self):
        task = self.coordinator.data.get("node", {}).get("last_task", {})
        tasks_list = self.coordinator.data.get("tasks", [])

        errors = [
            f"{t.get('type')}: {t.get('status')}"
            for t in tasks_list
            if t.get("status") and "OK" not in t.get("status")
        ]

        return {
            "user": task.get("user"),
            "status_raw": task.get("status"),
            "recent_errors": errors[:5] if errors else 0,
        }


class ProxmoxCPUInfoSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "cpuinfo", "CPU Info", None, f"p_node_cpu_{node}", node
        )
        self._attr_icon = "mdi:cpu-64-bit"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        info = self.coordinator.data.get("node", {}).get("cpuinfo", {})
        return info.get("model") or f"{info.get('cores', '?')} cores"


class ProxmoxKSMSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "ksm", "KSM Shared", "GB", f"p_node_ksm_{node}", node
        )
        self._attr_icon = "mdi:memory-arrow-down"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        val = self.coordinator.data.get("node", {}).get("ksm", {}).get("shared", 0)
        return round(val / (1024**3), 2)


class ProxmoxMemorySensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "memory", "Memory Usage", "%", f"p_node_mem_{node}", node
        )
        self._attr_icon = "mdi:memory"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("memory", {})
        used = data.get("used", 0)
        total = data.get("total", 1)
        return round((used / total) * 100, 2)


class ProxmoxSwapSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(
            coordinator, "swap", "Swap Usage", "%", f"p_node_swap_{node}", node
        )
        self._attr_icon = "mdi:swap-horizontal"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("swap", {})
        total = data.get("total", 0)
        if total == 0:
            return 0
        return round((data.get("used", 0) / total) * 100, 2)


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

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("rootfs", {})
        total = data.get("total", 1)
        return round((data.get("used", 0) / total) * 100, 2)


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
        return self._node

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        node_data = data.get("node", {})

        vm_count = 0
        ct_count = 0

        if "vms" in data:
            for vm_id, vm_info in data["vms"].items():
                if isinstance(vm_info, dict) and vm_info.get("node") == self._node:
                    vm_count += 1

        if "cts" in data:
            for ct_id, ct_info in data["cts"].items():
                if isinstance(ct_info, dict) and ct_info.get("node") == self._node:
                    ct_count += 1

        storage_count = 0
        storage_details = []

        if "storage" in data:
            storage_count = len(data["storage"])
            for storage_name, storage_info in data["storage"].items():
                if isinstance(storage_info, dict):
                    storage_details.append(
                        {
                            "name": storage_name,
                            "type": storage_info.get("type", "unknown"),
                            "total_gb": round(
                                storage_info.get("total", 0) / (1024**3), 2
                            ),
                            "used_gb": round(
                                storage_info.get("used", 0) / (1024**3), 2
                            ),
                            "free_gb": round(
                                storage_info.get("avail", 0) / (1024**3), 2
                            ),
                            "percentage": storage_info.get("percentage", 0),
                        }
                    )

        node_status = node_data.get("status", "unknown")
        cpu_usage = node_data.get("cpu", 0)
        if isinstance(cpu_usage, (int, float)):
            cpu_usage = round(cpu_usage * 100, 2)

        memory_data = node_data.get("memory", {})
        memory_used = memory_data.get("used", 0)
        memory_total = memory_data.get("total", 1)
        memory_percentage = (
            round((memory_used / memory_total) * 100, 2) if memory_total > 0 else 0
        )

        active_tasks = 0
        if "tasks" in data:
            for task in data["tasks"]:
                if isinstance(task, dict) and task.get("node") == self._node:
                    if task.get("status") not in ["OK", "stopped"]:
                        active_tasks += 1

        return {
            "node_name": self._node,
            "status": node_status,
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_percentage,
            "vm_count": vm_count,
            "ct_count": ct_count,
            "storage_count": storage_count,
            "active_tasks": active_tasks,
            "storage_details": storage_details,
            "last_update": data.get("last_update", "unknown"),
            "pve_version": node_data.get("pveversion", "unknown"),
            "kernel_version": node_data.get("kversion", "unknown"),
            "uptime_seconds": node_data.get("uptime", 0),
        }


class ProxmoxStoragesSensor(CoordinatorEntity, SensorEntity):
    """Sensor listing all available storages in configured node."""

    def __init__(self, coordinator, entry_id, node):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._node = node
        self._attr_name = f"Proxmox Storages ({node})"
        self._attr_unique_id = f"{entry_id}_storages_{node}"
        self._attr_icon = "mdi:database"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
            "name": f"1. Node: {self._node}",
        }

    def _format_size(self, bytes_size):
        if bytes_size == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(bytes_size)

        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024
            i += 1

        if i >= 3:
            return f"{size:.2f} {size_names[i]}"
        elif i >= 1:
            return f"{size:.1f} {size_names[i]}"
        else:
            return f"{size:.0f} {size_names[i]}"

    def _bytes_to_gb(self, bytes_size):
        if not bytes_size:
            return 0
        return round(bytes_size / (1024**3), 2)

    @property
    def native_value(self):
        data = self.coordinator.data
        if "storage" in data:
            return len(data["storage"])
        return 0

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data

        if "storage" not in data:
            return {
                "node": self._node,
                "storages": [],
                "count": 0,
                "message": "No storage data available",
            }

        storages_list = []
        total_capacity_bytes = 0
        total_used_bytes = 0
        total_free_bytes = 0
        type_accumulators = {}

        for storage_name, storage_info in data["storage"].items():
            if isinstance(storage_info, dict):
                total_bytes = storage_info.get("total", 0)
                used_bytes = storage_info.get("used", 0)
                free_bytes = storage_info.get("avail", 0)
                percentage = storage_info.get("percentage", 0)
                storage_type = storage_info.get("type", "unknown")

                if storage_type not in type_accumulators:
                    type_accumulators[storage_type] = {"count": 0, "total_bytes": 0}
                type_accumulators[storage_type]["count"] += 1
                type_accumulators[storage_type]["total_bytes"] += total_bytes

                total_gb = self._bytes_to_gb(total_bytes)
                used_gb = self._bytes_to_gb(used_bytes)
                free_gb = self._bytes_to_gb(free_bytes)

                storages_list.append(
                    {
                        "name": storage_name,
                        "type": storage_type,
                        "path": storage_info.get("path", ""),
                        "content": storage_info.get("content", ""),
                        "total": self._format_size(total_bytes),
                        "used": self._format_size(used_bytes),
                        "free": self._format_size(free_bytes),
                        "total_gb": total_gb,
                        "used_gb": used_gb,
                        "free_gb": free_gb,
                        "percentage": percentage,
                        "active": storage_info.get("active", 1) == 1,
                        "enabled": storage_info.get("enabled", 1) == 1,
                    }
                )

                total_capacity_bytes += total_bytes
                total_used_bytes += used_bytes
                total_free_bytes += free_bytes

        total_capacity_gb = self._bytes_to_gb(total_capacity_bytes)
        total_used_gb = self._bytes_to_gb(total_used_bytes)
        total_free_gb = self._bytes_to_gb(total_free_bytes)

        total_percentage = (
            round((total_used_bytes / total_capacity_bytes * 100), 1)
            if total_capacity_bytes > 0
            else 0
        )

        by_type = {}
        for storage_type, accumulator in type_accumulators.items():
            total_bytes_for_type = accumulator["total_bytes"]
            by_type[storage_type] = {
                "count": accumulator["count"],
                "total_capacity": self._format_size(total_bytes_for_type),
                "total_capacity_gb": self._bytes_to_gb(total_bytes_for_type),
            }

        return {
            "node": self._node,
            "storages": [s["name"] for s in storages_list],
            "count": len(storages_list),
            "storage_details": storages_list,
            "total_capacity": self._format_size(total_capacity_bytes),
            "total_used": self._format_size(total_used_bytes),
            "total_free": self._format_size(total_free_bytes),
            "total_capacity_gb": total_capacity_gb,
            "total_used_gb": total_used_gb,
            "total_free_gb": total_free_gb,
            "total_percentage": total_percentage,
            "by_type": by_type,
            "last_update": data.get("last_update", "unknown"),
            "summary": f"{len(storages_list)} storages, {self._format_size(total_capacity_bytes)} total, {total_percentage}% used",
        }


class PVEBackupProgressSensor(CoordinatorEntity, SensorEntity):
    """Sensor for backup progress in PVE using available tasks data."""

    def __init__(self, coordinator, node, entry_id):
        super().__init__(coordinator)
        self._node = node
        self._entry_id = entry_id
        self._attr_name = f"PVE Backup Progress ({node})"
        self._attr_unique_id = f"{entry_id}_backup_progress_{node}"
        self._attr_icon = "mdi:backup-restore"
        self._attr_native_unit_of_measurement = "%"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
            "name": f"1. Node: {self._node}",
        }

    def _get_backup_tasks(self):
        data = self.coordinator.data
        backup_tasks = []

        if "tasks" in data:
            for task in data["tasks"]:
                if (
                    task.get("type") in ["vzdump", "backup"]
                    and task.get("node") == self._node
                ):
                    backup_tasks.append(
                        {
                            "id": task.get("id", task.get("upid", "unknown")),
                            "vmid": task.get("id", "unknown"),
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

    @property
    def native_value(self):
        backup_tasks = self._get_backup_tasks()

        if not backup_tasks:
            return 0

        from time import time

        current_time = time()
        recent_tasks = [
            t for t in backup_tasks if t.get("starttime", 0) > (current_time - 86400)
        ]

        if not recent_tasks:
            return 0

        completed = len([t for t in recent_tasks if t.get("status") == "OK"])
        total = len(recent_tasks)

        return round((completed / total) * 100, 1) if total > 0 else 0

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

        return {
            "node": self._node,
            "total_backups_last_24h": len(recent_tasks),
            "running": len(running_tasks),
            "completed": len(completed_tasks),
            "failed": len(failed_tasks),
            "other": len(other_tasks),
            "percentage": self.native_value,
            "last_update": self.coordinator.data.get("last_update", "unknown"),
            "current_task": (
                {
                    "vmid": current_task.get("vmid") if current_task else None,
                    "user": current_task.get("user") if current_task else None,
                    "starttime": (
                        current_task.get("starttime") if current_task else None
                    ),
                    "upid": current_task.get("upid") if current_task else None,
                }
                if current_task
                else None
            ),
            "recent_backups": recent_backups_list,
            "all_backups_count": len(backup_tasks),
        }

    @property
    def state_class(self):
        return SensorStateClass.MEASUREMENT

    @property
    def suggested_display_precision(self):
        return 1
