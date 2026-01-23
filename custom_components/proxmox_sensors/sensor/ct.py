"""Container (LXC) sensors for Proxmox."""
from .base import ProxmoxBaseSensor
from ..const import DOMAIN


class ProxmoxContainerSensor(ProxmoxBaseSensor):
    """Main status sensor for LXC Containers."""

    def __init__(self, coordinator, ct_id, node, label):
        """Initialize the container status sensor."""
        name = "Status"
        uid = f"proxmox_ct_{node}_{ct_id}_status_v4"
        self._label = label
        super().__init__(coordinator, ct_id, name, None, uid, node)
        self._attr_icon = "mdi:label-outline"

    @property
    def device_info(self):
        """Define the container device linked to the Proxmox Node."""
        node_id = self._node.lower()
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._sensor_id}_v4")},
            "name": f"3. CT: {self._label}",
            "via_device": (DOMAIN, f"proxmox_node_{node_id}"),
            "manufacturer": "Proxmox",
            "model": "LXC Container",
        }

    def _get_value(self):
        """Return the current status of the container."""
        ct_data = self.coordinator.data.get("cts", {}).get(self._sensor_id, {})
        return str(ct_data.get("status", "unknown")).capitalize()


class ProxmoxContainerAttributeSensor(ProxmoxBaseSensor):
    """Attribute sensors for LXC (CPU, RAM, Disk, Uptime, Network)."""

    def __init__(self, coordinator, ct_id, node, label, attr_name, unit, icon):
        """Initialize the container attribute sensor."""
        display_name = attr_name.replace("_", " ").title()
        uid = f"proxmox_ct_{node}_{ct_id}_{attr_name}_v4"

        self._label = label
        self._attr_key = attr_name

        super().__init__(coordinator, ct_id, display_name, unit, uid, node)
        self._attr_icon = icon

    @property
    def device_info(self):
        """Link attributes to the same container device."""
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._sensor_id}_v4")},
            "name": f"3. CT: {self._label}",
        }

    def _get_value(self):
        """Calculate and return the attribute value."""
        ct_data = self.coordinator.data.get("cts", {}).get(self._sensor_id, {})
        if not ct_data:
            return None

        try:
            # CPU Usage percentage calculation
            if self._attr_key == "cpu_usage":
                val = ct_data.get("cpu")
                return round(float(val) * 100, 2) if val is not None else None

            # Network RX/TX (convert bytes → MB)
            if self._attr_key == "network_rx":
                val = ct_data.get("netin")
                return round(float(val) / (1024**2), 2) if val is not None else None

            if self._attr_key == "network_tx":
                val = ct_data.get("netout")
                return round(float(val) / (1024**2), 2) if val is not None else None

            # Proxmox API key mapping
            keys = {
                "memory_used": "mem",
                "memory_total": "maxmem",
                "disk_used": "disk",
                "disk_total": "maxdisk",
                "uptime": "uptime",
            }

            api_key = keys.get(self._attr_key)
            val = ct_data.get(api_key)
            if val is None:
                return None

            # Uptime conversion from seconds to hours
            if self._attr_key == "uptime":
                return round(float(val) / 3600, 1)

            # Storage/Memory conversion from Bytes to GB
            return round(float(val) / (1024**3), 2)

        except (ValueError, TypeError):
            return None
