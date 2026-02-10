# 📚 Dokumentation und Anleitungen

Um eine reibungslose Einrichtung sicherzustellen, folge bitte diesen Schritt‑für‑Schritt‑Anleitungen:

---

## 🌡️ [01. Hardware‑Sensoren konfigurieren](01-install-sensors.md)
Wie man **lm-sensors** auf deinem Proxmox‑Knoten installiert und konfiguriert, um Temperatur‑ und Lüfterüberwachung zu aktivieren.

---

## 🔑 [02. Proxmox konfigurieren](02-proxmox-config.md)
Wie man einen sicheren **Benutzer** und einen **API‑Token** in Proxmox (PVE und PBS) mit den minimal erforderlichen Berechtigungen erstellt.

---

## ⚙️ [03. Anmeldung der Integration (PVE und PBS)](03-login-pve-pbs.md)
Anleitung durch den Ersteinrichtungsprozess in Home Assistant und die Verbindung zu deinen Servern.

---

## ❓ [04. Häufige Fragen und Fehlerbehebung](04-faq.md)
Häufige Fragen, bekannte Probleme und wie man sie löst.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Einführung

**Proxmox Extended Sensors ist die vollständigste, effizienteste und fortschrittlichste Integration für Home Assistant, entwickelt, um echte Kontrolle und tiefgehendes Monitoring für Proxmox VE und Proxmox Backup Server (PBS) bereitzustellen.**

Diese Integration geht weit über die einfache Anzeige von Daten hinaus: Sie bietet **vollständige Sichtbarkeit** deiner Infrastruktur und fügt **echte Steuerungsfunktionen** hinzu, sodass du Knoten, virtuelle Maschinen, Container, Festplatten, Datastores und PBS‑Aufgaben direkt aus Home Assistant verwalten kannst.

Im Gegensatz zu anderen Lösungen wurde Proxmox Extended Sensors mit einem professionellen Ansatz entwickelt:

- **Erweitertes Monitoring** von Hardware, VMs, CTs, Festplatten und PBS.
- **Umfassende Steuerungsaktionen** (Starten, Stoppen, Herunterfahren, Neustarten, Reset, Pausieren, Ruhezustand…).
- **Vollständig integrierte Backup‑Dienste**, sowohl einzelne als auch Massen‑Backups.
- **Volle PBS‑Kompatibilität**, einschließlich Deduplication und automatischer Benennung.
- **Sichere Token‑basierte Authentifizierung**.
- **Saubere und organisierte Struktur** für Entitäten und Geräte.
- **Minimaler Ressourcenverbrauch** dank optimiertem Polling.

Backups, die aus Home Assistant erstellt werden, integrieren sich perfekt mit denen, die aus Proxmox VE erstellt wurden, verwenden identifizierbare Namen wie:  
**HA-{{vmid}}-{{guestname}}**  
und behalten **alle Vorteile von PBS**, einschließlich Deduplication und Kompatibilität mit bestehenden Backup‑Ketten.

Kurz gesagt verwandelt diese Integration Home Assistant in ein **vollwertiges Kontrollzentrum für Proxmox**, das detailliertes Monitoring, erweiterte Automatisierung und vollständige Infrastrukturkontrolle kombiniert.

---

## 🧩 Unterstützte Versionen

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x oder neuer

---

## 📑 Inhaltsverzeichnis

