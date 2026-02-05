# 🚀 Step 1: Sensor Installation and Configuration
**This guide explains how to prepare the Proxmox node to expose hardware data and ensure temperature readings are available for Home Assistant.**

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

**Answer YES (or press Enter) to all questions. Once finished, the system will identify the required modules (e.g., coretemp for Intel CPUs).**

## 3. Module Persistence
**To ensure the sensors activate automatically when the server reboots, the sensors-detect wizard will ask a key question at the very end:**

`Do you want to add these lines automatically to /etc/modules? (yes/NO)`

> [!CAUTION]
> **You must manually type yes and press Enter.** If you just press Enter without typing anything, the system will select NO by default. If this happens, the sensors will not load after a reboot, and Home Assistant will stop receiving temperature data.

## 4. Immediate Verification
**To activate the sensors right now without rebooting, run:**

```bash
# Load the detected modules (example for Intel)

modprobe coretemp

# Verify that temperatures are being displayed
sensors
```

## 🚀 Step 5: Sensor Server Installation (API Bridge)
**Since the official Proxmox API does not expose all hardware data, it is necessary to install this small "bridge" script on the Proxmox host.**

1. **Script download and installation**
Run these commands in your Proxmox server terminal:
```bash
# Download the script from the repository
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Grant execution permissions
chmod +x /usr/local/bin/pve-sensors-api.py
```

2. **System service configuration**
To ensure the script starts automatically with the server, create the service file:
```bash
cat <<EOF > /etc/systemd/system/pve-sensors.service
[Unit]
Description=PVE Sensors API
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

3. **Immediate activation**
Enable and start the service with these commands:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
```

4. **Final verification**
You can verify that the server is working by opening this address in your browser (replacing it with your Proxmox IP): `http://YOUR_PROXMOX_IP:9000/sensors`

If you see text in JSON format with the temperatures, the integration will now be able to read the data correctly.

---

**Done! Once the sensors command returns data in the terminal, your Home Assistant integration will be able to read them automatically through the Proxmox API.**
