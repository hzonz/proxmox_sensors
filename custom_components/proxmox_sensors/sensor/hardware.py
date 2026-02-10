from .base import ProxmoxBaseSensor
from ..const import DOMAIN


class ProxmoxHardwareSensor(ProxmoxBaseSensor):
    def __init__(self, coordinator, sensor_id, node, sensor_name=None):

        # Friendly name detection
        friendly = self._friendly_name(sensor_id)

        name = f"{friendly} ({node})"
        clean_id = sensor_id.lower().replace(" ", "_").replace("-", "_")
        unique_id = f"proxmox_hw_{node}_{clean_id}"

        super().__init__(coordinator, sensor_id, name, "°C", unique_id, node)

        self._sensor_id = sensor_id

        # ------------ICON ASSIGNMENT--------------------
        sid = sensor_id.lower()

        if any(
            x in sid
            for x in ["coretemp", "package id", "k10temp", "tctl", "tdie", "cpu"]
        ):
            self._attr_icon = "mdi:thermometer-lines"

        elif "pch" in sid:
            self._attr_icon = "mdi:thermometer-lines"

        elif any(x in sid for x in ["nvme", "composite"]):
            self._attr_icon = "mdi:harddisk-plus"

        elif any(x in sid for x in ["drivetemp", "scsi", "sda", "sdb", "sdc"]):
            self._attr_icon = "mdi:harddisk"

        else:
            self._attr_icon = "mdi:thermometer-lines"

        # Device class and state class
        self._attr_device_class = "temperature"
        self._attr_state_class = "measurement"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "name": f"1. Node: {self._node}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
        }

    # ===========FRIENDLY NAME IMPROVED=============

    def _friendly_name(self, sensor_id: str) -> str:
        sid = sensor_id.lower()

        # 1. CPU: Intel coretemp & AMD k10temp
        if any(x in sid for x in ["coretemp", "package id", "k10temp", "tctl", "tdie"]):
            if "core" in sid:
                core_part = sid.split("core")[-1].replace("_", " ").strip()
                return f"CPU – Core {core_part} Temp"
            if "package" in sid:
                return "CPU – Package Temperature"
            return "CPU – Processor Temperature"

        # 2. Intel PCH chipset
        if "pch" in sid:
            return "Intel PCH – Chipset Temperature"

        # 3. NVMe SSD
        if any(x in sid for x in ["nvme", "composite"]):
            if "nvme" in sid and "_" in sid:
                bus_id = sid.split("_")[-1]
                return f"NVMe SSD ({bus_id}) – Temperature"
            return "NVMe SSD – Temperature"

        # 4. SATA / DriveTemp
        if any(x in sid for x in ["drivetemp", "scsi", "sda", "sdb", "sdc"]):
            for letter in ["sda", "sdb", "sdc", "sdd", "sde"]:
                if letter in sid:
                    return f"SATA Drive ({letter.upper()}) – Temp"
            return "SATA Drive – Temperature"

        return sensor_id.replace("_", " ").replace("-", " ").title()

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

        # Case 1: Dictionary
        if isinstance(value, dict):
            # Priority 1: Standard temp1_input
            temp = value.get("temp1_input")

            # Priority 2: Dynamic finder (AMD Ryzen or NVMe)
            if temp is None:
                for k, v in value.items():
                    if any(x in k.lower() for x in ["input", "val", "temp", "tdie"]):
                        try:
                            float(v)
                            temp = v
                            break
                        except (ValueError, TypeError):
                            continue

            return self._parse_numeric(temp)

        # Case 2: Direct Value
        return self._parse_numeric(value)

    def _parse_numeric(self, val):
        if val in ("N/A", "Desconocido", "unknown", "Unknown", "", None):
            return None
        try:
            f_val = float(val)
            if 1.0 < f_val < 145.0:
                return f_val
            return None
        except (ValueError, TypeError):
            return None

    @property
    def extra_state_attributes(self):
        value = self.coordinator.data.get("hardware", {}).get(self._sensor_id)
        if isinstance(value, dict):
            return {k: v for k, v in value.items() if v not in (None, "N/A", "")}
        return {}
