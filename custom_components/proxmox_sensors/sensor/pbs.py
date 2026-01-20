from homeassistant.const import PERCENTAGE, UnitOfInformation
from ..const import DOMAIN
from .base import ProxmoxPbsBaseSensor

# ============================================================
#  DATASTORE SENSORS
# ============================================================

class ProxmoxPBSDatastoreUsageSensor(ProxmoxPbsBaseSensor):
    """Percentage of datastore used."""
    def __init__(self, coordinator, server_id, store):
        name = "Usage"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_usage",
            name=name,
            unit=PERCENTAGE
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
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSDatastoreSizeSensor(ProxmoxPbsBaseSensor):
    """Total / Used / Free size in GB."""
    def __init__(self, coordinator, server_id, store, key, label, icon=None):
        name = label
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_{key}",
            name=name,
            unit=UnitOfInformation.GIGABYTES
        )
        self._store = store
        self._key = key
        if icon:
            self._attr_icon = icon

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return round(data.get(self._key, 0) / (1024**3), 2)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSDedupSensor(ProxmoxPbsBaseSensor):
    """Deduplication factor."""
    def __init__(self, coordinator, server_id, store):
        name = "Deduplication"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_dedup",
            name=name,
            unit="x"
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
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


# ============================================================
#  BACKUP SENSORS
# ============================================================

class ProxmoxPBSBackupCountSensor(ProxmoxPbsBaseSensor):
    """Number of backups in datastore."""
    def __init__(self, coordinator, server_id, store):
        name = "Backup Count"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_backup_count",
            name=name
        )
        self._store = store
        self._attr_icon = "mdi:counter"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return data.get("backup_count", 0)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSLastBackupTimeSensor(ProxmoxPbsBaseSensor):
    """Timestamp of the last backup."""
    def __init__(self, coordinator, server_id, store):
        name = "Last Backup Time"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_last_backup_time",
            name=name
        )
        self._store = store
        self._attr_icon = "mdi:clock-outline"

    def _get_value(self):
        from datetime import datetime
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        last = data.get("last_backup")
        if not last:
            return None
        ts = last.get("backup-time")
        if not ts:
            return None
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSLastBackupSizeSensor(ProxmoxPbsBaseSensor):
    """Size of the last backup."""
    def __init__(self, coordinator, server_id, store):
        name = "Last Backup Size"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_last_backup_size",
            name=name,
            unit=UnitOfInformation.GIGABYTES
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
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSLastBackupStatusSensor(ProxmoxPbsBaseSensor):
    """Status of the last backup."""
    def __init__(self, coordinator, server_id, store):
        name = "Last Backup Status"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_last_backup_status",
            name=name
        )
        self._store = store
        self._attr_icon = "mdi:check-circle-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        last = data.get("last_backup")
        if not last:
            return "No backups"
        ver = last.get("verification", {})
        return ver.get("state", "unknown")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


class ProxmoxPBSBackupErrorsSensor(ProxmoxPbsBaseSensor):
    """Number of failed backups."""
    def __init__(self, coordinator, server_id, store):
        name = "Backup Errors"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_backup_errors",
            name=name
        )
        self._store = store
        self._attr_icon = "mdi:alert-circle-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        return len(data.get("backup_errors", []))

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }


# ============================================================
#  SYSTEM SENSORS
# ============================================================

class ProxmoxPBSVersionSensor(ProxmoxPbsBaseSensor):
    """PBS Version."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="version",
            name="Version"
        )
        self._attr_icon = "mdi:information-outline"

    def _get_value(self):
        return self.coordinator.data.get("pbs_version", "Unknown")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSReleaseSensor(ProxmoxPbsBaseSensor):
    """PBS Release."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="release",
            name="Release"
        )
        self._attr_icon = "mdi:tag"

    def _get_value(self):
        return self.coordinator.data.get("pbs_release", "Unknown")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSAuthStatusSensor(ProxmoxPbsBaseSensor):
    """PBS authentication status."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="auth_status",
            name="Auth Status"
        )
        self._attr_icon = "mdi:shield-check"

    def _get_value(self):
        return self.coordinator.data.get("pbs_auth_status", "UNKNOWN")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


# ============================================================
#  TASK SENSORS
# ============================================================

class ProxmoxPBSTaskSensor(ProxmoxPbsBaseSensor):
    """Last PBS task summary."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task",
            name="Last Task"
        )
        self._attr_icon = "mdi:clipboard-list"

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        if isinstance(task, dict) and task:
            return f"{task.get('worker_type', 'Task')}: {task.get('status', 'OK')}"
        return "No data"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_tasks_{self._server_id}")},
            "name": f"PBS Tasks ({self._server_id})",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskTypeSensor(ProxmoxPbsBaseSensor):
    """Type of the last PBS task."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_type",
            name="Last Task Type"
        )
        self._attr_icon = "mdi:clipboard-text"

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        return task.get("worker_type") if isinstance(task, dict) else None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_tasks_{self._server_id}")},
            "name": f"PBS Tasks ({self._server_id})",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskStatusSensor(ProxmoxPbsBaseSensor):
    """Status of the last PBS task."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_status",
            name="Last Task Status"
        )
        self._attr_icon = "mdi:information"

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        return task.get("status") if isinstance(task, dict) else None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_tasks_{self._server_id}")},
            "name": f"PBS Tasks ({self._server_id})",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskMessageSensor(ProxmoxPbsBaseSensor):
    """Message of the last PBS task."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_message",
            name="Last Task Message"
        )
        self._attr_icon = "mdi:message-text-outline"

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        if not isinstance(task, dict):
            return "OK"
        msg = task.get("msg")
        return msg if msg else "OK"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_tasks_{self._server_id}")},
            "name": f"PBS Tasks ({self._server_id})",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }


class ProxmoxPBSTaskDurationSensor(ProxmoxPbsBaseSensor):
    """Duration of the last PBS task."""
    def __init__(self, coordinator, server_id):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id="last_task_duration",
            name="Last Task Duration",
            unit="s"
        )
        self._attr_icon = "mdi:timer-outline"

    def _get_value(self):
        task = self.coordinator.data.get("pbs_tasks")
        duration = task.get("duration") if isinstance(task, dict) else None
        return duration if duration else 0

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_tasks_{self._server_id}")},
            "name": f"PBS Tasks ({self._server_id})",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }
