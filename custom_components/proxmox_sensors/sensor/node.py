from .base import ProxmoxBaseSensor
from ..const import DOMAIN

# ---------------------------------------------------------
# NODE GENERIC SENSOR (CPU %, WAIT, UPTIME)
# ---------------------------------------------------------
class ProxmoxNodeSensor(ProxmoxBaseSensor):
    """Sensores generales del nodo (CPU, Load, Uptime, etc.)."""
    def __init__(self, coordinator, sensor_id, node):
        unit = None
        icon = "mdi:information-outline"
        state_class = None

        if sensor_id == "cpu":
            friendly_name = "CPU Usage"
            unit = "%"
            icon = "mdi:cpu-64-bit"
            state_class = "measurement"
        elif sensor_id == "wait":
            friendly_name = "CPU I/O Wait"
            unit = "%"
            icon = "mdi:timer-sand"
            state_class = "measurement"
        elif sensor_id == "uptime":
            friendly_name = "Uptime"
            icon = "mdi:clock-outline"
        elif sensor_id == "kversion":
            friendly_name = "Kernel Version"
            icon = "mdi:linux"
        elif sensor_id == "pveversion":
            friendly_name = "PVE Version"
            icon = "mdi:numeric"
        elif sensor_id == "loadavg":
            friendly_name = "Load Average"
            icon = "mdi:chart-line"
        else:
            friendly_name = sensor_id.replace("_", " ").title()

        unique_id = f"proxmox_node_{node}_{sensor_id}_v3"
        super().__init__(coordinator, sensor_id, friendly_name, unit, unique_id, node)

        self._attr_icon = icon
        self._attr_state_class = state_class

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
            return value.get("release") or value.get("version", "").split("\n")[0] or None
        if isinstance(value, str):
            return value.split("\n")[0]
        return value

# ---------------------------------------------------------
# CLUSTER TASKS MONITOR
# ---------------------------------------------------------
class ProxmoxClusterTasksSensor(ProxmoxBaseSensor):
    """Monitor de la última tarea ejecutada en el nodo."""
    def __init__(self, coordinator, node):
        uid = f"proxmox_{node}_cluster_tasks_v3"
        super().__init__(coordinator, "last_task", "Last Task", None, uid, node)

    def _get_value(self):
        task = self.coordinator.data.get("node", {}).get("last_task")
        if not task: return "No Tasks"
        return f"{task.get('type', 'unknown')}: {task.get('status', 'unknown')}"

    @property
    def extra_state_attributes(self):
        task = self.coordinator.data.get("node", {}).get("last_task", {})
        tasks_list = self.coordinator.data.get("tasks", [])
        errors = [f"{t.get('type')}: {t.get('status')}" for t in tasks_list 
                 if t.get("status") and "OK" not in t.get("status")]
        return {
            "user": task.get("user"),
            "status_raw": task.get("status"),
            "recent_errors": errors[:5] if errors else 0
        }

# ---------------------------------------------------------
# CPU INFO, KSM, MEMORY, SWAP & ROOTFS
# ---------------------------------------------------------
class ProxmoxCPUInfoSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(coordinator, "cpuinfo", "CPU Info", None, f"p_node_cpu_{node}_v3", node)
        self._attr_icon = "mdi:cpu-64-bit"

    def _get_value(self):
        info = self.coordinator.data.get("node", {}).get("cpuinfo", {})
        return info.get("model") or f"{info.get('cores', '?')} cores"

class ProxmoxKSMSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(coordinator, "ksm", "KSM Shared", "GB", f"p_node_ksm_{node}_v3", node)
        self._attr_icon = "mdi:memory-arrow-down"

    def _get_value(self):
        val = self.coordinator.data.get("node", {}).get("ksm", {}).get("shared", 0)
        return round(val / (1024**3), 2)

class ProxmoxMemorySensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(coordinator, "memory", "Memory Usage", "%", f"p_node_mem_{node}_v3", node)
        self._attr_icon = "mdi:memory"

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("memory", {})
        used = data.get("used", 0)
        total = data.get("total", 1)
        return round((used / total) * 100, 2)

class ProxmoxSwapSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(coordinator, "swap", "Swap Usage", "%", f"p_node_swap_{node}_v3", node)
        self._attr_icon = "mdi:swap-horizontal"

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("swap", {})
        total = data.get("total", 0)
        if total == 0: return 0
        return round((data.get("used", 0) / total) * 100, 2)

class ProxmoxRootFSSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, node):
        super().__init__(coordinator, "rootfs", "Root FS Usage", "%", f"p_node_rootfs_{node}_v3", node)
        self._attr_icon = "mdi:folder"

    def _get_value(self):
        data = self.coordinator.data.get("node", {}).get("rootfs", {})
        total = data.get("total", 1)
        return round((data.get("used", 0) / total) * 100, 2)