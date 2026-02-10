from datetime import datetime
import logging

from homeassistant.const import PERCENTAGE, UnitOfInformation
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity

from ..const import DOMAIN
from .base import ProxmoxPbsBaseSensor

_LOGGER = logging.getLogger(__name__)


class ProxmoxPBSVersionSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="version",
            name="Version",
        )
        self._attr_icon = "mdi:information-outline"

    def _get_value(self):
        return self.coordinator.data.get("pbs_version", "Unknown")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "name": "Server",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSReleaseSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="release",
            name="Release",
        )
        self._attr_icon = "mdi:tag"

    def _get_value(self):
        return self.coordinator.data.get("pbs_release", "Unknown")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "name": "Server",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSAuthStatusSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="auth_status",
            name="Auth Status",
        )
        self._attr_icon = "mdi:shield-check"

    def _get_value(self):
        return self.coordinator.data.get("pbs_auth_status", "UNKNOWN")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "name": "Server",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSCpuSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(coordinator, server_id, "node_cpu", "CPU Usage", "%")
        self._attr_icon = "mdi:cpu-64-bit"

    def _get_value(self):
        status = self.coordinator.data.get("pbs_node_status", {})
        cpu = status.get("cpu")
        return round(cpu * 100, 2) if cpu is not None else 0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "name": "Server",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSRamSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(coordinator, server_id, "node_ram", "RAM Usage", "%")
        self._attr_icon = "mdi:memory"

    def _get_value(self):
        status = self.coordinator.data.get("pbs_node_status", {})
        memory = status.get("memory", {})
        total = memory.get("total")
        used = memory.get("used")
        if total and used:
            return round((used / total) * 100, 2)
        return 0

    @property
    def extra_state_attributes(self):
        status = self.coordinator.data.get("pbs_node_status", {})
        memory = status.get("memory", {})
        return {
            "total_gb": round(memory.get("total", 0) / (1024**3), 2),
            "used_gb": round(memory.get("used", 0) / (1024**3), 2),
            "free_gb": round(memory.get("free", 0) / (1024**3), 2),
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "name": "Server",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSRamTotalSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id):
        super().__init__(coordinator)
        self._server_id = server_id
        self._attr_name = "RAM Total"
        self._attr_unique_id = f"pbs_ram_total_{server_id}"
        self._attr_icon = "mdi:memory"
        self._attr_native_unit_of_measurement = "GB"

    @property
    def native_value(self):
        ram = self.coordinator.data.get("pbs_node_status", {}).get("memory", {})
        return round(ram.get("total", 0) / (1024**3), 2)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Backup Server",
            "name": "PBS Server",
        }


class ProxmoxPBSRamUsedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id):
        super().__init__(coordinator)
        self._server_id = server_id
        self._attr_name = "RAM Used"
        self._attr_unique_id = f"pbs_ram_used_{server_id}"
        self._attr_icon = "mdi:memory"
        self._attr_native_unit_of_measurement = "GB"

    @property
    def native_value(self):
        ram = self.coordinator.data.get("pbs_node_status", {}).get("memory", {})
        return round(ram.get("used", 0) / (1024**3), 2)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Backup Server",
            "name": "PBS Server",
        }


class ProxmoxPBSRamFreeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id):
        super().__init__(coordinator)
        self._server_id = server_id
        self._attr_name = "RAM Free"
        self._attr_unique_id = f"pbs_ram_free_{server_id}"
        self._attr_icon = "mdi:memory"
        self._attr_native_unit_of_measurement = "GB"

    @property
    def native_value(self):
        ram = self.coordinator.data.get("pbs_node_status", {}).get("memory", {})
        return round(ram.get("free", 0) / (1024**3), 2)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "server")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Backup Server",
            "name": "PBS Server",
        }


class ProxmoxPBSTaskSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task",
            name="Last Task",
        )
        self._attr_icon = "mdi:clipboard-list"

    def _get_value(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return "No data"

        task = tasks[0]
        worker = task.get("worker_type", "Task")
        status = task.get("status") or task.get("msg") or "OK"
        return f"{worker}: {status}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tasks")},
            "name": "Tasks",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskTypeSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_type",
            name="Last Task Type",
        )
        self._attr_icon = "mdi:clipboard-text"

    def _get_value(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return None
        task = tasks[0]
        return task.get("worker_type")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tasks")},
            "name": "Tasks",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskStatusSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_status",
            name="Last Task Status",
        )
        self._attr_icon = "mdi:information"

    def _get_value(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return "OK"

        task = tasks[0]
        status = task.get("status")
        if status:
            return status

        msg = task.get("msg", "").lower()
        if "ok" in msg:
            return "OK"
        if "error" in msg:
            return "Error"

        return "OK"

    @property
    def extra_state_attributes(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return {}

        task = tasks[0]

        def format_ts(ts):
            if ts and isinstance(ts, (int, float)):
                return datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M:%S")
            return ts

        return {
            "task_type": task.get("worker_type"),
            "vmid": task.get("worker_id"),
            "node": task.get("node", "server"),
            "upid": task.get("upid"),
            "start_time": format_ts(task.get("starttime")),
            "end_time": format_ts(task.get("endtime")),
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tasks")},
            "name": "Tasks",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskMessageSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_message",
            name="Last Task Message",
        )
        self._attr_icon = "mdi:message-text-outline"

    def _get_value(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return "OK"
        task = tasks[0]
        msg = task.get("msg")
        return msg if msg else "OK"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tasks")},
            "name": "Tasks",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskDurationSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_duration",
            name="Last Task Duration",
            unit="s",
        )
        self._attr_icon = "mdi:timer-outline"

    def _get_value(self):
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return 0

        task = tasks[0]
        start = task.get("starttime")
        end = task.get("endtime")

        if start and end:
            return int(end - start)

        if start and not end:
            import time

            return int(time.time() - start)

        return 0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tasks")},
            "name": "Tasks",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSDatastoreUsageSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_usage",
            name="Usage",
            unit=PERCENTAGE,
        )
        self._store = store
        self._attr_icon = "mdi:database-clock"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        used = data.get("used", 0)
        total = data.get("total", 0)
        return round((used / total) * 100, 2) if total > 0 else 0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSDatastoreSizeSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store, key, label, icon=None):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_{key}",
            name=label,
            unit=UnitOfInformation.GIGABYTES,
        )
        self._store = store
        self._key = key

        if icon:
            self._attr_icon = icon
        else:
            icons = {
                "total": "mdi:database",
                "used": "mdi:database-arrow-up",
                "free": "mdi:database-arrow-down",
            }
            self._attr_icon = icons.get(key, "mdi:database-outline")

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return round(data.get(self._key, 0) / (1024**3), 2)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSDedupSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_dedup",
            name="Deduplication",
            unit="x",
        )
        self._store = store
        self._attr_icon = "mdi:clippy"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        idx = data.get("index-data-bytes", 0)
        disk = data.get("disk-bytes", 0)
        return round(idx / disk, 2) if disk > 0 else 1.0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSBackupCountSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_backup_count",
            name="Backup Count",
        )
        self._store = store
        self._attr_icon = "mdi:counter"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return data.get("backup_count", 0)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSLastBackupTimeSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_last_backup_time",
            name="Last Backup Time",
        )
        self._store = store
        self._attr_icon = "mdi:clock-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        last = data.get("last_backup")
        if not last:
            return None
        ts = last.get("backup-time")
        if not ts:
            return None
        return datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M:%S")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSLastBackupSizeSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_last_backup_size",
            name="Last Backup Size",
            unit=UnitOfInformation.GIGABYTES,
        )
        self._store = store
        self._attr_icon = "mdi:database"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        last = data.get("last_backup")
        size = last.get("size") if last else 0
        return round(size / (1024**3), 2)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSLastBackupStatusSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_last_backup_status",
            name="Last Backup Status",
        )
        self._store = store
        self._attr_icon = "mdi:check-circle-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        last = data.get("last_backup")

        if not last:
            return "No backups"

        ver = last.get("verification")
        if ver:
            state = ver.get("state")
            if state == "ok":
                return "Verified OK"
            if state == "failed":
                return "Verification Failed"
            return str(state).capitalize()

        return "Finished (Not Verified)"

    @property
    def icon(self):
        status = self.native_value
        if status == "Verified OK":
            return "mdi:check-decagram"
        if status == "Verification Failed":
            return "mdi:alert-decagram"
        if status == "No backups":
            return "mdi:database-off"
        return "mdi:check-circle-outline"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSBackupErrorsSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_backup_errors",
            name="Backup Errors",
        )
        self._store = store
        self._attr_icon = "mdi:alert-circle-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return len(data.get("backup_errors", []))

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSBackupsListSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_backups_summary",
            name="Backups Summary",
        )
        self._store = store
        self._attr_icon = "mdi:archive-clock-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return len(data.get("backups", []))

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        backups = data.get("backups", [])

        summary = {}
        for b in backups:
            b_type = b.get("backup-type")
            b_id = b.get("backup-id")
            b_time = b.get("backup-time")
            if b_type and b_id and b_time:
                key = f"{b_type}/{b_id}"
                if key not in summary or b_time > summary[key]["raw_time"]:
                    summary[key] = {
                        "raw_time": b_time,
                        "last_backup": datetime.fromtimestamp(b_time).strftime(
                            "%d/%m/%Y %H:%M:%S"
                        ),
                    }

        return {
            "last_backups_per_resource": {
                k: v["last_backup"] for k, v in sorted(summary.items())
            },
            "total_snapshots": len(backups),
            "datastore_name": self._store,
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"datastore_{self._store}")},
            "name": f"Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSMaintenanceSensor(ProxmoxPbsBaseSensor):
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_gc_status",
            name="GC Status",
        )
        self._store = store
        self._attr_icon = "mdi:recycle-variant"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_gc", {}).get(self._store, {})
        last_run, pending, removed, processed = (
            data.get("last-run"),
            data.get("pending-bytes", 0),
            data.get("removed-bytes", 0),
            data.get("processed-bytes", 0),
        )

        if not any([last_run, pending, removed, processed]):
            return "No Data"

        tasks = self.coordinator.data.get("pbs_tasks", [])
        task = tasks[0] if isinstance(tasks, list) and tasks else {}
        if task.get("worker_type") == "garbage_collection" and not task.get("endtime"):
            return "Running"
        if pending > 0:
            return "Pending"
        if removed > 0:
            return "Cleaned"

        return "OK" if last_run else "At Rest"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get("pbs_gc", {}).get(self._store, {})
        attrs = {}

        last_run = data.get("last-run")
        if last_run:
            attrs["last_run"] = datetime.fromtimestamp(last_run).strftime(
                "%d/%m/%Y %H:%M:%S"
            )

        for key, attr_name in [
            ("removed-bytes", "removed_gb"),
            ("pending-bytes", "pending_gb"),
            ("processed-bytes", "processed_gb"),
        ]:
            val = data.get(key, 0)
            attrs[attr_name] = round(float(val) / (1024**3), 2) if val else 0.0

        return attrs

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"maintenance_{self._store}")},
            "name": f"Maintenance: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Maintenance",
        }
