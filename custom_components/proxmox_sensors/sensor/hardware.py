from .base import ProxmoxBaseSensor
from ..const import DOMAIN

class ProxmoxHardwareSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, sensor_id, node, sensor_name=None):

        # Friendly name detection
        friendly = self._friendly_name(sensor_id)

        name = f"{friendly} ({node})"
        clean_id = sensor_id.lower().replace(" ", "_")
        unique_id = f"proxmox_hw_{node}_{clean_id}"

        super().__init__(coordinator, sensor_id, name, "°C", unique_id, node)

        self._sensor_id = sensor_id

        # ------------ICON ASSIGNMENT--------------------

        sid = sensor_id.lower()

        if "coretemp" in sid or "package id" in sid:
            self._attr_icon = "mdi:thermometer-lines"

        elif "pch" in sid:
            self._attr_icon = "mdi:thermometer-lines"

        elif "nvme" in sid:
            self._attr_icon = "mdi:harddisk"

        elif "drivetemp" in sid or "scsi" in sid:
            self._attr_icon = "mdi:harddisk"

        else:
            self._attr_icon = "mdi:thermometer-lines"

        # Device class and state class
        self._attr_device_class = "temperature"
        self._attr_state_class = "measurement"

    # =============FRIENDLY NAME======================

    def _friendly_name(self, sensor_id: str) -> str:
        sid = sensor_id.lower()

        # CPU sensors (Intel coretemp)
        if "coretemp" in sid or "package id" in sid:
            return "CPU – Processor Temperature"

        # Intel PCH chipset
        if "pch" in sid:
            return "Intel PCH – Chipset Temperature"

        # NVMe SSD
        if "nvme" in sid:
            return "NVMe SSD – Temperature"

        # SATA / SAS / USB drives
        if "drivetemp" in sid or "scsi" in sid:
            return "SATA Drive – Temperature"

        return sensor_id.replace("_", " ").title()



    def is_valid(self) -> bool:
        val = self._get_value()
        return val is not None

    @property
    def available(self) -> bool:
        val = self._get_value()
        return val is not None and super().available

    @property
    def native_value(self):
        return self._get_value()

    def _get_value(self):
        value = self.coordinator.data.get("hardware", {}).get(self._sensor_id)

        # dict (lm-sensors grouped)
        if isinstance(value, dict):
            temp = value.get("temp1_input")
            try:
                f_val = float(temp)
                return f_val if f_val != 0 else None
            except (ValueError, TypeError):
                return None

        # direct invalid values
        if value in ("N/A", "Desconocido", "unknown", "Unknown", "", None):
            return None

        # numeric conversion
        try:
            f_val = float(value)
            if f_val <= -50 or f_val >= 150:
                return None
            return f_val
        except (ValueError, TypeError):
            return None

    @property
    def extra_state_attributes(self):
        value = self.coordinator.data.get("hardware", {}).get(self._sensor_id)
        if isinstance(value, dict):
            return {
                k: v for k, v in value.items()
                if k != "temp1_input" and v not in (None, "N/A", "")
            }
        return {}
