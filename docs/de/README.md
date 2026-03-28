# 📚 Dokumentation und Anleitungen

Diese Anleitungen decken die notwendigen Schritte ab, um die Integration korrekt zu konfigurieren und alle ihre Funktionen zu nutzen.

---

## 🌡️ [01. Hardware-Sensor-Konfiguration](01-install-sensors.md)
So installierst und konfigurierst du **lm-sensors** auf deinem Proxmox-Knoten, um Temperatur- und Lüfterüberwachung zu aktivieren.

---

## 🔑 [02. Proxmox-Konfiguration](02-proxmox-config.md)
So erstellst du einen sicheren **Benutzer** und **API-Token** in Proxmox (PVE und PBS) mit den minimal erforderlichen Berechtigungen.

---

## ⚙️ [03. Anmeldung der Integration (PVE und PBS)](03-login-pve-pbs.md)
Schritt-für-Schritt-Anleitung zum Verbinden der Integration mit deinen Servern von Home Assistant aus.

---

## ❓ [04. Häufig gestellte Fragen und Fehlerbehebung](04-faq.md)
Häufige Probleme, typische Fragen und deren Lösungen.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Einführung

**Proxmox Extended Sensors ist eine Integration für Home Assistant, die entwickelt wurde, um erweiterte Überwachung und vollständige Kontrolle über Proxmox VE und Proxmox Backup Server (PBS) zu bieten.**

Im Gegensatz zu rein metrikbasierten Lösungen führt diese Integration einen **erkenntnisorientierten** Ansatz ein, der es dir ermöglicht, nicht nur zu verstehen, was im System passiert, sondern auch, wie es tatsächlich funktioniert.

Sie bietet vollständige Transparenz über die Infrastruktur und fügt direkte Steuerungsmöglichkeiten für Knoten, virtuelle Maschinen, Container, Speicher und Backup-Dienste hinzu.

---

## 🧠 System Insight (Neu in V3)

Version 3 führt Sensoren ein, die technische Metriken in interpretierbare Informationen verwandeln:

- **Node Score** → globale Bewertung des Knotenzustands  
- **Load Average (1m / 5m / 15m)** → tatsächliche Systemlast  
- **IO Wait** → Erkennung von Festplattenbelastung  
- **Node Stress** → Identifizierung von Stresssituationen  
- **Disk Overload** → Erkennung von Speichersättigung  
- **Pro-Kern CPU-Auslastung** (Knoten, VM und Container)

Diese Sensoren ermöglichen es, Engpässe zu erkennen, Probleme vorherzusehen und intelligentere Automatisierungen zu erstellen.

---

## 🔍 Hauptfunktionen

- Vollständige Überwachung von:
  - Knoten
  - Virtuellen Maschinen (QEMU)
  - Containern (LXC)
  - Festplatten und Speicher
  - Proxmox Backup Server (PBS)

- Erweiterte System- und Infrastruktursensoren  
- Steuerungsaktionen von Home Assistant aus  
- Integrierte Backup-Dienste  
- Vollständige PBS-Kompatibilität (einschließlich Deduplizierung)  
- Sichere tokenbasierte Authentifizierung  
- Saubere und konsistente Entitätsstruktur  
- Optimierte Aktualisierungen und geringer Ressourcenverbrauch  

---

## 🧩 Unterstützte Versionen

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x oder neuer  

---

## 📑 Inhaltsverzeichnis

