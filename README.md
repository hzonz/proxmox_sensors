<p align="center">
  <img src="/custom_components/proxmox_sensors/images/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>




# 🚀 Proxmox Sensors Extended
**The most comprehensive, efficient, and organized integration for monitoring Proxmox VE and PBS from Home Assistant.**

This integration has been designed for advanced users who require full control over their hardware without overloading their server. Unlike other solutions, Proxmox Sensors Extended focuses on energy efficiency, secure Token-based authentication, and impeccable visual organization.

---

## 🔥 Key Features

### 🌡️ Deep Hardware Monitoring

**Don't settle for just CPU usage. See what is actually happening "under the hood":**

* **Real-time Temperatures: CPU Cores, VRM, and NVMe/SSD/HDD drives.**

* **Mechanical Sensors: Fan speeds (RPM) and motherboard voltages.**

* **Smart Sensors: Only entities that report valid data are created, keeping your system clutter-free.**

**(Note: Requires installing lm-sensors on the Proxmox host).**

---

### 🧠 Performance-Focused

**Designed with resource-constrained hardware in mind:**

* **DataUpdateCoordinator: Minimizes calls to the Proxmox API to avoid saturating the server's processor.**

* **Silent SSL: Automatic verification of SSL certificates (including self-signed) without spamming your error logs.**

---

### 🗄️ Advanced Proxmox Backup Server (PBS)
* **External Mode: Seamlessly connect to remote PBS servers using only the domain.**

* **Task Monitoring: Detailed status of the last Backup, Garbage Collector, or Verify task.**

---

### 🎨 Dynamic & Organized UI
* **Smart Dashboard: Sensors are automatically grouped into devices: 1. Node, 2. Physical Disks, 3. VMs, 4. Containers.**

* **Auto-Naming: Automatic prefixes (e.g., pv1-cpu-temp) so your dashboards stay logically ordered by themselves.**

---

### 🖥️ Hardware Sensors (PVE & PBS)
CPU temperatures • VRM temperatures • NVMe/SSD/HDD temperatures  
Fan speeds (RPM) • Voltages • Power sensors • `pvesensors` entities

### 🧠 Node Status
CPU usage (%) • RAM usage (%) • RAM used/total  
Uptime • Load average

### 💾 Disks
Total capacity • Used space (GB and %)  
Wear-level (NVMe) • SMART health (if available)

### 🖥️ Virtual Machines (QEMU)
CPU usage (%) • RAM usage (%)  
Status (running/stopped) • Auto/manual selection

### 📦 Containers (LXC)
CPU usage (%) • RAM usage (%)  
Status • Auto/manual selection

### 🗄️ Proxmox Backup Server (PBS)
Datastore usage (GB and %) • Backup count  
Garbage Collector status • Last backup task status


  
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
