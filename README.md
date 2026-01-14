# Proxmox Sensors Extended

An advanced integration for **Proxmox VE (PVE)** and **Proxmox Backup Server (PBS)** that brings detailed hardware, node, disk, VM, container, and datastore metrics into Home Assistant.

This project aims to be **more complete, more modular, and faster** than the official Proxmox integration, while remaining easy to configure through the Home Assistant UI.

---

## ✨ Features

### 🖥️ Hardware Sensors (PVE & PBS)
- CPU temperatures
- VRM temperatures
- NVMe / SSD / HDD temperatures
- Fan speeds (RPM)
- Voltages
- Power sensors
- Any sensor exposed by `pvesensors`

### 🧠 Node Status
- CPU usage (%)
- RAM usage (%)
- RAM used / total
- Uptime
- Load average

### 💾 Disks
- Total capacity
- Used space (GB and %)
- Wear-level (NVMe)
- SMART health (if available)

### 🖥️ Virtual Machines (QEMU)
- CPU usage (%)
- RAM usage (%)
- Status (running / stopped)
- Automatic or manual selection

### 📦 Containers (LXC)
- CPU usage (%)
- RAM usage (%)
- Status
- Automatic or manual selection

### 🗄️ Proxmox Backup Server (PBS)
- Datastore usage (GB and %)
- Backup count
- Garbage Collector status
- Last backup task status

---

## 🧰 Requirements

- Home Assistant 2023.6 or newer  
- Proxmox VE 7/8 or Proxmox Backup Server 2/3  
- User + password authentication (API tokens optional in future versions)

---

## 📦 Installation

### 🔧 Manual installation

1. Download this repository.
2. Copy the folder: custom_components/proxmox_sensors into your Home Assistant installation: /config/custom_components/proxmox_sensors
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration**.
5. Search for **Proxmox Sensors Extended**.


---

## ⚙️ Configuration

This integration includes a full **UI-based config flow** — no YAML required.

### Steps:

1. Enter:
   - Host (IP or hostname)
   - Username
   - Password
   - Node name
   - Server type (PVE or PBS)

2. Choose which categories you want to enable:
   - Hardware sensors
   - Node status sensors
   - Disk sensors
   - Virtual machines
   - Containers
   - PBS datastores
   - PBS tasks

3. For each category:
   - Hardware, node, and disk sensors → selectable individually  
   - VMs and containers → automatic or manual selection  
   - PBS datastores → manual selection  
   - PBS tasks → always automatic  

4. The integration will automatically create all required entities.

---

## 🧩 Entity Structure

Entities are grouped by category:

### Hardware

- sensor.cpu_core_0_temp

- sensor.nvme0_temp

- sensor.vrm_temp

...

### Node

- sensor.node_cpu_usage

- sensor.node_ram_usage

- sensor.node_uptime

...

### Disks

- sensor.disk_nvme0_usage

- sensor.disk_sda_usage

...

### Virtual Machines

- sensor.vm_101_cpu

- sensor.vm_101_ram

- sensor.vm_102_cpu

...

### Containers

- sensor.ct_201_cpu

- sensor.ct_201_ram

...

### PBS

- sensor.pbs_datastore_backup_usage

- sensor.pbs_last_task_status

...


---

## 🚀 Roadmap

- Add network RX/TX sensors for VMs and CTs  
- Add more detailed host CPU/RAM metrics  
- Add custom Lovelace cards  
- Add support for API tokens  
- Publish to HACS  

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open issues or pull requests:

https://github.com/Javisen/proxmox_sensors

---

## 📄 License

MIT License.
