# ❓ FAQ — Häufig gestellte Fragen

Im Folgenden findest du die häufigsten Fragen und Probleme bei der Verwendung der Integration **Proxmox Sensors Extended**, zusammen mit schnellen Lösungen.

---

## 🔐 Ich kann mich nicht in der Integration anmelden (PVE oder PBS)

### ✔ 1. Du darfst kein `http://` oder `https://` eingeben
Gib **nur die Domain oder IP** ein, zum Beispiel:

`192.168.1.10  
pve.meine-domain.com`

---

### ✔ 2. Du darfst keinen Port angeben
Die Integration erkennt den richtigen Port automatisch.

### ✔ 3. Überprüfe die Berechtigungen des API‑Tokens
Der Benutzer muss folgende Rechte besitzen:

- **PVE:**  
  - `Sys.Audit`  
  - `VM.Audit`  
  - `Datastore.Audit`  
  - `Permissions.Modify` (nur wenn du automatische Auswahl von VMs/LXCs nutzt)

- **PBS:**  
  - `Datastore.Audit`  
  - `Datastore.Read`  
  - `Sys.Audit`

---

### ✔ 4. Stelle sicher, dass das Token aktiviert ist
In Proxmox → Datacenter → Permissions → API Tokens  
Muss **Enabled: Yes** angezeigt werden.

---

## 🔑 „Permission denied“, obwohl das Token korrekt ist

Dies liegt meist an:

### ✔ 1. Das Token hat keine Berechtigungen auf `/`
In Proxmox müssen Berechtigungen auf `/ (root)` gesetzt werden, **nicht auf einem einzelnen Node**.

### ✔ 2. Das Token gehört zu einem Benutzer ohne Berechtigungen
Der übergeordnete Benutzer muss Rechte besitzen, nicht nur das Token.

---

## 🌐 Die Integration erkennt meinen PBS von Tuxis nicht

Das ist normal.

Von Tuxis verwaltete PBS‑Instanzen erlauben **keinen Zugriff auf interne Metriken** über die API:

- Datastore‑Speicher  
- Festplattennutzung  
- RRD‑Statistiken  
- Node‑Hardware  
- Temperatur  
- SMART‑Daten  
- CPU/RAM  

Das ist **kein Fehler der Integration**:  
Tuxis blockiert diese Endpunkte absichtlich.

Die Integration erkennt automatisch, dass es sich um einen Tuxis‑PBS handelt, und blendet nicht verfügbare Sensoren aus.

---

## 📦 Ich sehe keine Datastore‑Speichersensoren in PBS

### ✔ Wenn dein PBS von Tuxis ist → **nicht verfügbar**
Aus Sicherheitsgründen blockiert Tuxis den Endpunkt:  
`/api2/json/admin/datastore/<name>/status`

Ohne diesen Endpunkt können folgende Daten nicht abgerufen werden:

- Gesamtspeicher  
- freier Speicher  
- Nutzungsprozentsatz  
- Deduplizierung  
- Chunks  
- GC  

---

## 🌡️ Keine Temperatursensoren in PVE sichtbar

### ✔ 1. Du musst `lm-sensors` auf dem Node installieren  
Vollständige Anleitung: 01-install-sensors.md

### ✔ 2. Du musst `sensors-detect` ausführen  
Und alle sicheren Optionen akzeptieren.

### ✔ 3. Du musst die empfohlenen Module laden  
Beispiel:

```bash
modprobe coretemp
modprobe nct6775
```

### ✔ 4. Du musst einen systemd‑Dienst erstellen  
Damit die Sensoren nach einem Neustart funktionieren.

---

## 🖥️ Keine NVMe/SSD/HDD‑Sensors sichtbar

### ✔ 1. Das Laufwerk muss Temperatursensoren unterstützen  
Einige OEM‑Modelle stellen keine Sensoren bereit.

### ✔ 2. Virtuelle NVMe‑Laufwerke (in VMs) haben keine Sensoren  
Nur echte Hardware unterstützt dies.

### ✔ 3. In Tuxis‑PBS werden keine Festplattensensoren bereitgestellt  
Einschränkung des Anbieters.

---

## 🧠 Meine VMs oder Container erscheinen nicht

### ✔ 1. Überprüfe die Token‑Berechtigungen  
Es muss `VM.Audit` enthalten sein.

### ✔ 2. Wenn du automatische Auswahl nutzt  
Die Integration benötigt: `Permissions.Modify`

### ✔ 3. Wenn du ein Cluster verwendest  
Du musst dich mit dem **Hauptnode** verbinden, nicht mit einem sekundären Node.

---

## 🔄 Die Integration aktualisiert Werte langsam

Das ist normal.

Die Integration verwendet den `DataUpdateCoordinator`, um:

* die API nicht zu überlasten  
* die Last auf dem Node zu reduzieren  
* die Leistung zu verbessern  

