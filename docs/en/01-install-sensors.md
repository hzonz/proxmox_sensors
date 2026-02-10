# 🚀 Step 1: Installation and sensor configuration

**This guide explains how to prepare the Proxmox node to expose hardware data and ensure that temperature readings and Smart data are available for Home Assistant.**


## 1. Installation of dependencies

*In order for the integration to read all hardware sensors and SMART attributes of the disks, it is necessary to install the following tools on Proxmox:*

- **lm-sensors** → CPU, motherboard, chipset, VRM, fan sensors…**
- **smartmontools** → SMART information for HDD, SSD and NVMe**


```bash

apt update && apt install lm-sensors smartmontools -y

```

## 2. Hardware detection

* **Run the detection wizard to identify the necessary modules:**


```bash

sensors-detect

```

**Answer YES (or press Enter) to all questions. At the end, the system will identify the necessary modules (for example: `coretemp` for Intel CPUs).**


## 3. Module persistence

**To ensure the sensors activate automatically when the server reboots, the `sensors-detect` wizard will ask a key question at the end of the process:**


`Do you want to add these lines automatically to /etc/modules? (yes/NO)`



> [!CAUTION]
> **You must manually type `yes` and press Enter.** If you just press Enter without typing anything, the system will select `NO` by default. If this happens, the sensors will not load after a reboot and Home Assistant will stop receiving temperature data.



## 4. Immediate verification

**To activate the sensors right now without having to reboot, run:**



```bash

# Load the detected modules (example for Intel)

modprobe coretemp

# Verify that temperatures are displayed

sensors

```

## 🚀 Step 5: Installation of the Sensor Server (API Bridge)
**The official Proxmox API does not expose all hardware sensors, so it is necessary to install a small script that acts as a bridge between Proxmox and Home Assistant.**

1. **Script download and installation**
Run these commands in your Proxmox server terminal:
```bash
# Download the script from the repository
wget [https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py](https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py) -O /usr/local/bin/pve-sensors-api.py

# Grant execution permissions
chmod +x /usr/local/bin/pve-sensors-api.py
```
2. **Configuration as a system service**
Create the service file:
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

```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
```

4. **Final verification**
Open in your browser:
```
http://YOUR_PROXMOX_IP:9000/sensors
```

If a JSON appears with temperatures and sensors, the server is working correctly.

## ✔ Conclusion

**Once the sensors command returns readings and the pve-sensors service is active, Home Assistant will be able to obtain all hardware data without the need for additional configurations.**
