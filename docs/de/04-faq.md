# ❓ FAQ — Häufig gestellte Fragen

Hier findest du die häufigsten Fragen und Probleme bei der Verwendung der **Proxmox Extended Sensors**‑Integration, zusammen mit schnellen Lösungen.

---

## 🔐 Ich kann mich nicht in der Integration anmelden (PVE oder PBS)

### ✔ 1. Kein `http://` oder `https://` eingeben
Gib nur die Domain oder IP ein, zum Beispiel:

192.168.1.10  
pve.meine-domain.com

---

### ✔ 2. Keinen Port eingeben
Die Integration erkennt den richtigen Port automatisch.

---

### ✔ 3. Benutzer‑ oder Token‑Berechtigungen prüfen
Der Benutzer muss folgende Rollen haben:

- PVE: `PVEAdmin`  
- PBS: `Administrator`

Die Berechtigungen müssen im Root‑Pfad `/` gesetzt werden.

---

### ✔ 4. Token muss aktiviert sein
In Proxmox → Datacenter → Permissions → API Tokens  
Muss **Enabled: Yes** angezeigt werden.

---

## 🔑 „Permission denied“, obwohl der Token korrekt ist

Häufige Ursachen:

### ✔ 1. Der Token hat keine Berechtigungen im Root‑Pfad `/`
Berechtigungen müssen in `/ (root)` gesetzt werden,  
nicht auf einem einzelnen Node.

### ✔ 2. Der Token gehört zu einem Benutzer ohne Berechtigungen
Der Benutzer selbst muss die Rolle `PVEAdmin` oder `Administrator` besitzen.

---

## 🌐 Die Integration erkennt mein Tuxis PBS nicht

Das ist normal.

Tuxis‑PBS‑Server geben **keine internen Systemmetriken** über die API frei:

- Datastore‑Speicher  
- Festplattennutzung  
- RRD‑Statistiken  
- Hardware‑Informationen  
- Temperatur  
- SMART  
- CPU/RAM  

Das ist kein Fehler der Integration.  
Tuxis blockiert diese Endpunkte absichtlich.

Die Integration erkennt Tuxis automatisch und blendet nicht verfügbare Sensoren aus.

---

## 📦 Ich sehe keine Datastore‑Speichersensoren in PBS

### ✔ Wenn dein PBS von Tuxis ist → diese Daten sind nicht verfügbar
Tuxis blockiert den Endpunkt, der den Datastore‑Status liefert.

Ohne diesen Endpunkt sind folgende Daten nicht abrufbar:

- Gesamtspeicher  
- Freier Speicher  
- Nutzungsgrad  
- Deduplizierung  
- Chunks  
- Garbage Collection  

---

## 🌡️ Keine Temperatursensoren in PVE sichtbar

### ✔ 1. `lm-sensors` muss auf dem Node installiert sein  
### ✔ 2. `sensors-detect` muss ausgeführt werden  
### ✔ 3. Die empfohlenen Module müssen geladen werden  
Beispiel:

modprobe coretemp  
modprobe nct6775  

### ✔ 4. Ein systemd‑Dienst muss erstellt werden  
Damit die Sensoren nach einem Neustart funktionieren.

---

## 🖥️ NVMe/SSD/HDD‑Sensoren werden nicht angezeigt

### ✔ 1. Das Laufwerk muss Temperaturdaten unterstützen  
Einige OEM‑Modelle liefern keine Sensorwerte.

### ✔ 2. Virtuelle NVMe‑Geräte in VMs haben keine Sensoren  
Nur echte Hardware liefert Werte.

### ✔ 3. Tuxis PBS zeigt keine Festplattensensoren  
Provider‑Einschränkung.

---

## 🧠 Meine VMs oder Container werden nicht angezeigt

### ✔ 1. Benutzerberechtigungen prüfen  
Der Benutzer muss die Rolle `PVEAdmin` haben.

### ✔ 2. Bei Clustern  
Du musst dich mit dem **Hauptnode** verbinden, nicht mit einem sekundären Node.

---

## 🔄 Die Integration aktualisiert Werte langsam

Das ist normal.

Die Integration verwendet einen internen Koordinator, um:

- API‑Überlastung zu vermeiden  
- die Node‑Last zu reduzieren  
- die Leistung zu verbessern  