**Das Standardintervall beträgt 10 Sekunden und ist konfigurierbar.**

---

## 🧩 Kann ich mehrere PVE‑ und PBS‑Instanzen gleichzeitig verwenden?

### Ja.
Die Integration erlaubt das Hinzufügen mehrerer Instanzen, jede mit ihrem eigenen Token.

---

## 🔒 Ist es sicher, API‑Tokens zu verwenden?
### Ja.

Die Integration:

* speichert keine Passwörter  
* verwendet nur Tokens mit minimalen Berechtigungen  
* führt keine Befehle auf dem Server aus  
* ändert keine Proxmox‑Konfiguration  
* öffnet keine zusätzlichen Ports  

---

## 🧹 Wie entferne ich alte Sensoren?
**Home Assistant entfernt verwaiste Entitäten automatisch.**

**Wenn du die Bereinigung erzwingen möchtest:**

* Entferne die Integration  
* Starte Home Assistant neu  
* Füge die Integration erneut hinzu  

---

## 🛠️ Wo kann ich Fehler melden?
**Du kannst ein Issue auf GitHub eröffnen mit:**

* HA‑Version  
* Proxmox‑Version  
* relevanten Logs  
* Schritten zur Reproduktion  
* Servertyp (PVE, PBS, Tuxis usw.)

---

# 🧾 Checkliste vor dem Erstellen eines Issues

Bevor du ein Problem meldest, überprüfe diese kurze Liste.  
90 % aller Fehler werden hier gelöst:

### ✔ 1. Kannst du Proxmox im Browser öffnen?
Wenn du die PVE/PBS‑Weboberfläche nicht erreichst, kann die Integration es auch nicht.

### ✔ 2. Verwendest du nur Domain/IP?
Kein `http://`, `https://` und keine Ports eingeben.

### ✔ 3. Ist das API‑Token aktiv?
In Proxmox → Datacenter → Permissions → API Tokens  
Muss **Enabled: Yes** stehen.

### ✔ 4. Hat der Benutzer Berechtigungen auf `/`?
Berechtigungen müssen auf `/ (root)` gesetzt werden, nicht auf einem einzelnen Node.

### ✔ 5. Hast du `lm-sensors` auf PVE installiert und konfiguriert?
Ohne diese Pakete erscheinen keine Hardware‑Sensoren.

### ✔ 6. Ist dein PBS von Tuxis?
Falls ja, beachte, dass **keine internen Metriken** verfügbar sind (Speicher, Hardware, RRD).

### ✔ 7. Hast du Home Assistant nach Berechtigungsänderungen neu gestartet?
HA cached alte Berechtigungen.

### ✔ 8. Gibt es Fehler in den Home‑Assistant‑Logs?
Gehe zu:  
**Einstellungen → Protokolle → Integrationen**

### ✔ 9. Hast du es im Inkognito‑Modus getestet?
Das HA‑Frontend cached Ressourcen wochenlang.

---

# 🚫 Bekannte Einschränkungen

Diese Einschränkungen sind keine Fehler der Integration, sondern Vorgaben von Proxmox oder dem Anbieter:

### 🔒 1. PBS von Tuxis
Von Tuxis verwaltete PBS‑Server erlauben **keinen Zugriff auf:**

- Datastore‑Speicher  
- Festplattennutzung  
- Deduplizierung  
- Chunks  
- RRD‑Statistiken  
- Node‑Hardware  
- Temperatur  
- SMART  
- CPU/RAM  

Die Integration erkennt diese Einschränkung automatisch und blendet nicht verfügbare Sensoren aus.

---

### 🧊 2. Hardware‑Sensoren in virtuellen Maschinen
VMs stellen **keine echten Sensoren** bereit:

- Temperaturen  
- Lüfter  
- Spannungen  
- SMART  

Diese funktionieren nur auf echter Hardware.

---

### 📦 3. NVMe/SSD‑Laufwerke ohne Sensoren
Einige OEM‑Modelle oder RAID‑Controller **stellen keine Temperatur‑ oder SMART‑Daten** bereit.

---

### 🔐 4. Tokens ohne Berechtigungen auf `/`
Wenn Berechtigungen auf einen Node statt auf die Wurzel gesetzt werden, blockiert Proxmox die API.

---

### 🕒 5. Aktualisierungsintervalle
Um die API nicht zu überlasten, verwendet die Integration ein Mindestintervall.  
Es ist kein Fehler, wenn Werte ein paar Sekunden verzögert erscheinen.

---

### 🧩 6. Proxmox‑Cluster
Du musst dich mit dem **Hauptnode** verbinden.  
Sekundäre Nodes stellen nicht die vollständige API bereit.

---

### 🌐 7. Selbstsignierte SSL‑Zertifikate
Die Integration akzeptiert sie automatisch, aber einige Browser zeigen Warnungen an.

---
