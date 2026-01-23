from homeassistant.const import PERCENTAGE, UnitOfInformation
from ..const import DOMAIN
from .base import ProxmoxPbsBaseSensor

# ============================================================
#  PBS SERVER SENSORS (NODE-LEVEL)
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


class ProxmoxPBSCpuSensor(ProxmoxPbsBaseSensor):
    """CPU usage of the PBS node."""
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
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }


class ProxmoxPBSRamSensor(ProxmoxPbsBaseSensor):
    """PBS node RAM usage."""
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
            "identifiers": {(DOMAIN, f"pbs_server_{self._server_id}")},
            "name": f"PBS Server {self._server_id}",
            "manufacturer": "Proxmox",
            "model": "Backup Server",
        }

# ============================================================
#  PBS TASK SENSORS (GLOBAL TASKS)
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
        tasks = self.coordinator.data.get("pbs_tasks", [])

        if not isinstance(tasks, list) or not tasks:
            return "No data"

        task = tasks[0]  # Last task
        worker = task.get("worker_type", "Task")
        status = task.get("status") or task.get("msg") or "OK"

        return f"{worker}: {status}"

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
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return None

        task = tasks[0]
        return task.get("worker_type")

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
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return None

        task = tasks[0]
        status = task.get("status")
        if status:
            return status

        msg = task.get("msg", "").lower()
        if "ok" in msg:
            return "OK"
        if "error" in msg:
            return "Error"

        return None

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
        tasks = self.coordinator.data.get("pbs_tasks", [])
        if not isinstance(tasks, list) or not tasks:
            return "OK"

        task = tasks[0]
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
            "identifiers": {(DOMAIN, f"pbs_tasks_{self._server_id}")},
            "name": f"PBS Tasks ({self._server_id})",
            "manufacturer": "Proxmox",
            "model": "Backup Server Tasks",
        }
# ============================================================
#  PBS DATASTORE SENSORS
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

        # Icono manual tiene prioridad
        if icon:
            self._attr_icon = icon
        else:
            # Iconos automáticos según el tipo de dato
            if key == "total":
                self._attr_icon = "mdi:database"
            elif key == "used":
                self._attr_icon = "mdi:database-arrow-up"
            elif key == "free":
                self._attr_icon = "mdi:database-arrow-down"
            else:
                # Fallback elegante
                self._attr_icon = "mdi:database-outline"

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
    """Status of the last backup with dynamic icons and state mapping."""
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

        # 1. Try to read verification info from snapshot
        ver = last.get("verification")
        if ver:
            state = ver.get("state")
            if state == "ok":
                return "Verified OK"
            if state == "failed":
                return "Verification Failed"
            return str(state).capitalize()

        # 2. Check PBS tasks for verification
        tasks = self.coordinator.data.get("pbs_tasks", [])
        task = tasks[0] if isinstance(tasks, list) and tasks else {}

        if task.get("worker_type") == "verify":
            msg = task.get("msg", "").lower()
            status = task.get("status", "").lower()

            if last.get("backup-id") in task.get("upid", ""):
                if "ok" in msg or status == "ok":
                    return "Verified OK"
                if "error" in msg or status == "error":
                    return "Verification Failed"

        # 3. No verification found
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


class ProxmoxPBSBackupsListSensor(ProxmoxPbsBaseSensor):
    """Displays the total count and a summary of the latest backups per resource."""
    def __init__(self, coordinator, server_id, store):
        name = "Backups Summary"
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_backups_summary",
            name=name
        )
        self._store = store
        self._attr_icon = "mdi:archive-clock-outline"

    def _get_value(self):
        data = self.coordinator.data.get("pbs_datastores", {}).get(self._store, {})
        backups = data.get("backups", [])
        return len(backups)

    @property
    def extra_state_attributes(self):
        from datetime import datetime
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
                    dt_str = datetime.fromtimestamp(b_time).strftime('%d/%m/%Y %H:%M')
                    summary[key] = {
                        "raw_time": b_time,
                        "last_backup": dt_str
                    }

        final_list = {k: v["last_backup"] for k, v in sorted(summary.items())}

        return {
            "last_backups_per_resource": final_list,
            "total_snapshots": len(backups),
            "datastore_name": self._store
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"pbs_datastore_{self._server_id}_{self._store}")},
            "name": f"PBS Datastore: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Datastore",
        }

