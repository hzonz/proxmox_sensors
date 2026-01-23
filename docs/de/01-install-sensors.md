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

**Fertig! Sobald der Befehl `sensors` Daten im Terminal anzeigt, kann deine Home‑Assistant‑Integration diese automatisch über die Proxmox‑API auslesen.**
