<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

# 🚀 Proxmox Extended Sensors

**The most comprehensive, efficient, and organized integration for monitoring and controlling Proxmox VE and Proxmox Backup Server (PBS) from Home Assistant.**

This integration is built for users who need **full visibility and control** over their Proxmox infrastructure without overloading the server.  
Unlike other solutions, **Proxmox Extended Sensors** focuses on:

- Energy‑efficient polling  
- Secure Token‑based authentication  
- Clean, logical and visually organized entities and devices  

---

## 📚 Documentation & Guides

**Select your language to start the installation and configuration:**

[![English](https://img.shields.io/badge/ENGLISH-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/en/README.md)
[![Español](https://img.shields.io/badge/ESPA%C3%91OL-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/es/README.md)
[![Italiano](https://img.shields.io/badge/ITALIANO-green?style=for-the-badge&logo=translate&logoColor=white)](docs/it/README.md)
[![Français](https://img.shields.io/badge/FRAN%C3%87AIS-blue?style=for-the-badge&logo=translate&logoColor=white)](docs/fr/README.md)
[![Deutsch](https://img.shields.io/badge/DEUTSCH-red?style=for-the-badge&logo=translate&logoColor=white)](docs/de/README.md)
[![Nederlands](https://img.shields.io/badge/NEDERLANDS-orange?style=for-the-badge&logo=translate&logoColor=white)](docs/nl/README.md)
[![Português](https://img.shields.io/badge/PORTUGU%C3%8AS-green?style=for-the-badge&logo=translate&logoColor=white)](docs/pt/README.md)
[![Русский](https://img.shields.io/badge/%D0%A0%D0%A3%D0%A1%D0%A1%D0%9A%D0%98%D0%99-lightgrey?style=for-the-badge&logo=translate&logoColor=white)](docs/ru/README.md)

---

## 🖼️ Dashboard Preview

*Example of a modern dashboard using **Card‑Mod** (Dark Mode) and the structured sensors provided by the integration:*

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## 🔥 Key Features (v2.0.0)

### 🌡️ Advanced Hardware Monitoring (PVE & PBS)

- **Real‑time temperatures:** CPU cores, VRM, chipset, NVMe/SSD/HDD.
- **Mechanical sensors:** Fan speeds (RPM), voltages and other board sensors.
- **Smart filtering:** Only entities with valid data are created to keep your system clean.  
  > Requires `lm-sensors` on the Proxmox host.

---

## Guía Visual de Configuración

<details>
  <summary>📸 Captura: Proceso de Logueo user + passw</summary>
  <p align="center">
    <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/tree/img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Asegúrate de usar el reino `pam` o `pve` según tu configuración de usuario.
</details>

<details>
  <summary>📸 Captura: Proceso de Logueo user + token</summary>
  <p align="center">
    <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  > Asegúrate de usar el reino `pam` o `pve` según tu configuración de usuario.
</details>

<details>
  <summary>⚙️ Captura: Configuración de la Integración</summary>
  <br>
  
  ![Configuración]([ruta/a/tu/imagen_config.png](https://raw.githubusercontent.com/Javisen/proxmox_sensors/img/install/setup_pve_1.png))
  
  *Nota: Introduce la IP del nodo y el token de la API.*
</details>

<details>
  <summary>📊 Captura: Detalles de los Sensores</summary>
  <br>
  
  ![Sensores](ruta/a/tu/imagen_sensores.png)
  
  Lista de sensores incluidos: CPU Usage, RAM, Status y Uptime.
</details>


### 🧠 Node Status & Performance

- CPU usage, I/O wait, load average.
- RAM total/used/free and percentage.
- Uptime and kernel/PVE version.
- Network RX/TX sensors for node, VMs and containers.

---

### 💾 Disks & SMART

- Physical disk sensors grouped as dedicated devices.
- Total/used space, wear level (NVMe), and more.
- SMART‑related attributes for HDD/SSD/NVMe (where available).
- Dedicated temperature sensors per disk type (SATA, NVMe, etc.).

---

### 🖥️ Virtual Machines (QEMU)

- Status, CPU usage, memory used/total, disk used/total.
- Network RX/TX per VM.
- Uptime and basic info sensors.
- Clean device grouping per VM in Home Assistant.

---

### 📦 Containers (LXC)

- Status, CPU usage, memory used/total, disk used/total.
- Network RX/TX per container.
- Uptime and basic info sensors.
- Same clean device structure as VMs.

---

### 🗄️ Proxmox Backup Server (PBS)

**Deep datastore and task monitoring:**

- Datastore usage (GB and %), total, used and free.
- Deduplication ratio and backup count.
- Last backup time, size and status.
- Backup errors and backup summary.
- Garbage Collector (GC) status and related sensors.
- Last task: type, status, message and duration.

**PBS control actions:**

- Run **Garbage Collector (GC)**.
- Run **Prune**.
- Run **Verify**.
- Run **Sync**.

---

### 🎛️ Control Actions (PVE & PBS)

**Node controls:**

- Shutdown node.
- Reboot node.

**VM controls (QEMU):**

- Start, Stop, Shutdown, Reboot, Reset.
- Pause, Resume, Hibernate.

**Container controls (LXC):**

- Start, Stop, Shutdown, Reboot.

**PBS controls:**

- GC, Prune, Verify, Sync (per datastore).

---

### 🎨 Visual Organization & Naming

- Sensors automatically grouped into logical devices:
  1. Node  
  2. Physical disks  
  3. Virtual machines  
  4. Containers  
  5. Storages / Datastores  
  6. PBS server and tasks
- Consistent, clean naming for entities and devices to keep dashboards readable and scalable.

---

## 🧩 Installation

### 🔹 Via HACS (recommended)

1. Open **HACS → Integrations**.
2. Click the three dots (⋮) → **Custom repositories**.
3. Add this repository:
   - URL: `https://github.com/Javisen/proxmox_sensors`
   - Category: **Integration**
4. Search for **“Proxmox Extended Sensors”** in HACS and install it.
5. Restart Home Assistant.
6. Go to **Settings → Devices & Services → Add Integration** and search for **Proxmox Extended Sensors**.

### 🔹 Manual installation

1. Copy the folder `custom_components/proxmox_sensors` into:
   - `/config/custom_components/proxmox_sensors`
2. Restart Home Assistant.
3. Add the integration from **Settings → Devices & Services**.

---
**If you enjoy this integration or find it useful, please consider giving the project a ⭐ on GitHub.**  
**It helps visibility, motivates development, and supports future features.**

## 🤝 Contributing & Community

Contributions are welcome! Feel free to open issues or pull requests.  
**[Visit GitHub Repository](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Maintained by Javisen - MIT License</i></p>
