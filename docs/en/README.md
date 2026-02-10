# 📚 Documentation & Guides

To ensure a smooth setup, please follow these step-by-step guides:

---

## 🌡️ [01. Hardware Sensors Setup](01-install-sensors.md)
How to install and configure **lm-sensors** on your Proxmox node to enable temperature and fan monitoring.

---

## 🔑 [02. Proxmox Configuration](02-proxmox-config.md)
How to create a secure **user** and **API Token** in Proxmox (PVE & PBS) with the minimum required permissions.

---

## ⚙️ [03. Integration Login (PVE & PBS)](03-login-pve-pbs.md)
Walking through the first-time setup in Home Assistant and connecting to your servers.

---

## ❓ [04. FAQ & Troubleshooting](04-faq.md)
Common questions, known issues, and how to fix them.


---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Introduction

**Proxmox Extended Sensors is the most complete, efficient, and advanced integration for Home Assistant, designed to provide real control and deep monitoring of Proxmox VE and Proxmox Backup Server (PBS).**

This integration goes far beyond simple data display: it delivers **full visibility** of your infrastructure and adds **real control capabilities**, allowing you to manage nodes, virtual machines, containers, disks, datastores, and PBS tasks directly from Home Assistant.

Unlike other solutions, Proxmox Extended Sensors is built with a professional approach:

- **Advanced monitoring** of hardware, VMs, CTs, disks, and PBS  
- **Full control actions** (start, stop, shutdown, reboot, reset, pause, hibernate…)  
- **Fully integrated backup services**, both single and massive backups  
- **Complete PBS compatibility**, including deduplication and automatic naming  
- **Secure Token‑based authentication**  
- **Clean and organized entity/device structure**  
- **Minimal resource usage** thanks to optimized polling  

Backups created from Home Assistant integrate seamlessly with those created from Proxmox VE, using identifiable names such as: HA-{{vmid}}-{{guestname}} 
and retain **all PBS advantages**, including deduplication and compatibility with existing backup chains.

In short, this integration turns Home Assistant into a **complete control panel for Proxmox**, combining detailed monitoring, advanced automation, and full infrastructure control.

---

## 🧩 Supported Versions

- Proxmox VE 7.x / 8.x / 9.x
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x or newer  

---

## 📑 Table of Contents

