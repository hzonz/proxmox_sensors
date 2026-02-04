# 🚀 Schritt 1: Installation und Konfiguration der Sensoren
**Diese Anleitung erklärt, wie der Proxmox-Knoten vorbereitet wird, damit er Hardwaredaten bereitstellt und sicherstellt, dass Temperaturwerte für Home Assistant verfügbar sind.**

## 1. Installation der Abhängigkeiten
* **Zuerst installieren wir die notwendigen Werkzeuge, um die integrierten Sensoren des Mainboards und der CPU auszulesen:**

```bash
apt update && apt install lm-sensors -y
```

## 2. Hardware-Erkennung
* **Damit das System erkennt, welche Treiber benötigt werden, führen wir den Erkennungsassistenten aus:**

```bash
sensors-detect
```

**Beantworte alle Fragen mit YES (oder drücke einfach Enter). Am Ende identifiziert das System die benötigten Module (z. B. `coretemp` für Intel-CPUs).**

## 3. Module dauerhaft aktivieren
**Damit die Sensoren nach einem Neustart automatisch geladen werden, stellt der Assistent `sensors-detect` am Ende eine wichtige Frage:**

```text
Do you want to add these lines automatically to /etc/modules? (yes/NO)
```

> [!CAUTION]
> **Du musst `yes` manuell eingeben und Enter drücken.** Wenn du nur Enter drückst, ohne etwas einzugeben, wird standardmäßig `NO` ausgewählt. In diesem Fall werden die Sensoren nach einem Neustart nicht geladen und Home Assistant erhält keine Temperaturdaten mehr.

## 4. Sofortige Überprüfung
**Um die Sensoren sofort zu aktivieren, ohne den Server neu zu starten, führe Folgendes aus:**

```bash
# Lade die erkannten Module (Beispiel für Intel)
modprobe coretemp

# Überprüfe, ob die Temperaturen angezeigt werden
sensors
```
## 🚀 Schritt 5: Installation des Sensorservers (API-Bridge)
**Da die offizielle Proxmox-API nicht alle Hardware-Daten bereitstellt, muss dieses kleine "Bridge-Skript" auf dem Proxmox-Host installiert werden.**

1. **Skript herunterladen und installieren**
Führen Sie diese Befehle im Terminal Ihres Proxmox-Servers aus:
```bash
# Skript aus dem Repository herunterladen
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Ausführungsrechte vergeben
chmod +x /usr/local/bin/pve-sensors-api.py
```

2. **Konfiguration als Systemdienst**
Damit das Skript automatisch mit dem Server startet, erstellen Sie die Dienstdatei:
```bash
cat <<EOF > /etc/systemd/system/pve-sensors.service
[Unit]
Description=PVE Sensors API
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

3. **Sofortige Aktivierung**
Aktivieren und starten Sie den Dienst mit diesen Befehlen:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
```

4. **Abschlussprüfung**
Sie können überprüfen, ob der Server läuft, indem Sie diese Adresse in Ihrem Browser öffnen (ersetzen Sie sie durch die IP Ihres Proxmox-Servers): `http://IHRE_PROXMOX_IP:9000/sensors`

Wenn Sie einen Text im JSON-Format mit den Temperaturen sehen, kann die Integration die Daten nun korrekt lesen.
---

**Fertig! Sobald der Befehl `sensors` Daten im Terminal anzeigt, kann deine Home‑Assistant‑Integration diese automatisch über die Proxmox‑API auslesen.**
