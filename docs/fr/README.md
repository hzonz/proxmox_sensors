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

---

### 🟦 1. Service de Sauvegarde Individuelle  
Crée une sauvegarde d’une VM ou d’un CT spécifique.

**Service :** `proxmox_sensors.create_vzdump_backup`

**Options disponibles :**

- **Nœud** – Sélectionne le nœud Proxmox.  
- **Stockage de destination** – Tout stockage compatible avec les sauvegardes (local, NFS, PBS, etc.).  
- **ID de VM/CT** – ID de la machine à sauvegarder.  
- **Mode de sauvegarde :**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Compression :**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

Les sauvegardes créées depuis Home Assistant sont automatiquement nommées :  
**HA-{{vmid}}-{{guestname}}**

Cela garantit une identification facile tout en maintenant une **compatibilité totale avec les sauvegardes existantes de Proxmox**.

<details>
  <summary>📦 Service de Sauvegarde Individuelle</summary>
  <p align="center">
    <img src="../../img/pve/single_backup.png" alt="Service de Sauvegarde Individuelle" width="600">
  </p>
</details>

---

### 🟩 2. Service de Sauvegarde Massive  
Effectue des sauvegardes de **toutes les VMs et/ou CTs** d’un nœud sélectionné.

**Service :** `proxmox_sensors.backup_all`

**Options disponibles :**

- **Nœud** – Sélectionne le nœud à sauvegarder.  
- **Stockage de destination** – Tout stockage compatible avec les sauvegardes.  
- **Mode de sauvegarde :** snapshot / suspend / stop.  
- **Compression :** zstd / gzip / lzo / none.  
- **Nombre maximal de sauvegardes simultanées** – Contrôle l’exécution en parallèle.  
- **Délai entre sauvegardes** – Secondes entre chaque sauvegarde.  
- **Inclure les VMs** – Interrupteur (Oui/Non).  
- **Inclure les CTs** – Interrupteur (Oui/Non).

Ce service est idéal pour les sauvegardes nocturnes planifiées ou les routines de maintenance automatisées.

<details>
  <summary>📦 Service de Sauvegarde Massive</summary>
  <p align="center">
    <img src="../../img/pve/massive_backups.png" alt="Service de Sauvegarde Massive" width="600">
  </p>
</details>

---

### 🟧 Compatibilité PBS et Déduplication

Les sauvegardes créées via ces services :

- Sont stockées exactement comme celles créées depuis Proxmox VE  
- Utilisent la même structure de noms et de métadonnées  
- Supportent automatiquement la **déduplication PBS**  
- S’intègrent parfaitement aux chaînes de sauvegardes existantes  
- Apparaissent dans le datastore PBS avec une compatibilité totale  

Aucune configuration spéciale n’est requise : PBS gère la déduplication et l’indexation exactement comme si la sauvegarde avait été créée depuis l’interface graphique ou la CLI de Proxmox.

---

### 🗄️ Proxmox Backup Server (PBS)

**Supervision avancée du datastore et des tâches :**

- Utilisation du datastore (GB et %), total, utilisé et libre.  
- Ratio de déduplication et nombre de sauvegardes.  
- Heure, taille et état de la dernière sauvegarde.  
- Erreurs de sauvegarde et résumé des tâches.  
- État du Garbage Collector (GC) et capteurs associés.  
- Dernière tâche : type, état, message et durée.

<details>
  <summary>🗄️ Vue d’ensemble du Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Serveur PBS</summary>
  <p align="center">
    <img src="../../img/pbs/pbs_server.png" alt="Serveur PBS" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Détails des Tâches</summary>
  <p align="center">
    <img src="../../img/pbs/task.png" alt="Tâche PBS" width="600">
  </p>
</details>

<details>
  <summary>🗄️ État du Garbage Collector</summary>
  <p align="center">
    <img src="../../img/pbs/gc_status_attr.png" alt="État GC" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Maintenance du Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Maintenance Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Résumé de la Dernière Tâche</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Dernière Tâche" width="600">
  </p>
