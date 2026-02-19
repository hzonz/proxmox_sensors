# 🚀 Schritt 1: Installation und Konfiguration der Sensoren

**Diese Anleitung erklärt, wie Sie den Proxmox-Knoten so vorbereiten, dass er Hardwaredaten bereitstellt und sicherstellt, dass Temperaturwerte und Smart-Daten für Home Assistant verfügbar sind.**


## 1. Installation der Abhängigkeiten

*Damit die Integration alle Hardwaresensoren und SMART-Attribute der Festplatten lesen kann, müssen die folgenden Tools in Proxmox installiert werden:*

- **lm-sensors** → Sensoren für CPU, Mainboard, Chipsatz, VRM, Lüfter…**
- **smartmontools** → SMART-Informationen von HDD, SSD und NVMe**


```bash

apt update && apt install lm-sensors smartmontools -y

```

## 2. Hardware-Erkennung

* **Führen Sie den Erkennungs-Assistenten aus, um die erforderlichen Module zu identifizieren:**


```bash

sensors-detect

```

**Antworten Sie auf alle Fragen mit YES (oder drücken Sie Enter). Am Ende wird das System die benötigten Module identifizieren (zum Beispiel: `coretemp` für Intel-CPUs).**


## 3. Persistenz der Module

**Damit die Sensoren beim Neustart des Servers automatisch aktiviert werden, stellt Ihnen der Assistent `sensors-detect` am Ende des Prozesses eine wichtige Frage:**


`Do you want to add these lines automatically to /etc/modules? (yes/NO)`



> [!CAUTION]
> **Sie müssen manuell `yes` eingeben und Enter drücken.** Wenn Sie nur Enter drücken, ohne etwas zu schreiben, wählt das System standardmäßig `NO`. In diesem Fall werden die Sensoren nach einem Neustart nicht geladen, und Home Assistant empfängt keine Temperaturdaten mehr.



## 4. Sofortige Überprüfung

**Um die Sensoren sofort ohne Neustart zu aktivieren, führen Sie Folgendes aus:**



```bash

# Lädt die erkannten Module (Beispiel für Intel)

modprobe coretemp

# Überprüfen Sie, ob die Temperaturen angezeigt werden

sensors

```

## 🚀 Schritt 5: Installation des Sensorservers (API Bridge)
**Die offizielle Proxmox-API stellt nicht alle Hardwaresensoren bereit. Daher ist es notwendig, ein kleines Skript zu installieren, das als Brücke zwischen Proxmox und Home Assistant fungiert.**

1. **Download und Installation des Skripts**
Führen Sie diese Befehle im Terminal Ihres Proxmox-Servers aus:
```bash
# Skript aus dem Repository herunterladen
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Ausführungsrechte vergeben
chmod +x /usr/local/bin/pve-sensors-api.py
```
2. **Konfiguration als Systemdienst**
Erstellen Sie die Dienstdatei:
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

```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
```

4. **Abschließende Überprüfung**
Öffnen Sie in Ihrem Browser:
```
http://IHRE_PROXMOX_IP:9000/sensors
```

Wenn ein JSON mit Temperaturen und Sensoren erscheint, funktioniert der Server ordnungsgemäß.

## ✔ Fazit

**Sobald der Befehl "sensors" Werte zurückgibt und der Dienst "pve-sensors" aktiv ist, kann Home Assistant alle Hardwaredaten ohne zusätzliche Konfigurationen abrufen.**
