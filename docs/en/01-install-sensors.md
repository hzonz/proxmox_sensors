# 🚀 Step 1: Installation and Sensor Automation
**This guide explains how to prepare the Proxmox node to expose hardware data and ensure the telemetry service starts automatically with the system.**

## 1. Installing Dependencies
* **First, we install the necessary tools to read the sensors integrated into the motherboard and CPU:**

```bash
apt update && apt install lm-sensors -y
```

## 2. Hardware Detection
* **To allow the system to identify which drivers it needs, we run the detection assistant:**

```bash
sensors-detect
```
**Answer YES (or press Enter) to all questions. Once finished, the system will identify the required modules (e.g., coretemp, nct6775).**

## 3. Module Persistence
**To ensure the sensors activate automatically when the server reboots, the sensors-detect wizard will ask a key question at the very end:**
```
Do you want to add these lines automatically to /etc/modules? (yes/NO)
```
> [!CAUTION]
> **You must manually type `yes` and press Enter.** If you just press Enter without typing anything, the system will select `NO` by default, and the sensors will not load after a reboot.

```bash
# Replace 'detected_module' with the names provided by the previous command
echo "detected_module" >> /etc/modules
```

## 4. Telemetry Service (Auto-Start)
**To allow Home Assistant to read this data continuously, we will configure the API script as a system service (systemd). This ensures that even if the server reboots, the service will start automatically.**

### A. Create the Service File

```bash
nano /etc/systemd/system/proxmox-sensors.service
```

### B. Service Configuration
**Copy and paste the following block. This design ensures that the service is lightweight and restarts automatically if a failure occurs:**

**💡 Tip for beginners: In most Proxmox terminals, you paste by right-clicking with the mouse or pressing Shift + Insert.**

* The standard Ctrl + V shortcut usually does not work here.

`Ini, TOML`
```ini
[Unit]
Description=Sensor API for Home Assistant
After=network.target

[Service]
Type=simple
User=root
# ⚠️ IMPORTANT: Change the path below to the ACTUAL location of your script
ExecStart=/usr/bin/python3 /path/to/your/sensor_script.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### C. Save and Exit
**Once you have pasted the code above, you must save the file by following these keyboard steps:**

1. Press Ctrl + O (this means "Write Out/Save").
2. Press Enter to confirm the filename.
3. Press Ctrl + X to exit the editor and return to the terminal.

### D. Service Activation
**Run these commands to register and activate the auto-start:**

```bash
# Reload the service configuration
systemctl daemon-reload

# Enable automatic start at system boot
systemctl enable proxmox-sensors.service

# Start the service immediately
systemctl start proxmox-sensors.service
```

# ✅ Verification
**To confirm that the service is running and scheduled for the next reboot, run:**

```bash
systemctl status proxmox-sensors.service
```

**You should see the status as active (running) and the indication enabled.**