</details>

---

## Actions de contrôle PBS :

- Exécuter **Garbage Collector (GC)**  
- Exécuter **Prune**  
- Exécuter **Verify**  
- Exécuter **Sync**  

<details>
  <summary>🗄️ Maintenance du Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Maintenance Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Dernière Tâche</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Dernière Tâche" width="600">
  </p>
</details>

---

### 🎛️ Actions de Contrôle (PVE & PBS)

**Contrôles du nœud :**

- Éteindre le nœud  
- Redémarrer le nœud  

**Contrôles des machines virtuelles (QEMU) :**

- Démarrer, Arrêter, Éteindre, Redémarrer, Reset  
- Pause, Reprise, Hibernation  

**Contrôles des conteneurs (LXC) :**

- Démarrer, Arrêter, Éteindre, Redémarrer  

**Contrôles PBS :**

- GC, Prune, Verify, Sync (par datastore)

---

### 🎨 Organisation Visuelle et Nommage

- Les capteurs sont automatiquement regroupés en appareils logiques :
  1. Nœud  
  2. Disques physiques  
  3. Machines virtuelles  
  4. Conteneurs  
  5. Stockages / Datastores  
  6. Serveur PBS et tâches  

- Nommage cohérent et clair pour garder les dashboards lisibles et évolutifs.

---

## 🧩 Installation

### 🔹 Via HACS (recommandé)

1. Ouvre **HACS → Intégrations**  
2. Clique sur les trois points (⋮) → **Custom repositories**  
3. Ajoute ce dépôt :  
   - URL : `https://github.com/Javisen/proxmox_sensors`  
   - Catégorie : **Integration**  
4. Recherche **“Proxmox Extended Sensors”** dans HACS et installe‑le  
5. Redémarre Home Assistant  
6. Va dans **Paramètres → Appareils & Services → Ajouter une intégration** et cherche **Proxmox Extended Sensors**

### 🔹 Installation manuelle

1. Copie le dossier `custom_components/proxmox_sensors` dans :  
   - `/config/custom_components/proxmox_sensors`  
2. Redémarre Home Assistant  
3. Ajoute l’intégration depuis **Paramètres → Appareils & Services**

---

## 🧭 Guide Visuel de Configuration

Ci‑dessous, un guide visuel complet du processus de configuration, incluant les méthodes de connexion, la sélection des ressources et les étapes d’installation.

<details>
  <summary>🪪 Connexion au Serveur</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Connexion Proxmox" width="600">
  </p>
  > Pas besoin de saisir "http://" ou "https://". Nous le faisons automatiquement.
</details>

<details>
  <summary>🪪 Connexion avec Nom d’utilisateur et Mot de passe (PVE uniquement)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Connexion Proxmox" width="600">
  </p>
  > Assure‑toi d’utiliser le bon realm (`pam` ou `pve`).
</details>

<details> 
  <summary>🪪 Connexion avec Utilisateur et Token (PVE et PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Connexion Proxmox" width="600">
  </p>
  **Dans le champ Token_id, tu dois uniquement entrer le nom du token.**
</details>

<details>
  <summary>⚙️ Sélection des Ressources</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Sélection des Ressources" width="600">
  </p>
  *Note : sélectionne les CTs, VMs et Stockages que tu veux ajouter, ainsi que les options correspondantes.*
</details>

---

**Si tu apprécies cette intégration ou la trouves utile, pense à laisser une ⭐ sur GitHub.**  
**Cela aide à la visibilité, motive le développement et soutient les futures fonctionnalités.**

## 🤝 Contributions & Communauté

Les contributions sont les bienvenues ! Tu peux ouvrir des issues ou des pull requests.  
**[Voir le dépôt GitHub](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Maintenu par Javisen – Licence MIT</i></p>
