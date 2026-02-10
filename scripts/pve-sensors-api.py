#!/usr/bin/env python3
import json
import subprocess
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/sensors":
            self._handle_sensors()
        elif self.path == "/smart":
            self._handle_smart()
        elif self.path == "/smart-extended":
            self._handle_smart_extended()
        elif self.path == "/health":
            self._handle_health()
        else:
            self.send_response(404)
            self.end_headers()

    def _handle_sensors(self):
        """Handle lm-sensors data."""
        try:
            data = subprocess.check_output(["sensors", "-j"], timeout=5)
            self._send_json_response(data)
        except Exception as e:
            self._send_error_response(f"Error getting sensors: {e}")

    def _handle_smart(self):
        """Handle SMART data - optimized version."""
        try:
            smart_data = self._get_smart_data_fast()
            self._send_json_response(json.dumps(smart_data))
        except Exception as e:
            self._send_error_response(f"Error getting SMART data: {e}")

    def _handle_smart_extended(self):
        """Extended SMART data with more details."""
        try:
            smart_data = self._get_smart_data_extended()
            self._send_json_response(json.dumps(smart_data))
        except Exception as e:
            self._send_error_response(f"Error: {e}")

    def _handle_health(self):
        """Return health status."""
        try:
            # Obtain basic data
            sensors_ok = self._check_sensors()
            smart_ok = self._check_smartctl()
            disks = self._get_disk_health_summary()
            
            health_data = {
                "status": "healthy" if sensors_ok and smart_ok else "degraded",
                "sensors": sensors_ok,
                "smartctl": smart_ok,
                "disks_working": disks["working"],
                "disks_failed": disks["failed"],
                "disks_total": disks["total"],
                "timestamp": subprocess.check_output(["date", "+%s"]).decode().strip()
            }
            self._send_json_response(json.dumps(health_data))
        except Exception as e:
            self._send_error_response(f"Error: {e}")

    def _get_smart_data_fast(self):
        """Universal SMART data collection for all disks."""
        smart_data = {}
        
        try:
            # 1. Use smartctl --scan-open for available disks
            scan_cmd = ["smartctl", "--scan-open"]
            result = subprocess.run(
                scan_cmd,
                capture_output=True,
                text=True,
                timeout=20
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                
                for line in lines:
                    if line and not line.startswith("#"):
                        # Format: /dev/sda -d sat # /dev/sda, ATA device
                        parts = line.split()
                        if len(parts) >= 3:
                            device = parts[0]
                            device_type = parts[2]  # -d parameter value
                            device_key = device.replace("/dev/", "")
                            
                            # Get disc info
                            disk_info = self._get_disk_info_safe(
                                device, device_type, timeout=10
                            )
                            
                            if disk_info:
                                smart_data[device_key] = disk_info
                            else:
                                # Disk accessible without SMART
                                smart_data[device_key] = {
                                    "model": "Device (no SMART)",
                                    "smart_available": False,
                                    "device_type": device_type,
                                    "path": device
                                }
            
            # 2. If there are no disks, check basic disks.
            if not smart_data:
                _LOGGER.debug("No SMART-capable disks found via scan, checking basics")
                
                # Test only basic system disks
                basic_checks = [
                    ("/dev/sda", "sat"),
                    ("/dev/nvme0", "nvme"),
                ]
                
                for device, dev_type in basic_checks:
                    device_key = device.replace("/dev/", "")
                    info = self._get_disk_info_safe(device, dev_type, timeout=5)
                    if info:
                        smart_data[device_key] = info
            
            return smart_data
            
        except Exception as e:
            _LOGGER.error("Error scanning disks: %s", e)
            return {"error": f"Scan failed: {str(e)}"}

    def _get_smart_data_extended(self):
        """Get extended SMART data with retry logic."""
        smart_data = self._get_smart_data_fast()
        
        # For working discs, get more details.
        for disk_key in list(smart_data.keys()):
            if smart_data[disk_key].get("smart_available"):
                # Obtain detailed SMART attributes
                detailed = self._get_detailed_smart_attributes(f"/dev/{disk_key}")
                if detailed:
                    smart_data[disk_key].update(detailed)
        
        return smart_data

    def _get_disk_info_safe(self, device, device_type, timeout=10):
        """Safely get disk info with timeout."""
        device_key = device.replace("/dev/", "")
        
        try:
            # Build command according to type
            if device_type == "scsi":
                base_cmd = ["smartctl", "-a", "-d", "scsi"]
            elif device_type == "nvme":
                base_cmd = ["smartctl", "-a", "-d", "nvme"]
            else:
                base_cmd = ["smartctl", "-a", "-d", "sat"]
            
            # Try JSON first
            cmd_json = base_cmd + ["-j", device]
            result = subprocess.run(
                cmd_json,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                disk_info = json.loads(result.stdout)
                return self._parse_smart_info(disk_info, result.returncode)
            else:
                # Fallback to basic information without JSON
                cmd_info = ["smartctl", "-i", device]
                result_info = subprocess.run(
                    cmd_info,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                if result_info.returncode == 0:
                    return self._parse_basic_info_text(result_info.stdout, result.returncode)
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            pass
        
        return None

    def _parse_smart_info(self, disk_info, returncode):
        """Parse JSON SMART data with all critical attributes."""
        parsed = {
            "model": disk_info.get("model_name", "Unknown"),
            "serial": disk_info.get("serial_number", "Unknown"),
            "firmware": disk_info.get("firmware_version", "Unknown"),
            "capacity_gb": round(disk_info.get("user_capacity", {}).get("bytes", 0) / (1024**3), 1),
            "smart_passed": disk_info.get("smart_status", {}).get("passed", False),
            "smart_available": bool(
                disk_info.get("smart_status")
                or disk_info.get("ata_smart_attributes")
                or disk_info.get("nvme_smart_health_information_log")
            ),
            "temperature_c": None,
            "power_on_hours": None,
            "device_type": disk_info.get("device", {}).get("type", ""),
            "returncode": returncode,
            # CRITICAL ATTRIBUTES
            "reallocated_sectors": None,
            "pending_sectors": None,
            "uncorrectable_errors": None,
            "media_errors": None,
            "spin_retry_count": None,
            "seek_error_rate": None,
            # NVMe-SPECIFIC ATTRIBUTES
            "available_spare": None,
            "available_spare_threshold": None,
            "percentage_used": None,
            "data_units_read": None,
            "data_units_written": None,
            "data_units_read_tb": None,
            "data_units_written_tb": None,
            "host_read_commands": None,
            "host_write_commands": None,
            "controller_busy_time": None,
            "power_cycles": None,
            "unsafe_shutdowns": None,
            "error_info_log_entries": None,
            "warning_temp_time": None,
            "critical_temp_time": None,
            "critical_warning": None,
        }
        
        device_type = disk_info.get("device", {}).get("type", "").lower()
        
        # ========== NVMe ==========
        
        if "nvme" in device_type:
            nvme_smart = disk_info.get("nvme_smart_health_information_log", {})
            if nvme_smart:
                # Temperatura (principal)
                parsed["temperature_c"] = nvme_smart.get("temperature")
                
                # Available Spare (0-100%)
                parsed["available_spare"] = nvme_smart.get("available_spare")
                
                # Available Spare Threshold
                parsed["available_spare_threshold"] = nvme_smart.get("available_spare_threshold")
                
                # Percentage Used (desgaste)
                parsed["percentage_used"] = nvme_smart.get("percentage_used")
                
                # Data R/W
                data_units_read = nvme_smart.get("data_units_read")
                if data_units_read:
                    parsed["data_units_read"] = data_units_read
                    # Convert to TB
                    parsed["data_units_read_tb"] = round(data_units_read * 512 / (1000**4), 1)
                
                data_units_written = nvme_smart.get("data_units_written")
                if data_units_written:
                    parsed["data_units_written"] = data_units_written
                    parsed["data_units_written_tb"] = round(data_units_written * 512 / (1000**4), 1)
                
                # Commands
                parsed["host_read_commands"] = nvme_smart.get("host_read_commands")
                parsed["host_write_commands"] = nvme_smart.get("host_write_commands")
                
                # Controller time
                parsed["controller_busy_time"] = nvme_smart.get("controller_busy_time")
                
                # Cycles and shutdowns
                parsed["power_cycles"] = nvme_smart.get("power_cycles")
                parsed["unsafe_shutdowns"] = nvme_smart.get("unsafe_shutdowns")
                
                # Errors
                parsed["media_errors"] = nvme_smart.get("media_and_data_integrity_errors")
                parsed["error_info_log_entries"] = nvme_smart.get("error_information_log_entries")
                
                # Temperature times
                parsed["warning_temp_time"] = nvme_smart.get("warning_composite_temperature_time")
                parsed["critical_temp_time"] = nvme_smart.get("critical_composite_temperature_time")
                
                # Critical Warning
                parsed["critical_warning"] = nvme_smart.get("critical_warning")
                
                # Power on hours
                parsed["power_on_hours"] = nvme_smart.get("power_on_hours")
            
            # For NVMe, DO NOT use pending_sectors as available_spare
            if "pending_sectors" in parsed:
                parsed["pending_sectors"] = None
        
        else:
            # ========== PARA HDD/SSD SATA ==========
            
            # Temperature
            temp = disk_info.get("temperature", {})
            if temp:
                parsed["temperature_c"] = temp.get("current", temp.get("value"))
            
            # Power on hours
            power_time = disk_info.get("power_on_time", {})
            if power_time:
                parsed["power_on_hours"] = power_time.get("hours")
            
            # Parse specific SMART attributes - FIND THE CRITICAL ONES
            attributes = disk_info.get("ata_smart_attributes", {}).get("table", [])
            for attr in attributes:
                name = attr.get("name", "")
                raw_value = attr.get("raw", {}).get("value", 0)
                normalized_name = name.lower().replace("_", "").replace("-", "")
                
                # Temperature
                if "temperature" in normalized_name:
                    parsed["temperature_c"] = raw_value if not parsed["temperature_c"] else parsed["temperature_c"]
                
                # Power on hours
                elif "poweronhours" in normalized_name:
                    parsed["power_on_hours"] = raw_value if not parsed["power_on_hours"] else parsed["power_on_hours"]
                
                # === CRITICAL ATTRIBUTES ===
                
                # Current_Pending_Sector
                elif any(x in normalized_name for x in ["currentpendingsector", "pending"]):
                    parsed["pending_sectors"] = raw_value
                
                # Reallocated_Sector_Ct
                elif any(x in normalized_name for x in ["reallocatedsectorct", "reallocated"]):
                    parsed["reallocated_sectors"] = raw_value
                
                # Uncorrectable_Error_Cnt
                elif any(x in normalized_name for x in ["uncorrectableerrorcnt", "offlineuncorrectable"]):
                    parsed["uncorrectable_errors"] = raw_value
                
                # Spin_Retry_Count
                elif "spinretrycount" in normalized_name:
                    parsed["spin_retry_count"] = raw_value
                
                # Seek_Error_Rate
                elif "seekerrorrate" in normalized_name:
                    parsed["seek_error_rate"] = raw_value
                
                # Search by attribute ID
                attr_id = attr.get("id")
                if attr_id:
                    # Common SMART attribute IDs
                    if attr_id == 5:  # Reallocated_Sector_Ct
                        parsed["reallocated_sectors"] = raw_value
                    elif attr_id == 197:  # Current_Pending_Sector
                        parsed["pending_sectors"] = raw_value
                    elif attr_id == 198:  # Offline_Uncorrectable o Uncorrectable_Error_Cnt
                        parsed["uncorrectable_errors"] = raw_value
                    elif attr_id == 10:  # Spin_Retry_Count
                        parsed["spin_retry_count"] = raw_value
                    elif attr_id == 7:  # Seek_Error_Rate
                        parsed["seek_error_rate"] = raw_value
        
        return parsed

    def _parse_basic_info_text(self, text_output, returncode):
        """Parse basic disk info from text output."""
        parsed = {
            "model": "Unknown",
            "smart_available": False,
            "returncode": returncode,
            # Inicializar atributos críticos
            "reallocated_sectors": None,
            "pending_sectors": None,
            "uncorrectable_errors": None,
        }
        
        lines = text_output.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            if "model:" in line_lower and "unknown" not in line_lower:
                parsed["model"] = line.split(":", 1)[1].strip()
            elif "serial number:" in line_lower:
                parsed["serial"] = line.split(":", 1)[1].strip()
            elif "user capacity:" in line_lower:
                import re
                match = re.search(r'(\d+[,\.]?\d*)\s*bytes', line, re.IGNORECASE)
                if match:
                    try:
                        bytes_str = match.group(1).replace(',', '').replace('.', '')
                        bytes_val = int(bytes_str)
                        parsed["capacity_gb"] = round(bytes_val / (1024**3), 1)
                    except:
                        pass
        
        return parsed

    def _get_detailed_smart_attributes(self, device):
        """Get detailed SMART attributes for working disks."""
        detailed = {}

        try:
            # Determine device type
            cmd_check = ["smartctl", "-i", device]
            result_check = subprocess.run(
                cmd_check,
                capture_output=True,
                text=True,
                timeout=5
            )

            device_type = "unknown"
            if "nvme" in result_check.stdout.lower():
                device_type = "nvme"
            elif "ata" in result_check.stdout.lower() or "sata" in result_check.stdout.lower():
                device_type = "ata"

            # =======NVMe EXTENDED PARSING==========

            if device_type == "nvme":
                cmd = ["smartctl", "-x", device]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:

                        # Available Spare
                        if "Available Spare:" in line:
                            match = re.search(r'Available Spare:\s+(\d+)%', line)
                            if match:
                                detailed["available_spare"] = int(match.group(1))

                        # Available Spare Threshold
                        elif "Available Spare Threshold:" in line:
                            match = re.search(r'Available Spare Threshold:\s+(\d+)%', line)
                            if match:
                                detailed["available_spare_threshold"] = int(match.group(1))

                        # Percentage Used
                        elif "Percentage Used:" in line:
                            match = re.search(r'Percentage Used:\s+(\d+)%', line)
                            if match:
                                detailed["percentage_used"] = int(match.group(1))

                        # Data Units Read
                        elif "Data Units Read:" in line:
                            match = re.search(r'Data Units Read:\s+([\d,]+)', line)
                            if match:
                                val = int(match.group(1).replace(",", ""))
                                detailed["data_units_read"] = val
                                detailed["data_units_read_tb"] = round(val * 512 / (1000**4), 1)

                        # Data Units Written
                        elif "Data Units Written:" in line:
                            match = re.search(r'Data Units Written:\s+([\d,]+)', line)
                            if match:
                                val = int(match.group(1).replace(",", ""))
                                detailed["data_units_written"] = val
                                detailed["data_units_written_tb"] = round(val * 512 / (1000**4), 1)

                        # Host Read Commands
                        elif "Host Read Commands" in line:
                            match = re.search(r'Host\s+Read\s+Commands:\s+([\d,]+)', line)
                            if match:
                                detailed["host_read_commands"] = int(match.group(1).replace(",", ""))


                        # Host Write Commands
                        elif "Host Write Commands" in line:
                            match = re.search(r'Host\s+Write\s+Commands:\s+([\d,]+)', line)
                            if match:
                                detailed["host_write_commands"] = int(match.group(1).replace(",", ""))


                        # Controller Busy Time
                        elif "Controller Busy Time:" in line:
                            match = re.search(r'Controller Busy Time:\s+(\d+)', line)
                            if match:
                                detailed["controller_busy_time"] = int(match.group(1))

                        # Power Cycles
                        elif "Power Cycles:" in line:
                            match = re.search(r'Power Cycles:\s+(\d+)', line)
                            if match:
                                detailed["power_cycles"] = int(match.group(1))

                        # Power On Hours
                        elif "Power On Hours:" in line:
                            match = re.search(r'Power On Hours:\s+(\d+)', line)
                            if match:
                                detailed["power_on_hours"] = int(match.group(1))

                        # Unsafe Shutdowns
                        elif "Unsafe Shutdowns:" in line:
                            match = re.search(r'Unsafe Shutdowns:\s+(\d+)', line)
                            if match:
                                detailed["unsafe_shutdowns"] = int(match.group(1))

                        # Media Errors
                        elif "Media and Data Integrity Errors:" in line:
                            match = re.search(r'Media and Data Integrity Errors:\s+(\d+)', line)
                            if match:
                                detailed["media_errors"] = int(match.group(1))

                        # Error Log Entries
                        elif "Error Information Log Entries" in line:
                            match = re.search(r'Entries:\s+(\d+)', line)
                            if match:
                                detailed["error_info_log_entries"] = int(match.group(1))

                        # Warning Temp Time
                        elif "Warning  Comp. Temperature Time" in line:
                            match = re.search(r'Time:\s+(\d+)', line)
                            if match:
                                detailed["warning_temp_time"] = int(match.group(1))


                        # Critical Temp Time
                        elif "Critical Comp. Temperature Time" in line:
                            match = re.search(r'Time:\s+(\d+)', line)
                            if match:
                                detailed["critical_temp_time"] = int(match.group(1))

            # =======SATA / SAS PARSING======
            
            else:
                cmd = ["smartctl", "-A", device]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:

                        if "Reallocated_Sector_Ct" in line:
                            match = re.search(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
                            if match:
                                detailed["reallocated_sectors"] = int(match.group(4))

                        elif "Current_Pending_Sector" in line:
                            match = re.search(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
                            if match:
                                detailed["pending_sectors"] = int(match.group(4))

                        elif "Uncorrectable_Error_Cnt" in line:
                            match = re.search(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
                            if match:
                                detailed["uncorrectable_errors"] = int(match.group(4))

        except Exception:
            pass

        return detailed


    def _check_sensors(self):
        """Check if lm-sensors is working."""
        try:
            result = subprocess.run(
                ["sensors", "-v"],
                capture_output=True,
                timeout=3
            )
            return result.returncode == 0
        except Exception:
            return False

    def _check_smartctl(self):
        """Check if smartctl is working."""
        try:
            result = subprocess.run(
                ["smartctl", "--version"],
                capture_output=True,
                timeout=3
            )
            return result.returncode == 0
        except Exception:
            return False

    def _get_disk_health_summary(self):
        """Get disk health summary."""
        try:
            smart_data = self._get_smart_data_fast()
            working = 0
            failed = 0
            
            for disk, info in smart_data.items():
                if info.get("smart_available") and info.get("smart_passed"):
                    working += 1
                else:
                    failed += 1
            
            return {
                "working": working,
                "failed": failed,
                "total": working + failed
            }
        except Exception:
            return {"working": 0, "failed": 0, "total": 0}

    def _send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if isinstance(data, bytes):
            self.wfile.write(data)
        else:
            self.wfile.write(data.encode())

    def _send_error_response(self, message):
        """Send error response."""
        error_data = json.dumps({"error": message})
        self.send_response(500)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(error_data.encode())

    def log_message(self, format, *args):
        """Reduce log noise."""
        pass

def main():
    port = 9000
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"PVE Sensors API v2 started on port {port}")
    print("Endpoints:")
    print(f"  GET /sensors         - lm-sensors data")
    print(f"  GET /smart           - Basic SMART data (fast)")
    print(f"  GET /smart-extended  - Extended SMART data")
    print(f"  GET /health          - System health status")
    server.serve_forever()

if __name__ == "__main__":
    main()
