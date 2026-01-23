<p align="center">
  <img src="/custom_components/proxmox_sensors/images/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>



# UNDER CONSTRUCTION

### 🌐 Choose your language / Elige tu idioma

| [![English](https://img.shields.io/badge/ENGLISH-blue?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/en/README.md) | [![Español](https://img.shields.io/badge/ESPA%C3%91OL-orange?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/es/README.md) | [![Italiano](https://img.shields.io/badge/ITALIANO-green?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/it/README.md) | [![Français](https://img.shields.io/badge/FRAN%C3%87AIS-blue?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/fr/README.md) |
|:---:|:---:|:---:|:---:|

<br>

<p align="center">
| [![Deutsch](https://img.shields.io/badge/DEUTSCH-red?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/de/README.md) | [![Nederlands](https://img.shields.io/badge/NEDERLANDS-orange?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/nl/README.md) | [![Русский](https://img.shields.io/badge/%D0%A0%D0%A3%D0%A1%D0%A1%D0%9A%D0%98%D0%99-lightgrey?style=for-the-badge&logo=googletranslate&logoColor=white)](docs/ru/README.md) |
|:---:|:---:|:---:|
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
## Featured Sensors
## PVE
### 🖥️ Hardware Sensors (PVE & PBS)
CPU temperatures • VRM temperatures • NVMe/SSD/HDD temperatures  
Fan speeds (RPM) • Voltages • Power sensors • `pvesensors` entities
• Chipset temperature 

### 🧠 Node Status
CPU usage (%) • RAM usage (%) • RAM used/total  
Uptime • Load average • CPU I/O Wait 

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
• Complete Tasks Information and more 

**Dashboard Example**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

  
---

## 📚 Documentation & Guides
To ensure a smooth setup, please follow these step-by-step guides:

### 🚀 Installation Guide: How to add the repository via HACS or manual method.

### 🔑 API Token & Permissions: How to create a secure user and token in Proxmox with the correct permissions.

### 🌡️ Hardware Sensors Setup: How to install and configure lm-sensors on your Proxmox node.

### ⚙️ Initial Configuration: Walking through the first-time setup and login process.
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