Der Standard‑Intervall beträgt 10 Sekunden (konfigurierbar).

---

## 🧩 Kann ich mehrere PVE‑ und PBS‑Server gleichzeitig nutzen?

Ja.  
Die Integration unterstützt mehrere Instanzen, jede mit eigenem Token.

---

## 🔒 Sind API‑Tokens sicher?

Ja.

Die Integration:

- speichert keine Passwörter  
- verwendet ausschließlich Tokens  
- führt keine Befehle auf dem Server aus  
- ändert keine Proxmox‑Konfiguration  
- öffnet keine zusätzlichen Ports  

---

## 🧹 Wie entferne ich alte Sensoren?

Home Assistant entfernt verwaiste Entitäten automatisch.

Wenn du eine manuelle Bereinigung möchtest:

1. Integration entfernen  
2. Home Assistant neu starten  
3. Integration erneut hinzufügen  

---

## 🛠️ Wo kann ich Fehler melden?

Erstelle ein Issue auf GitHub und gib folgende Informationen an:

- HA‑Version  
- Proxmox‑Version  
- relevante Logs  
- Schritte zur Reproduktion  
- Servertyp (PVE, PBS, Tuxis usw.)  

---

# 🧾 Checkliste vor dem Erstellen eines Issues

Diese Liste löst 90% aller Probleme:

### ✔ 1. Kannst du Proxmox im Browser öffnen?  
Wenn nicht, kann die Integration es auch nicht.

### ✔ 2. Verwendest du nur Domain/IP?  
Kein `http://`, `https://` oder Ports.

### ✔ 3. Ist der API‑Token aktiviert?  
Muss **Enabled: Yes** anzeigen.

### ✔ 4. Hat der Benutzer Berechtigungen im Root‑Pfad `/`?  
Nur dort funktionieren die API‑Aufrufe.

### ✔ 5. Ist `lm-sensors` installiert und konfiguriert?  
Ohne dieses Paket gibt es keine Hardware‑Sensoren.

### ✔ 6. Ist dein PBS von Tuxis?  
Dann sind interne Metriken nicht verfügbar.

### ✔ 7. Hast du Home Assistant nach Berechtigungsänderungen neu gestartet?  
HA cached alte Berechtigungen.

### ✔ 8. Gibt es Fehler in den HA‑Logs?  
Im Bereich „Integrationen“ prüfen.

### ✔ 9. Hast du den Inkognito‑Modus getestet?  
Das HA‑Frontend cached Ressourcen sehr lange.

---

# 🚫 Bekannte Einschränkungen

Diese Einschränkungen sind keine Fehler der Integration, sondern Vorgaben von Proxmox oder dem Provider.

---

### 🔒 1. Tuxis PBS

Tuxis‑PBS‑Server geben keine folgenden Daten frei:

- Datastore‑Speicher  
- Festplattennutzung  
- Deduplizierung  
- Chunks  
- RRD‑Statistiken  
- Hardware‑Informationen  
- Temperatur  
- SMART  
- CPU/RAM  

Die Integration blendet diese Sensoren automatisch aus.

---

### 🧊 2. Hardware‑Sensoren in virtuellen Maschinen

VMs liefern keine echten Sensorwerte:

- Temperaturen  
- Lüfter  
- Spannungen  
- SMART  

Nur physische Hardware unterstützt diese Werte.

---

### 📦 3. NVMe/SSD ohne Sensoren

Einige OEM‑Modelle oder RAID‑Controller liefern keine Temperatur‑ oder SMART‑Daten.

---

### 🔐 4. Tokens ohne Berechtigungen im Root‑Pfad

Wenn Berechtigungen auf einem Node statt auf `/` gesetzt werden, blockiert Proxmox die API.

---

### 🕒 5. Aktualisierungsintervalle

Die Integration verwendet ein Mindestintervall, um API‑Überlastung zu vermeiden.  
Es ist normal, dass Werte ein paar Sekunden verzögert erscheinen.

---

### 🧩 6. Proxmox‑Cluster

Du musst dich mit dem **Hauptnode** verbinden.  
Sekundäre Nodes stellen nicht die vollständige API bereit.

---

### 🌐 7. Selbstsignierte SSL‑Zertifikate

Die Integration akzeptiert sie automatisch, aber einige Browser zeigen Warnungen an.