# ============================================================
#  PBS MAINTENANCE SENSORS (GC PER DATASTORE)
# ============================================================

class ProxmoxPBSMaintenanceSensor(ProxmoxPbsBaseSensor):
    """Garbage Collection status and Datastore maintenance."""
    def __init__(self, coordinator, server_id, store):
        super().__init__(
            coordinator=coordinator,
            server_id=server_id,
            sensor_id=f"{store}_gc_status",
            name="GC Status"
        )
        self._store = store
        self._attr_icon = "mdi:recycle-variant"

    def _get_value(self):
        """Determine the Garbage Collection status for the datastore."""
        data = self.coordinator.data.get("pbs_gc", {}).get(self._store, {})

        last_run = data.get("last-run")
        pending = data.get("pending-bytes", 0)
        removed = data.get("removed-bytes", 0)
        processed = data.get("processed-bytes", 0)

        # No GC data at all
        if not any([last_run, pending, removed, processed]):
            return "No Data"

        # GC running (task-level)
        tasks = self.coordinator.data.get("pbs_tasks", [])
        task = tasks[0] if isinstance(tasks, list) and tasks else {}

        if task.get("worker_type") == "garbage_collection" and not task.get("endtime"):
            return "Running"

        # Pending removals
        if pending > 0:
            return "Pending"

        # Removed something
        if removed > 0:
            return "Cleaned"

        # Completed GC
        if last_run:
            return "OK"

        return "At Rest"

    @property
    def extra_state_attributes(self):
        """GC details in GB + last run timestamp."""
        from datetime import datetime
        data = self.coordinator.data.get("pbs_gc", {}).get(self._store, {})

        attrs = {}

        last_run = data.get("last-run")
        if last_run:
            try:
                attrs["last_run"] = datetime.fromtimestamp(last_run).strftime('%d/%m/%Y %H:%M')
            except Exception:
                attrs["last_run"] = "Error format"

        for key, attr_name in [
            ("removed-bytes", "removed_gb"),
            ("pending-bytes", "pending_gb"),
            ("processed-bytes", "processed_gb")
        ]:
            val = data.get(key, 0)
            attrs[attr_name] = round(float(val) / (1024**3), 2) if val else 0.0

        return attrs

    @property
    def device_info(self):
        """Maintenance group for this datastore."""
        return {
            "identifiers": {(DOMAIN, f"pbs_maintenance_{self._server_id}_{self._store}")},
            "name": f"PBS Maintenance: {self._store}",
            "manufacturer": "Proxmox",
            "model": "Backup Server Maintenance",
        }

# ============================================================
#  END OF PBS SENSOR DEFINITIONS
# ============================================================

# Nota:
# Este archivo ha sido reorganizado siguiendo la arquitectura premium:
#
#   • PBS Server (estado del nodo)
#   • PBS Tasks (tareas globales)
#   • PBS Datastore (almacenamiento)
#   • PBS Maintenance (mantenimiento por datastore)
#
# Cada sensor tiene su propio device_info para que Home Assistant
# agrupe las entidades correctamente en dispositivos separados.
#
# Si añades nuevos sensores en el futuro, sigue esta estructura:
#
#   - Sensores del nodo → pbs_server_<id>
#   - Sensores de tareas → pbs_tasks_<id>
#   - Sensores del datastore → pbs_datastore_<id>_<store>
#   - Sensores de mantenimiento → pbs_maintenance_<id>_<store>
#
# Esto garantiza claridad, escalabilidad y una experiencia premium.
