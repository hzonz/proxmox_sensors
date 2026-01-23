"""Node sensors for Proxmox (CPU, Memory, Tasks, and System)."""
from .base import ProxmoxBaseSensor
from ..const import DOMAIN

# ---------------------------------------------------------
# NODE GENERIC SENSOR (CPU %, WAIT, UPTIME)
# ---------------------------------------------------------
class ProxmoxNodeSensor(ProxmoxBaseSensor):
    """General node sensors (CPU, Load, Uptime, etc.)."""
    
    def __init__(self, coordinator, sensor_id, node):
        """Initialize the node generic sensor."""
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
        """Parse and return the sensor value based on the sensor type."""
        value = self.coordinator.data.get("node", {}).get(self._sensor_id)
        
        # Extract version number from PVE version string (e.g., pve-manager/7.4-3/...)
        if self._sensor_id == "pveversion" and isinstance(value, str):
            parts = value.split("/")
            if len(parts) >= 2:
                return parts[1]

        # Convert 0.0-1.0 range to percentage
        if self._sensor_id in ["cpu", "wait"] and isinstance(value, (int, float)):
            return round(value * 100, 2)
            
        # Format uptime seconds into a human-readable string
        if self._sensor_id == "uptime" and isinstance(value, (int, float)):
            days = int(value // 86400)
            hours = int((value % 86400) // 3600)
            minutes = int((value % 3600) // 60)
            return f"{days}d {hours}h {minutes}m"
            
        # Handle complex objects (like kversion dicts)
        if isinstance(value, dict):
            return value.get("release") or value.get("version", "").split("\n")[0] or None
            
        # Clean up multiline strings
        if isinstance(value, str):
            return value.split("\n")[0]
            
        return value

# ---------------------------------------------------------
# CLUSTER TASKS MONITOR
# ---------------------------------------------------------
class ProxmoxClusterTasksSensor(ProxmoxBaseSensor):
    """Monitor for the last executed task on the node."""
    
    def __init__(self, coordinator, node):
        """Initialize the task sensor."""
        uid = f"proxmox_{node}_cluster_tasks_v3"
        super().__init__(coordinator, "last_task", "Last Task", None, uid, node)

    def _get_value(self):
        """Return a summary of the last task."""
        task = self.coordinator.data.get("node", {}).get("last_task")
        if not task:
            return "No Tasks"
        return f"{task.get('type', 'unknown')}: {task.get('status', 'unknown')}"

    @property
    def extra_state_attributes(self):
        """Return recent task errors and details as attributes."""
        task = self.coordinator.data.get("node", {}).get("last_task", {})
        tasks_list = self.coordinator.data.get("tasks", [])
        
        # Filter and format recent errors (tasks where status is not OK)
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
    """Sensor for CPU hardware model or core count."""
    
    def __init__(self, coordinator, node):
        """Initialize the CPU info sensor."""
        super().__init__(coordinator, "cpuinfo", "CPU Info", None, f"p_node_cpu_{node}_v3", node)
        self._attr_icon = "mdi:cpu-64-bit"

    def _get_value(self):
        """Return CPU model or cores summary."""
        info = self.coordinator.data.get("node", {}).get("cpuinfo", {})
        return info.get("model") or f"{info.get('cores', '?')} cores"

class ProxmoxKSMSensor(ProxmoxBaseSensor):
    """Sensor for Kernel Samepage Merging (KSM) shared memory."""
    
    def __init__(self, coordinator, node):
        """Initialize the KSM sensor."""
        super().__init__(coordinator, "ksm", "KSM Shared", "GB", f"p_node_ksm_{node}_v3", node)
        self._attr_icon = "mdi:memory-arrow-down"

    def _get_value(self):
        """Convert shared memory bytes to Gigabytes."""
        val = self.coordinator.data.get("node", {}).get("ksm", {}).get("shared", 0)
        return round(val / (1024**3), 2)

class ProxmoxMemorySensor(ProxmoxBaseSensor):
    """Sensor for RAM usage percentage."""
    
    def __init__(self, coordinator, node):
        """Initialize the RAM usage sensor."""
        super().__init__(coordinator, "memory", "Memory Usage", "%", f"p_node_mem_{node}_v3", node)
        self._attr_icon = "mdi:memory"

    def _get_value(self):
        """Calculate memory usage percentage."""
        data = self.coordinator.data.get("node", {}).get("memory", {})
        used = data.get("used", 0)
        total = data.get("total", 1)
        return round((used / total) * 100, 2)

class ProxmoxSwapSensor(ProxmoxBaseSensor):
    """Sensor for Swap usage percentage."""
    
    def __init__(self, coordinator, node):
        """Initialize the Swap usage sensor."""
        super().__init__(coordinator, "swap", "Swap Usage", "%", f"p_node_swap_{node}_v3", node)
        self._attr_icon = "mdi:swap-horizontal"

    def _get_value(self):
        """Calculate swap usage percentage."""
        data = self.coordinator.data.get("node", {}).get("swap", {})
        total = data.get("total", 0)
        if total == 0:
            return 0
        return round((data.get("used", 0) / total) * 100, 2)

class ProxmoxRootFSSensor(ProxmoxBaseSensor):
    """Sensor for Root File System (/) usage percentage."""
    
    def __init__(self, coordinator, node):
        """Initialize the Root FS sensor."""
        super().__init__(coordinator, "rootfs", "Root FS Usage", "%", f"p_node_rootfs_{node}_v3", node)
        self._attr_icon = "mdi:folder"

    def _get_value(self):
        """Calculate Root FS usage percentage."""
        data = self.coordinator.data.get("node", {}).get("rootfs", {})
        total = data.get("total", 1)
        return round((data.get("used", 0) / total) * 100, 2)