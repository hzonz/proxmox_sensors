# 📚 Documentation et Guides

Pour garantir une configuration sans problèmes, veuillez suivre ces guides étape par étape :

---

## 🌡️ [01. Configuration des Capteurs Matériels](01-install-sensors.md)
Comment installer et configurer **lm-sensors** sur votre nœud Proxmox afin d’activer la surveillance des températures et des ventilateurs.

---

## 🔑 [02. Configuration de Proxmox](02-proxmox-config.md)
Comment créer un **utilisateur** et un **API Token** sécurisés dans Proxmox (PVE et PBS) avec les permissions minimales nécessaires.

---

## ⚙️ [03. Connexion de l’Intégration (PVE et PBS)](03-login-pve-pbs.md)
Guide à travers le processus de configuration initiale dans Home Assistant et la connexion à vos serveurs.

---

## ❓ [04. Foire Aux Questions et Dépannage](04-faq.md)
Questions fréquentes, problèmes connus et comment les résoudre.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Introduction

**Proxmox Extended Sensors est l’intégration la plus complète, efficace et avancée pour Home Assistant, conçue pour offrir un contrôle réel et une surveillance approfondie de Proxmox VE et Proxmox Backup Server (PBS).**

Cette intégration va bien au‑delà de la simple visualisation de données : elle offre une **visibilité totale** de votre infrastructure et ajoute de **véritables capacités de contrôle**, vous permettant de gérer les nœuds, machines virtuelles, conteneurs, disques, datastores et tâches PBS directement depuis Home Assistant.

Contrairement à d’autres solutions, Proxmox Extended Sensors est construit avec une approche professionnelle :

- **Surveillance avancée** du matériel, des VMs, CTs, disques et PBS.  
- **Actions de contrôle complètes** (démarrer, arrêter, éteindre, redémarrer, réinitialiser, mettre en pause, hiberner…).  
- **Services de sauvegarde entièrement intégrés**, pour des backups individuels ou massifs.  
- **Compatibilité totale avec PBS**, incluant la déduplication et la nomenclature automatique.  
- **Authentification sécurisée basée sur des Tokens**.  
- **Structure propre et organisée** des entités et appareils.  
- **Utilisation minimale des ressources** grâce à un polling optimisé.

Les sauvegardes créées depuis Home Assistant s’intègrent parfaitement à celles créées depuis Proxmox VE, utilisant des noms identifiables tels que :  
**HA-{{vmid}}-{{guestname}}**  
et conservent **tous les avantages de PBS**, y compris la déduplication et la compatibilité avec les chaînes de sauvegarde existantes.

En résumé, cette intégration transforme Home Assistant en un **véritable panneau de contrôle Proxmox**, combinant surveillance détaillée, automatisation avancée et contrôle total de l’infrastructure.

---

## 🧩 Versions Compatibles

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x ou supérieur

---

## 📑 Table des Matières

- [Fonctionnalités Clés](#-caractéristiques-clé-v200)  
- [État et Performance du Nœud](#-état-et-performance-du-nœud)  
- [Disques et SMART](#-disques-et-smart)  
- [Machines Virtuelles (QEMU)](#-machines-virtuelles-qemu)  
- [Conteneurs (LXC)](#-conteneurs-lxc)  
- [Services de Sauvegarde](#-services-de-sauvegarde-vms-et-cts)  
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)  
- [Actions de Contrôle (PVE et PBS)](#-actions-de-contrôle-pve-et-pbs)  
- [Installation](#-installation)  
- [Guide Visuel de Configuration](#-guide-visuel-de-configuration)  
- [Contributions](#-contributions-et-communauté)

---

<details>
  <summary>🖼️ Aperçu du Dashboard</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox">
  </p>
  *Exemple d’un dashboard moderne utilisant **Card-Mod** (Mode Sombre) et nos capteurs structurés :*
</details>

---

## 🔥 Fonctionnalités Clés (v2.0.0)

### 🌡️ Surveillance Matérielle Avancée (PVE et PBS)

- **Températures en temps réel :** cœurs CPU, VRM, chipset, NVMe/SSD/HDD.  
- **Capteurs mécaniques :** vitesses des ventilateurs (RPM), tensions et autres capteurs de la carte mère.  
- **Filtrage intelligent :** seules les entités avec données valides sont créées pour garder votre système propre.  
  > Nécessite `lm-sensors` sur l’hôte Proxmox.

---

### 🧠 État et Performance du Nœud

- Utilisation CPU, I/O wait, load average.  
- RAM totale/utilisée/libre et pourcentage.  
- Temps de fonctionnement (uptime) et version du kernel/PVE.  
- Capteurs réseau RX/TX pour le nœud, les VMs et les conteneurs.

<details>
  <summary>🔳 Attributs du Nœud</summary>
  <p align="center">
    <img src="../../img/pve/node_attr.png" alt="Attributs du Nœud" width="600">
  </p>
</details>

<details>
  <summary>⭕ Contrôles du Nœud</summary>
  <p align="center">
    <img src="../../img/pve/node_controls.png" alt="Contrôles du Nœud" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Température CPU</summary>
  <p align="center">
    <img src="../../img/pve/cpu_temp_attr.png" alt="Température CPU" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Température du Chipset</summary>
  <p align="center">
    <img src="../../img/pve/chipset_temp.png" alt="Température Chipset" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O Wait</summary>
  <p align="center">
    <img src="../../img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Disques & SMART

- Capteurs de disques physiques regroupés comme appareils dédiés.  
- Espace total/utilisé, niveau d’usure (NVMe wear level) et plus.  
- Attributs SMART pour HDD/SSD/NVMe (si disponibles).  
- Capteurs de température dédiés selon le type de disque (SATA, NVMe, etc.).

<details>
  <summary>💾 Capteurs de Disque</summary>
  <p align="center">
    <img src="../../img/pve/disks_sensors.png" alt="Capteurs de Disque" width="600">
  </p>
</details>

<details>
  <summary>🩺 Attributs SMART HDD/SSD</summary>
  <p align="center">
    <img src="../../img/pve/disk_hd_smart_attr.png" alt="SMART HDD" width="600">
  </p>
</details>

<details>
  <summary>🩺 Attributs SMART NVMe</summary>
  <p align="center">
    <img src="../../img/pve/disk_nvme_smart_attr.png" alt="SMART NVMe" width="600">
  </p>
</details>

---

### 🖥️ Machines Virtuelles (QEMU)

- État, utilisation CPU, RAM utilisée/totale, disque utilisé/total.  
- Réseau RX/TX par VM.  
- Uptime et capteurs d’information de base.  
- Organisation propre des appareils par VM dans Home Assistant.

<details>
  <summary>🖥️ Contrôles et Capteurs de VM</summary>
  <p align="center">
    <img src="../../img/pve/vm_control.png" alt="Contrôle VM" width="600">
  </p>
</details>

---

### 📦 Conteneurs (LXC)

- État, utilisation CPU, RAM utilisée/totale, disque utilisé/total.  
- Réseau RX/TX par conteneur.  
- Uptime et capteurs d’information de base.  
- Même organisation propre que pour les VMs.

<details>
  <summary>📦 Contrôles et Capteurs de Conteneurs</summary>
  <p align="center">
    <img src="../../img/pve/ct_control.png" alt="Contrôle CT" width="600">
  </p>
</details>

---

## 💾 Services de Sauvegarde (VMs et CTs)

L’intégration inclut deux puissants services de sauvegarde permettant de créer **des backups Proxmox directement depuis Home Assistant**, totalement compatibles avec Proxmox VE et Proxmox Backup Server (PBS).
