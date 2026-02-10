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

---

### 🟦 1. Einzelner Backup‑Dienst  
Erstellt ein Backup einer bestimmten VM oder eines bestimmten CT.

**Dienst:** `proxmox_sensors.create_vzdump_backup`

**Verfügbare Optionen:**

- **Node** – Wähle den Proxmox‑Knoten.  
- **Zielspeicher** – Jeder Speicher, der Backups unterstützt (local, NFS, PBS usw.).  
- **VM/CT‑ID** – ID der Maschine, die gesichert werden soll.  
- **Backup‑Modus:**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Kompression:**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

Backups, die aus Home Assistant erstellt werden, erhalten automatisch den Namen:  
**HA-{{vmid}}-{{guestname}}**

Dies stellt sicher, dass sie leicht zu identifizieren sind und gleichzeitig **vollständig kompatibel mit bestehenden Proxmox‑Backups** bleiben.

<details>
  <summary>📦 Einzelner Backup‑Dienst</summary>
  <p align="center">
    <img src="../../img/pve/single_backup.png" alt="Einzelner Backup-Dienst" width="600">
  </p>
</details>

---

### 🟩 2. Massen‑Backup‑Dienst  
Erstellt Backups von **allen VMs und/oder CTs** auf einem ausgewählten Knoten.

**Dienst:** `proxmox_sensors.backup_all`

**Verfügbare Optionen:**

- **Node** – Wähle den Knoten, der gesichert werden soll.  
- **Zielspeicher** – Jeder Speicher mit Backup‑Fähigkeit.  
- **Backup‑Modus:** snapshot / suspend / stop.  
- **Kompression:** zstd / gzip / lzo / none.  
- **Maximale gleichzeitige Backups** – Steuert parallele Ausführung.  
- **Verzögerung zwischen Backups** – Sekunden zwischen den Sicherungen.  
- **VMs einschließen** – Schalter (Ja/Nein).  
- **CTs einschließen** – Schalter (Ja/Nein).

Dieser Dienst ist ideal für geplante nächtliche Backups oder automatisierte Wartungsroutinen.

<details>
  <summary>📦 Massen‑Backup‑Dienst</summary>
  <p align="center">
    <img src="../../img/pve/massive_backups.png" alt="Massen-Backup-Dienst" width="600">
  </p>
</details>

---

### 🟧 PBS‑Kompatibilität & Deduplizierung

Backups, die über diese Dienste erstellt werden:

- Werden exakt so gespeichert wie Backups aus Proxmox VE  
- Verwenden die gleiche Namens- und Metadatenstruktur  
- Unterstützen automatisch die **PBS‑Deduplizierung**  
- Integrieren sich nahtlos in bestehende Backup‑Ketten  
- Erscheinen vollständig kompatibel im PBS‑Datastore  

Es ist keine besondere Konfiguration erforderlich — PBS verarbeitet Deduplizierung und Indexierung genauso, als wäre das Backup über die Proxmox‑GUI oder CLI erstellt worden.

---

### 🗄️ Proxmox Backup Server (PBS)

**Tiefgehende Überwachung von Datastore und Aufgaben:**

- Datastore‑Nutzung (GB und %), gesamt, genutzt und frei.  
- Deduplizierungsrate und Anzahl der Backups.  
- Zeitpunkt, Größe und Status des letzten Backups.  
- Backup‑Fehler und Aufgabenübersicht.  
- Status des Garbage Collectors (GC) und zugehörige Sensoren.  
- Letzte Aufgabe: Typ, Status, Nachricht und Dauer.

<details>
  <summary>🗄️ Datastore‑Übersicht</summary>
  <p align="center">
    <img src="../../img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ PBS‑Server</summary>
  <p align="center">
    <img src="../../img/pbs/pbs_server.png" alt="PBS Server" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Aufgaben‑Details</summary>
  <p align="center">
    <img src="../../img/pbs/task.png" alt="PBS Task" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Garbage‑Collector‑Status</summary>
  <p align="center">
    <img src="../../img/pbs/gc_status_attr.png" alt="GC Status" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Datastore‑Wartung</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Zusammenfassung der letzten Aufgabe</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Last Task" width="600">
  </p>