- [Key Features](#-key-features-v200)
- [Node Status & Performance](#-node-status--performance)
- [Disks & SMART](#-disks--smart)
- [Virtual Machines (QEMU)](#-virtual-machines-qemu)
- [Containers (LXC)](#-containers-lxc)
- [Backups Services](#-Backup-Services-VMs--CTs)
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)
- [Control Actions (PVE & PBS)](#-control-actions-pve--pbs)
- [Installation](#-installation)
- [Visual Setup Guide](#-visual-setup-guide)
- [Contributing](#-contributing--community)



---

<details>
  <summary>🖼️ Dashboard Preview</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox" ">
  </p>
  *Example of a modern dashboard using **Card-Mod** (Dark Mode) and our structured sensors:*
</details>

---

## 🔥 Key Features (v2.0.0)

### 🌡️ Advanced Hardware Monitoring (PVE & PBS)

- **Real‑time temperatures:** CPU cores, VRM, chipset, NVMe/SSD/HDD.
- **Mechanical sensors:** Fan speeds (RPM), voltages and other board sensors.
- **Smart filtering:** Only entities with valid data are created to keep your system clean.  
  > Requires `lm-sensors` on the Proxmox host.

---

### 🧠 Node Status & Performance

- CPU usage, I/O wait, load average.
- RAM total/used/free and percentage.
- Uptime and kernel/PVE version.
- Network RX/TX sensors for node, VMs and containers.

<details>
  <summary>🔳 Node Attributes</summary>
  <p align="center">
    <img src="img/pve/node_attr.png" alt="Node Attributes" width="600">
  </p>
</details>

<details>
  <summary>⭕ Node Controls</summary>
  <p align="center">
    <img src="img/pve/node_controls.png" alt="Node Controls" width="600">
  </p>
</details>

<details>
  <summary>🌡️ CPU Temperature</summary>
  <p align="center">
    <img src="img/pve/cpu_temp_attr.png" alt="CPU Temperature" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Chipset Temperature</summary>
  <p align="center">
    <img src="img/pve/chipset_temp.png" alt="Chipset Temperature" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O Wait</summary>
  <p align="center">
    <img src="img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Disks & SMART

- Physical disk sensors grouped as dedicated devices.
- Total/used space, wear level (NVMe), and more.
- SMART‑related attributes for HDD/SSD/NVMe (where available).
- Dedicated temperature sensors per disk type (SATA, NVMe, etc.).

<details>
  <summary>💾 Disk Sensors</summary>
  <p align="center">
    <img src="img/pve/disks_sensors.png" alt="Disk Sensors" width="600">
  </p>
</details>

<details>
  <summary>🩺 HDD/SSD SMART Attributes</summary>
  <p align="center">
    <img src="img/pve/disk_hd_smart_attr.png" alt="HDD SMART" width="600">
  </p>
</details>

<details>
  <summary>🩺 NVMe SMART Attributes</summary>
  <p align="center">
    <img src="img/pve/disk_nvme_smart_attr.png" alt="NVMe SMART" width="600">
  </p>
</details>


---

### 🖥️ Virtual Machines (QEMU)

- Status, CPU usage, memory used/total, disk used/total.
- Network RX/TX per VM.
- Uptime and basic info sensors.
- Clean device grouping per VM in Home Assistant.

<details>
  <summary>🖥️ VM Controls & Sensors</summary>
  <p align="center">
    <img src="img/pve/vm_control.png" alt="VM Control" width="600">
  </p>
</details>

---

### 📦 Containers (LXC)

- Status, CPU usage, memory used/total, disk used/total.
- Network RX/TX per container.
- Uptime and basic info sensors.
- Same clean device structure as VMs.

<details>
  <summary>📦 Container Controls & Sensors</summary>
  <p align="center">
    <img src="img/pve/ct_control.png" alt="CT Control" width="600">
  </p>
</details>

---

## 💾 Backup Services (VMs & CTs)

The integration includes two powerful backup services that allow you to create **Proxmox backups directly from Home Assistant**, fully compatible with Proxmox VE and Proxmox Backup Server (PBS).

---

### 🟦 1. Single Backup Service  
Creates a backup of a specific VM or CT.

**Service:** `proxmox_sensors.create_vzdump_backup`

**Options available:**

- **Node** – Select the Proxmox node  
- **Target Storage** – Any storage supporting backups (local, NFS, PBS, etc.)  
- **VM/CT ID** – ID of the machine to back up  
- **Backup mode:**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Compression:**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

Backups created from Home Assistant are automatically named using: HA-{{vmid}}-{{guestname}}


This ensures they are easy to identify while remaining **fully compatible with existing Proxmox backups**.

<details>
  <summary>📦 Single Backup Service</summary>
  <p align="center">
    <img src="img/pve/single_backup.png" alt="Single Backup Service" width="600">
  </p>
</details>

---

### 🟩 2. Massive Backup Service  
Performs backups of **all VMs and/or CTs** on a selected node.

**Service:** `proxmox_sensors.backup_all`

**Options available:**

- **Node** – Select the node to back up  
- **Target Storage** – Any backup-capable storage  
- **Backup mode:** snapshot / suspend / stop  
- **Compression:** zstd / gzip / lzo / none  
- **Maximum concurrent backups** – Control parallel execution  
- **Delay between backups** – Seconds between each backup  
- **Include VMs** – Toggle  
- **Include CTs** – Toggle  

This service is ideal for scheduled nightly backups or automated maintenance routines.

<details>
  <summary>📦 Massive Backup Service</summary>
  <p align="center">
    <img src="img/pve/massive_backups.png" alt="Massive Backup Service" width="600">
  </p>
</details>


---

### 🟧 PBS Compatibility & Deduplication

Backups created through these services:

- Are stored exactly like backups created from Proxmox VE  
- Use the same naming and metadata structure  
- Support **PBS deduplication** automatically  
- Integrate seamlessly with existing backup chains  
- Appear in the PBS datastore with full compatibility  

No special configuration is required — PBS handles deduplication and indexing exactly as if the backup were created from the Proxmox GUI or CLI.

---


### 🗄️ Proxmox Backup Server (PBS)

**Deep datastore and task monitoring:**

- Datastore usage (GB and %), total, used and free.
- Deduplication ratio and backup count.
- Last backup time, size and status.
- Backup errors and backup summary.
- Garbage Collector (GC) status and related sensors.
- Last task: type, status, message and duration.

<details>
  <summary>🗄️ Datastore Overview</summary>
  <p align="center">
    <img src="img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ PBS Server</summary>
  <p align="center">
    <img src="img/pbs/pbs_server.png" alt="PBS Server" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Task Details</summary>
  <p align="center">
    <img src="img/pbs/task.png" alt="PBS Task" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Garbage Collector Status</summary>
  <p align="center">
    <img src="img/pbs/gc_status_attr.png" alt="GC Status" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Datastore Maintenance</summary>
  <p align="center">
    <img src="img/pbs/datastore_maintenance.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Last Task Summary</summary>
  <p align="center">
    <img src="img/pbs/last_task_stat.png" alt="Last Task" width="600">
  </p>
</details>

---

##PBS control actions:

- Run **Garbage Collector (GC)**.
- Run **Prune**.
- Run **Verify**.
- Run **Sync**.

<details>
  <summary>🗄️ Dtatastore Maintenance</summary>
  <p align="center">
    <img src="img/pbs/datastore_maintenance.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Last Task</summary>
  <p align="center">
    <img src="img/pbs/last_task_stat.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

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

## 🧭 Visual Setup Guide

Below you can find a complete visual walkthrough of the setup process, including login methods, resource selection, and configuration steps.

<details>
  <summary>🪪 Server Connection</summary>
  <p align="center">
    <img src="img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > We don't use "http://" or "https://". We already do it for you..
</details>

<details>
  <summary>🪪 Login using Username and Password (PVE only)</summary>
  <p align="center">
    <img src="img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Make sure to use the `pam` or `pve` realm according to your user settings.
</details>

<details> 
  <summary>🪪 Login using User and Token (PVE and PBS)</summary>
  <p align="center">
    <img src="img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **In the Token_id field, you should only enter the token name.**
</details>

<details>
  <summary>⚙️ Resources Selection</summary>
  <p align="center">
    <img src="img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Note: Select the CTs, VMs, and Storages you want to add, as well as the options.*
</details>

---

**If you enjoy this integration or find it useful, please consider giving the project a ⭐ on GitHub.**  
**It helps visibility, motivates development, and supports future features.**

## 🤝 Contributing & Community

Contributions are welcome! Feel free to open issues or pull requests.  
**[Visit GitHub Repository](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Maintained by Javisen - MIT License</i></p>