- [Hauptfunktionen](#-hauptfunktionen-v300)
- [Knotenstatus und -leistung](#-knotenstatus-und-leistung)
- [Festplatten und SMART](#-festplatten-und-smart)
- [Virtuelle Maschinen (QEMU)](#-virtuelle-maschinen-qemu)
- [Container (LXC)](#-container-lxc)
- [Backup-Dienste](#-backup-dienste-vms-und-cts)
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)
- [Steuerungsaktionen (PVE und PBS)](#-steuerungsaktionen-pve-und-pbs)
- [Installation](#-installation)
- [Visuelle Konfigurationsanleitung](#-visuelle-konfigurationsanleitung)
- [Beiträge](#-beiträge-und-community)

---

## 🔥 Hauptfunktionen (v3.0.0)

### ⚙️ Verbesserte Konfiguration

- Automatische Knotenerkennung  
- Optionale manuelle Auswahl  
- Einfachere und geführte Einrichtung  

---

### 🌡️ Erweiterte Hardware-Überwachung

- Echtzeit-Temperaturen (CPU, VRM, Chipsatz, Festplatten)  
- Lüfter- und Spannungssensoren  
- Intelligente Filterung gültiger Sensoren  
- Einheitliche Temperatursensoren (CPU + NVMe)  

> Erfordert `lm-sensors` auf dem Proxmox-Host

---

### 🧠 Knotenstatus und -leistung

- CPU, RAM, Betriebszeit, Kernel und PVE-Version  
- Netzwerküberwachung (RX/TX)  
- Aufgaben und Systemstatus  
- Erweiterte Last- und Leistungsmetriken  

---

### 💾 Festplatten und SMART

- Sensoren gruppiert nach physischer Festplatte  
- Gesamt-/genutzter Speicherplatz und erweiterte Metriken  
- SMART-Attribute (HDD, SSD, NVMe)  
- Temperaturen nach Festplattentyp  

---

### 🖥️ Virtuelle Maschinen (QEMU)

- Status, CPU, Arbeitsspeicher und Festplatte  
- Netzwerk RX/TX  
- Grundlegende Informationen und Betriebszeit  
- Pro-Kern CPU-Auslastung  

---

### 📦 Container (LXC)

- Status, CPU, Arbeitsspeicher und Festplatte  
- Netzwerk RX/TX  
- Grundlegende Informationen und Betriebszeit  
- Pro-Kern CPU-Auslastung  

---

## 💾 Backup-Dienste (VMs und CTs)

Die Integration ermöglicht die Erstellung von Backups direkt von Home Assistant aus, vollständig kompatibel mit Proxmox VE und PBS.

### 🟦 Einzelnes Backup

- Unterstützt mehrere IDs (kommagetrennt)  
- Modi: snapshot / suspend / stop  
- Komprimierung: zstd / gzip / lzo / none  

### 🟩 Massen-Backup

- Backup aller Ressourcen eines Knotens  
- Steuerung von Parallelität und Zeitplänen  
- Ideal für Automatisierungen  

Backups werden automatisch benannt als: ```HA-{{vmid}}-{{guestname}}```


Vollständig kompatibel mit PBS, einschließlich Deduplizierung und vorhandenen Ketten.

---

## 🗄️ Proxmox Backup Server (PBS)

Erweiterte Überwachung von Datastore und Aufgaben:

- Gesamt-, freier und genutzter Speicherplatz mit Prozentangabe  
- Deduplizierungsrate  
- Status des letzten Backups  
- Fehler und Aufgabenübersicht  
- Garbage Collector-Status  
- Detaillierte Aufgabeninformationen  

---

## 🎛️ Steuerungsaktionen (PVE & PBS)

**Knoten:**
- Herunterfahren / Neustarten / Wake-on-LAN  

**Virtuelle Maschinen:**
- Start / Stopp / Herunterfahren / Neustarten / Reset  
- Pause / Fortsetzen / Ruhezustand  

**Container:**
- Start / Stopp / Herunterfahren / Neustarten  

**PBS:**
- Garbage Collector  
- Prune  
- Verify  
- Sync  

---

## 🎨 Organisation und Struktur

- Sensoren automatisch gruppiert in:
  1. Knoten  
  2. Physische Festplatten  
  3. Virtuelle Maschinen  
  4. Container  
  5. Speicher / Datastores  
  6. PBS und Aufgaben  

- Konsistente und klare Namen zur Erleichterung von Dashboards und Automatisierungen  

---

## 🧩 Installation

### 🔹 Über HACS (empfohlen)

1. Öffne **HACS → Integrationen**  
2. Füge benutzerdefiniertes Repository hinzu  
3. Suche nach **Proxmox Extended Sensors**  
4. Installiere und starte Home Assistant neu  
5. Füge die Integration über die Einstellungen hinzu  

### 🔹 Manuelle Installation

1. Kopiere nach `/config/custom_components/proxmox_sensors`  
2. Starte Home Assistant neu  
3. Füge die Integration hinzu  

---

## 🧭 Visuelle Konfigurationsanleitung

Im Folgenden findest du eine vollständige visuelle Schritt-für-Schritt-Anleitung des Konfigurationsprozesses, einschließlich Zugriffsmethoden, Ressourcenauswahl und Installationsschritten.

<details>
  <summary>🪪 Serververbindung</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Proxmox Verbindung" width="600">
  </p>
  <p align="center"><i>Es ist nicht erforderlich, "http://" oder "https://" anzugeben. Dies wird automatisch behandelt.</i></p>
</details>

<details>
  <summary>🪪 Anmeldung mit Benutzername und Passwort (nur PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Anmeldung mit Benutzername und Passwort" width="600">
  </p>
  <p align="center"><i>Stelle sicher, dass du den richtigen Realm verwendest (`pam` oder `pve`).</i></p>
</details>

<details> 
  <summary>🪪 Anmeldung mit Benutzer und Token (PVE und PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Token-Anmeldung" width="600">
  </p>
  <p align="center"><i>Im Feld Token_id musst du nur den Token-Namen eingeben.</i></p>
</details>

<details>
  <summary>🧠 Knotenauswahl (V3)</summary>
  <p align="center">
    <img src="../../img/install/node_select.png" alt="Knotenauswahl" width="600">
  </p>
  <p align="center"><i>Wähle automatisch erkannte Knoten aus oder lege manuell fest, welche einbezogen werden sollen.</i></p>
</details>

<details>
  <summary>⚙️ Ressourcenauswahl</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Ressourcenauswahl" width="600">
  </p>
  <p align="center"><i>Wähle die CTs, VMs und Speicher aus, die du einbeziehen möchtest, zusammen mit den entsprechenden Optionen.</i></p>
</details>

---

**Wenn du diese Integration nützlich findest, hinterlasse gerne einen ⭐ auf GitHub.**

---

## 🤝 Beiträge und Community

Beiträge sind willkommen. Du kannst Issues oder Pull Requests öffnen.  
Repository: https://github.com/Javisen/proxmox_sensors

---

<p align="center"><i>Gepflegt von Javisen - MIT-Lizenz</i></p>