# 📚 Documentation et Guides

Pour garantir une configuration sans encombre, suivez ces guides étape par étape :

---

## 🌡️ [01. Configuration des Capteurs Matériels](01-install-sensors.md)
Comment installer et configurer **lm-sensors** sur votre nœud Proxmox pour activer la surveillance des températures et des ventilateurs.

---

## 🔑 [02. Configuration de Proxmox](02-proxmox-config.md)
Comment créer un **utilisateur** et un **Token API** sécurisé dans Proxmox (PVE & PBS) avec les permissions minimales requises.

---

## ⚙️ [03. Connexion à l'Intégration (PVE & PBS)](03-login-pve-pbs.md)
Guide du processus de configuration initiale dans Home Assistant et connexion à vos serveurs.

---

## ❓ [04. Foire Aux Questions et Dépannage](04-faq.md)
Questions courantes, problèmes connus et comment les résoudre.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---
# 🚀 Proxmox Extended Sensors

**L'intégration la plus complète, efficace et organisée pour surveiller Proxmox VE et PBS depuis Home Assistant.**

Cette intégration est conçue pour les utilisateurs avancés qui ont besoin d'un contrôle total sur leur matériel sans surcharger le serveur.
Contrairement à d'autres solutions, Proxmox Sensors Extended se concentre sur l'efficacité énergétique, l'authentification sécurisée par Tokens et une organisation visuelle impeccable.

---

## 🔥 Caractéristiques Principales

### 🌡️ Surveillance Matérielle Avancée

**Ne vous contentez pas de l'utilisation du CPU. Voyez ce qui se passe réellement "sous le capot" :**

* **Températures en temps réel :** Cœurs de CPU, VRM et unités NVMe/SSD/HDD.
* **Capteurs mécaniques :** Vitesse des ventilateurs (RPM) et tensions de la carte mère.
* **Capteurs intelligents :** Seules les entités rapportant des données valides sont créées, gardant votre système propre.

**(Note : Nécessite l'installation de lm-sensors sur l'hôte Proxmox).**

---

### 🧠 Optimisé pour la Performance

**Conçu pour le matériel aux ressources limitées :**

* **DataUpdateCoordinator :** Minimise les appels à l'API Proxmox pour éviter de saturer le processeur du serveur.
* **Silent SSL :** Vérification automatique des certificats SSL (y compris auto-signés) sans remplir vos logs d'erreurs.

---

### 🗄️ Proxmox Backup Server (PBS) Avancé

* **Mode Externe :** Connectez-vous facilement à des serveurs PBS distants en utilisant uniquement le domaine.
* **Surveillance des Tâches :** État détaillé de la dernière sauvegarde (Backup), du Garbage Collector ou de la tâche Verify.

---

### 🎨 Interface Dynamique et Organisée

* **Smart Dashboard :** Les capteurs sont automatiquement groupés par appareils :
  1. Nœud
  2. Disques physiques
  3. Machines virtuelles
  4. Conteneurs
  5. Stockages (Storages)
* **Auto-Naming :** Préfixes automatiques (ex. `pv1-cpu-temp`) pour maintenir vos tableaux de bord ordonnés de manière logique.

---

**Exemple de Dashboard**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## Capteurs Mis en Avant

## PVE

### 🖥️ Capteurs Matériels (PVE & PBS)

Températures CPU • Températures VRM • Températures NVMe/SSD/HDD
Vitesse des ventilateurs (RPM) • Tensions • Capteurs d'énergie • Entités `pvesensors`
• Température du chipset

---

### 🧠 État du Nœud

Utilisation CPU (%) • Utilisation RAM (%) • RAM utilisée/totale
Temps d'activité (uptime) • Load average • CPU I/O Wait

---

### 💾 Disques

Capacité totale • Espace utilisé (Go et %)
Niveau d'usure (NVMe) • État SMART (si disponible)

---

### 🖥️ Machines Virtuelles (QEMU)

Utilisation CPU (%) • Utilisation RAM (%) • Réseau Tx/Rx
État (allumé/éteint) • Sélection automatique/manuelle

---

### 📦 Conteneurs (LXC)

Utilisation CPU (%) • Utilisation RAM (%) • Réseau Tx/Rx
État • Sélection automatique/manuelle • et bien plus encore

---

### 🗄️ Proxmox Backup Server (PBS)

Utilisation du datastore (Go et %) • Nombre de sauvegardes
État du Garbage Collector • État de la dernière tâche de sauvegarde
• Informations complètes sur les tâches et plus