</details>

---

## PBS‑Steuerungsaktionen:

- **Garbage Collector (GC)** ausführen  
- **Prune** ausführen  
- **Verify** ausführen  
- **Sync** ausführen  

<details>
  <summary>🗄️ Datastore‑Wartung</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Letzte Aufgabe</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Datastore Maintenance" width="600">
  </p>
</details>

---

### 🎛️ Steuerungsaktionen (PVE & PBS)

**Node‑Steuerung:**

- Node herunterfahren  
- Node neu starten  

**VM‑Steuerung (QEMU):**

- Starten, Stoppen, Herunterfahren, Neustarten, Reset  
- Pausieren, Fortsetzen, Ruhezustand  

**Container‑Steuerung (LXC):**

- Starten, Stoppen, Herunterfahren, Neustarten  

**PBS‑Steuerung:**

- GC, Prune, Verify, Sync (pro Datastore)

---

### 🎨 Visuelle Organisation & Benennung

- Sensoren werden automatisch in logische Geräte gruppiert:
  1. Node  
  2. Physische Festplatten  
  3. Virtuelle Maschinen  
  4. Container  
  5. Storages / Datastores  
  6. PBS‑Server und Aufgaben  

- Konsistente, klare Benennung von Entitäten und Geräten für übersichtliche und skalierbare Dashboards.

---

## 🧩 Installation

### 🔹 Über HACS (empfohlen)

1. Öffne **HACS → Integrationen**.  
2. Klicke auf die drei Punkte (⋮) → **Custom repositories**.  
3. Füge dieses Repository hinzu:  
   - URL: `https://github.com/Javisen/proxmox_sensors`  
   - Kategorie: **Integration**  
4. Suche nach **“Proxmox Extended Sensors”** in HACS und installiere es.  
5. Starte Home Assistant neu.  
6. Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen** und suche **Proxmox Extended Sensors**.

### 🔹 Manuelle Installation

1. Kopiere den Ordner `custom_components/proxmox_sensors` nach:  
   - `/config/custom_components/proxmox_sensors`  
2. Starte Home Assistant neu.  
3. Füge die Integration über **Einstellungen → Geräte & Dienste** hinzu.

---

## 🧭 Visuelle Einrichtung

Nachfolgend findest du eine vollständige visuelle Anleitung zum Einrichtungsprozess, einschließlich Login‑Methoden, Ressourcenauswahl und Konfigurationsschritten.

<details>
  <summary>🪪 Server‑Verbindung</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Du musst kein "http://" oder "https://" eingeben — das erledigen wir automatisch.
</details>

<details>
  <summary>🪪 Login mit Benutzername und Passwort (nur PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Stelle sicher, dass du das richtige Realm (`pam` oder `pve`) verwendest.
</details>

<details> 
  <summary>🪪 Login mit Benutzer und Token (PVE und PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **Im Feld Token_id musst du nur den Token‑Namen eingeben.**
</details>

<details>
  <summary>⚙️ Ressourcenauswahl</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Hinweis: Wähle die CTs, VMs und Storages aus, die du hinzufügen möchtest, sowie die gewünschten Optionen.*
</details>

---

**Wenn dir diese Integration gefällt oder sie dir hilft, hinterlasse gerne ein ⭐ auf GitHub.**  
**Das verbessert die Sichtbarkeit, motiviert die Entwicklung und unterstützt zukünftige Funktionen.**

## 🤝 Beiträge & Community

Beiträge sind willkommen! Du kannst Issues oder Pull Requests erstellen.  
**[Zum GitHub‑Repository](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Maintained by Javisen – MIT‑Lizenz</i></p>

