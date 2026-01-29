<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

# 🚀 Proxmox Extended Sensors

**The most comprehensive, efficient, and organized integration for monitoring Proxmox VE and PBS from Home Assistant.**

This integration is designed for users who require full control over their hardware without overloading their server. Unlike other solutions, **Proxmox Sensors Extended** focuses on energy efficiency, secure Token-based authentication, and impeccable visual organization.

---

## 📚 Documentation & Guides
**Select your language to start the installation and configuration:**

[![English](https://img.shields.io/badge/ENGLISH-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/en/README.md)
[![Español](https://img.shields.io/badge/ESPA%C3%91OL-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/es/README.md)
[![Italiano](https://img.shields.io/badge/ITALIANO-green?style=for-the-badge&logo=translate&logoColor=white)](docs/it/README.md)
[![Français](https://img.shields.io/badge/FRAN%C3%87AIS-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/fr/README.md)
[![Deutsch](https://img.shields.io/badge/DEUTSCH-red?style=for-the-badge&logo=translate&logoColor=white)](docs/de/README.md)
[![Nederlands](https://img.shields.io/badge/NEDERLANDS-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/nl/README.md)
[![Русский](https://img.shields.io/badge/%D0%A0%D0%A3%D0%A1%D0%A1%D0%9A%D0%98%D0%99-lightgrey?style=for-the-badge&logo=translate&logoColor=white)](docs/ru/README.md)

---


## 🖼️ Dashboard Preview
*Example of a modern dashboard using **Card-Mod** (Dark Mode) and our structured sensors:*

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## 🔥 Key Features

### 🛡️ Advanced Backup Management (v1.3.0)
* **Trigger Backups from HA:** Start manual backups (`vzdump`) for VMs and Containers directly via Home Assistant actions.
* **Smart Identification:** Backups triggered from HA are automatically tagged with `ID | HA Backup` in Proxmox.
* **Remote Storage Support:** Full compatibility with local storage and **Proxmox Backup Server (PBS)**, including remote providers like **Tuxis**.
* **Incremental Efficiency:** Leverages PBS deduplication to minimize bandwidth and storage usage on every backup.

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/backup-iu.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

### 🌡️ Deep Hardware Monitoring
* **Real-time Temperatures:** CPU Cores, VRM, and NVMe/SSD/HDD drives.
* **Mechanical Sensors:** Fan speeds (RPM) and motherboard voltages.
* **Smart Filtering:** Only entities with valid data are created.
*(Note: Requires lm-sensors on the Proxmox host).*

### 🧠 Performance & Security
* **DataUpdateCoordinator:** Minimizes API calls to save CPU cycles.
* **Silent SSL:** Handles self-signed certificates without log spam.
* **Secure Auth:** Full support for Proxmox API Tokens (PVE & PBS).

### 🎨 Visual Organization
* **Smart Grouping:** Sensors automatically organized by: **1. Node**, **2. Physical Disks**, **3. VMs**, **4. Containers**.
* **Auto-Prefixes:** Keep your entity list and dashboards sorted by default.


---

## 🚀 Roadmap

- [x] **Network RX/TX sensors for VMs and Containers**  
- [x] **Detailed host CPU/RAM advanced metrics**  
- [x] **PBS maintenance buttons (GC, Prune, Verify, Sync)**  
- [x] **New PBS “Last Action” sensor with persistent local state**  
- [x] **Improved PBS sensor naming (cleaner UI without datastore prefix)**  
- [x] **Internal refactor and code cleanup for better stability and maintainability**  
- [x] **Create backups directly from PVE (VMs & Containers) via Home Assistant**
- [x] **Additional PBS maintenance sensors (progress, duration, logs)**  
- [ ] Custom Lovelace Card templates  
- [ ] Official HACS Repository submission  
- [ ] Optional advanced PBS dashboard  
  

---

## 🤝 Contributing & Community
Contributions are welcome! Feel free to open issues or pull requests.
**[Visit GitHub Repository](https://github.com/Javisen/proxmox_sensors)**

---
<p align="center"><i>Maintained by Javisen - MIT License</i></p>
