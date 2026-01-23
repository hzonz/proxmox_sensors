# 📚 Dokumentation und Anleitungen

Um eine reibungslose Konfiguration zu gewährleisten, folge bitte diesen Schritt-für-Schritt-Anleitungen:

---

## 🌡️ [01. Konfiguration der Hardware-Sensoren](01-install-sensors.md)
Anleitung zur Installation und Konfiguration von **lm-sensors** auf deinem Proxmox-Knoten, um die Überwachung von Temperaturen und Lüftern zu aktivieren.

---

## 🔑 [02. Proxmox-Konfiguration](02-proxmox-config.md)
So erstellst du einen sicheren **Benutzer** und **API-Token** in Proxmox (PVE & PBS) mit den erforderlichen Mindestberechtigungen.

---

## ⚙️ [03. Anmeldung in der Integration (PVE & PBS)](03-login-pve-pbs.md)
Leitfaden für den Ersteinrichtungsprozess in Home Assistant und die Verbindung mit deinen Servern.

---

## ❓ [04. Häufig gestellte Fragen und Fehlerbehebung](04-faq.md)
Häufige Fragen, bekannte Probleme und deren Lösungen.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---
# 🚀 Proxmox Extended Sensors

**Die vollständigste, effizienteste und am besten organisierte Integration zur Überwachung von Proxmox VE und PBS über Home Assistant.**

Diese Integration wurde für fortgeschrittene Benutzer entwickelt, die die volle Kontrolle über ihre Hardware benötigen, ohne den Server zu überlasten.
Im Gegensatz zu anderen Lösungen konzentriert sich Proxmox Sensors Extended auf Energieeffizienz, sichere Authentifizierung mittels Token und eine tadellose visuelle Organisation.

---

## 🔥 Hauptmerkmale

### 🌡️ Erweitertes Hardware-Monitoring

**Gib dich nicht nur mit der CPU-Auslastung zufrieden. Sieh nach, was wirklich „unter der Haube“ passiert:**

* **Echtzeit-Temperaturen:** CPU-Kerne, VRM und NVMe/SSD/HDD-Laufwerke.
* **Mechanische Sensoren:** Lüfterdrehzahl (RPM) und Mainboard-Spannungen.
* **Intelligente Sensoren:** Es werden nur Entitäten erstellt, die valide Daten liefern, um dein System sauber zu halten.

**(Hinweis: Erfordert die Installation von lm-sensors auf dem Proxmox-Host).**

---

### 🧠 Optimiert für Leistung

**Entwickelt für Hardware mit begrenzten Ressourcen:**

* **DataUpdateCoordinator:** Minimiert die Aufrufe an die Proxmox-API, um eine Sättigung des Serverprozessors zu vermeiden.
* **Silent SSL:** Automatische Überprüfung von SSL-Zertifikaten (einschließlich selbstsignierter), ohne deine Logs mit Fehlern zu füllen.

---

### 🗄️ Erweiterter Proxmox Backup Server (PBS)

* **Externer Modus:** Verbinde dich einfach mit entfernten PBS-Servern unter Verwendung der Domain.
* **Aufgaben-Überwachung:** Detaillierter Status des letzten Backups, Garbage Collectors oder der Verify-Aufgabe.

---

### 🎨 Dynamische und organisierte Benutzeroberfläche

* **Smart Dashboard:** Sensoren werden automatisch in Geräten gruppiert:
  1. Knoten (Node)
  2. Physische Datenträger
  3. Virtuelle Maschinen
  4. Container (LXC)
  5. Speicher (Storages)
* **Auto-Naming:** Automatische Präfixe (z. B. `pv1-cpu-temp`), um deine Dashboards logisch geordnet zu halten.

---

**Dashboard-Beispiel**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## Highlights der Sensoren

## PVE

### 🖥️ Hardware-Sensoren (PVE & PBS)

CPU-Temperaturen • VRM-Temperaturen • NVMe/SSD/HDD-Temperaturen
Lüftergeschwindigkeiten (RPM) • Spannungen • Energiesensoren • `pvesensors` Entitäten
• Chipsatz-Temperatur

---

### 🧠 Knoten-Status (Node)

CPU-Auslastung (%) • RAM-Auslastung (%) • RAM verwendet/gesamt
Betriebszeit (Uptime) • Load average • CPU I/O Wait

---

### 💾 Datenträger

Gesamtkapazität • Belegter Speicher (GB und %)
Verschleißgrad (NVMe Wearout) • SMART-Status (falls verfügbar)

---

### 🖥️ Virtuelle Maschinen (QEMU)

CPU-Auslastung (%) • RAM-Auslastung (%) • Netzwerk Tx/Rx
Status (An/Aus) • Automatische/Manuelle Auswahl

---

### 📦 Container (LXC)

CPU-Auslastung (%) • RAM-Auslastung (%) • Netzwerk Tx/Rx
Status • Automatische/Manuelle Auswahl • und viele mehr

---

### 🗄️ Proxmox Backup Server (PBS)

Datastore-Nutzung (GB und %) • Anzahl der Backups
Status des Garbage Collectors • Status der letzten Backup-Aufgabe
• Vollständige Aufgaben-Informationen und mehr