- [Wichtige Funktionen](#-wichtige-funktionen-v200)
- [Knotenstatus und Leistung](#-knotenstatus-und-leistung)
- [Festplatten und SMART](#-festplatten-und-smart)
- [Virtuelle Maschinen (QEMU)](#-virtuelle-maschinen-qemu)
- [Container (LXC)](#-container-lxc)
- [Backup‑Dienste](#-backup-dienste-vms-und-cts)
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)
- [Steuerungsaktionen (PVE und PBS)](#-steuerungsaktionen-pve-und-pbs)
- [Installation](#-installation)
- [Visuelle Einrichtung](#-visuelle-einrichtung)
- [Beiträge](#-beiträge-und-community)

---

<details>
  <summary>🖼️ Dashboard‑Vorschau</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox">
  </p>
  *Beispiel eines modernen Dashboards mit **Card‑Mod** (Dark Mode) und unseren strukturierten Sensoren:*
</details>

---

## 🔥 Wichtige Funktionen (v2.0.0)

### 🌡️ Erweitertes Hardware‑Monitoring (PVE und PBS)

- **Temperaturen in Echtzeit:** CPU‑Kerne, VRM, Chipsatz, NVMe/SSD/HDD.  
- **Mechanische Sensoren:** Lüftergeschwindigkeiten (RPM), Spannungen und weitere Board‑Sensoren.  
- **Intelligentes Filtern:** Es werden nur Entitäten erstellt, die gültige Daten liefern, um dein System sauber zu halten.  
  > Erfordert `lm-sensors` auf dem Proxmox‑Host.

---

### 🧠 Knotenstatus und Leistung

- CPU‑Auslastung, I/O‑Wait, Load Average.  
- RAM gesamt/genutzt/frei und Prozentwerte.  
- Uptime sowie Kernel‑/PVE‑Version.  
- Netzwerk‑RX/TX‑Sensoren für Knoten, VMs und Container.

<details>
  <summary>🔳 Knotenattribute</summary>
  <p align="center">
    <img src="../../img/pve/node_attr.png" alt="Knotenattribute" width="600">
  </p>
</details>

<details>
  <summary>⭕ Knotensteuerung</summary>
  <p align="center">
    <img src="../../img/pve/node_controls.png" alt="Knotensteuerung" width="600">
  </p>
</details>

<details>
  <summary>🌡️ CPU‑Temperatur</summary>
  <p align="center">
    <img src="../../img/pve/cpu_temp_attr.png" alt="CPU Temperatur" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Chipsatz‑Temperatur</summary>
  <p align="center">
    <img src="../../img/pve/chipset_temp.png" alt="Chipsatz Temperatur" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O‑Wait</summary>
  <p align="center">
    <img src="../../img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Festplatten & SMART

- Physische Festplattensensoren als eigene Geräte gruppiert.  
- Gesamtspeicher/genutzt, Verschleißlevel (NVMe Wear Level) und mehr.  
- SMART‑Attribute für HDD/SSD/NVMe (falls verfügbar).  
- Dedizierte Temperatursensoren je nach Festplattentyp (SATA, NVMe usw.).

<details>
  <summary>💾 Festplattensensoren</summary>
  <p align="center">
    <img src="../../img/pve/disks_sensors.png" alt="Festplattensensoren" width="600">
  </p>
</details>

<details>
  <summary>🩺 SMART‑Attribute HDD/SSD</summary>
  <p align="center">
    <img src="../../img/pve/disk_hd_smart_attr.png" alt="SMART HDD" width="600">
  </p>
</details>

<details>
  <summary>🩺 SMART‑Attribute NVMe</summary>
  <p align="center">
    <img src="../../img/pve/disk_nvme_smart_attr.png" alt="SMART NVMe" width="600">
  </p>
</details>

---

### 🖥️ Virtuelle Maschinen (QEMU)

- Status, CPU‑Auslastung, RAM genutzt/gesamt, Speicher genutzt/gesamt.  
- Netzwerk RX/TX pro VM.  
- Uptime und grundlegende Informationssensoren.  
- Saubere Gerätegruppierung pro VM in Home Assistant.

<details>
  <summary>🖥️ VM‑Steuerung und Sensoren</summary>
  <p align="center">
    <img src="../../img/pve/vm_control.png" alt="VM Steuerung" width="600">
  </p>
</details>

---

### 📦 Container (LXC)

- Status, CPU‑Auslastung, RAM genutzt/gesamt, Speicher genutzt/gesamt.  
- Netzwerk RX/TX pro Container.  
- Uptime und grundlegende Informationssensoren.  
- Gleiche saubere Geräteorganisation wie bei VMs.

<details>
  <summary>📦 CT‑Steuerung und Sensoren</summary>
  <p align="center">
    <img src="../../img/pve/ct_control.png" alt="CT Steuerung" width="600">
  </p>
</details>

---

## 💾 Backup‑Dienste (VMs und CTs)

Die Integration enthält zwei leistungsstarke Backup‑Dienste, mit denen du **Proxmox‑Backups direkt aus Home Assistant** erstellen kannst – vollständig kompatibel mit Proxmox VE und Proxmox Backup Server (PBS).

