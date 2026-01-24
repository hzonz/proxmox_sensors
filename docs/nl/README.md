# 📚 Documentatie en Handleidingen

Volg deze stapsgewijze handleidingen voor een probleemloze configuratie:

---

## 🌡️ [01. Hardware Sensoren Configureren](01-install-sensors.md)
Hoe installeer en configureer je **lm-sensors** op je Proxmox-node om monitoring van temperaturen en ventilatoren mogelijk te maken.

---

## 🔑 [02. Proxmox Configuratie](02-proxmox-config.md)
Hoe maak je een veilige **gebruiker** en **API Token** aan in Proxmox (PVE & PBS) met de minimaal vereiste machtigingen.

---

## ⚙️ [03. Inloggen op de Integratie (PVE & PBS)](03-login-pve-pbs.md)
Handleiding voor het initiële configuratieproces in Home Assistant en de verbinding met je servers.

---

## ❓ [04. Veelgestelde Vragen en Probleemoplossing](04-faq.md)
Veelvoorkomende vragen, bekende problemen en hoe je deze kunt oplossen.

---

<p align="center">
  <img src="[https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png](https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png)" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---
# 🚀 Proxmox Extended Sensors

**De meest complete, efficiënte en georganiseerde integratie om Proxmox VE en PBS te monitoren vanuit Home Assistant.**

Deze integratie is ontworpen voor gevorderde gebruikers die volledige controle over hun hardware nodig hebben zonder de server te overbelasten.
In tegenstelling tot andere oplossingen richt Proxmox Sensors Extended zich op energie-efficiëntie, veilige authenticatie via tokens en een onberispelijke visuele organisatie.

---

## 🔥 Belangrijkste Kenmerken

### 🌡️ Geavanceerde Hardware Monitoring

**Neem geen genoegen met alleen CPU-gebruik. Zie wat er echt gebeurt "onder de motorkap":**

* **Real-time temperaturen:** CPU-kernen, VRM en NVMe/SSD/HDD-schijven.
* **Mechanische sensoren:** Ventilatorsnelheid (RPM) en moederbordspanningen.
* **Slimme sensoren:** Er worden alleen entiteiten aangemaakt die geldige gegevens rapporteren, waardoor je systeem schoon blijft.

**(Let op: Vereist de installatie van lm-sensors op de Proxmox-host).**

---

### 🧠 Geoptimaliseerd voor Prestaties

**Ontworpen met hardware met beperkte middelen in gedachten:**

* **DataUpdateCoordinator:** Minimaliseert aanroepen naar de Proxmox API om verzadiging van de serverprocessor te voorkomen.
* **Silent SSL:** Automatische verificatie van SSL-certificaten (inclusief zelfondertekende) zonder je logs te vullen met fouten.

---

### 🗄️ Geavanceerde Proxmox Backup Server (PBS)

* **Externe Modus:** Maak eenvoudig verbinding met PBS-servers op afstand door alleen het domein te gebruiken.
* **Taakbewaking:** Gedetailleerde status van de laatste Backup, Garbage Collector of Verify-taak.

---

### 🎨 Dynamische en Georganiseerde Interface

* **Smart Dashboard:** Sensoren worden automatisch gegroepeerd in apparaten:
  1. Node
  2. Fysieke schijven
  3. Virtuele machines
  4. Containers
  5. Storages
* **Auto-Naming:** Automatische voorvoegsels (bijv. `pv1-cpu-temp`) om je dashboards logisch geordend te houden.

---

**Dashboard Voorbeeld**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## Uitgelichte Sensoren

## PVE

### 🖥️ Hardware Sensoren (PVE & PBS)

CPU-temperaturen • VRM-temperaturen • NVMe/SSD/HDD-temperaturen
Ventilatorsnelheid (RPM) • Spanningen • Stroomsensoren • `pvesensors` entiteiten
• Chipset temperatuur

---

### 🧠 Node Status

CPU-gebruik (%) • RAM-gebruik (%) • RAM gebruikt/totaal
Uptime • Load average • CPU I/O Wait

---

### 💾 Schijven

Totale capaciteit • Gebruikte ruimte (GB en %)
Slijtageniveau (NVMe) • SMART-status (indien beschikbaar)

---

### 🖥️ Virtuele Machines (QEMU)

CPU-gebruik (%) • RAM-gebruik (%) • Netwerk Tx/Rx
Status (aan/uit) • Automatische/handmatige selectie

---

### 📦 Containers (LXC)

CPU-gebruik (%) • RAM-gebruik (%) • Netwerk Tx/Rx
Status • Automatische/handmatige selectie • en nog veel meer

---

### 🗄️ Proxmox Backup Server (PBS)

Datastore gebruik (GB en %) • Aantal back-ups
Status van de Garbage Collector • Status van de laatste back-up taak
• Volledige taakinformatie en meer
