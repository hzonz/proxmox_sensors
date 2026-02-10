# 📚 Documentatie en Handleidingen

Om een probleemloze configuratie te garanderen, volg deze stapsgewijze handleidingen:

---

## 🌡️ [01. Configuratie van Hardware‑Sensors](01-install-sensors.md)
Hoe je **lm-sensors** installeert en configureert op je Proxmox‑node om temperatuur- en ventilatorbewaking mogelijk te maken.

---

## 🔑 [02. Proxmox Configuratie](02-proxmox-config.md)
Hoe je een veilige **gebruiker** en **API‑token** aanmaakt in Proxmox (PVE en PBS) met de minimaal vereiste rechten.

---

## ⚙️ [03. Aanmelden van de Integratie (PVE en PBS)](03-login-pve-pbs.md)
Gids voor het initiële configuratieproces in Home Assistant en de verbinding met je servers.

---

## ❓ [04. Veelgestelde Vragen en Probleemoplossing](04-faq.md)
Veelvoorkomende vragen, bekende problemen en hoe je ze oplost.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Introductie

**Proxmox Extended Sensors is de meest complete, efficiënte en geavanceerde integratie voor Home Assistant, ontworpen om echte controle en diepgaande monitoring te bieden voor Proxmox VE en Proxmox Backup Server (PBS).**

Deze integratie gaat veel verder dan alleen het tonen van gegevens: ze biedt **volledige zichtbaarheid** van je infrastructuur en voegt **echte bedieningsmogelijkheden** toe, zodat je nodes, virtuele machines, containers, schijven, datastores en PBS‑taken rechtstreeks vanuit Home Assistant kunt beheren.

In tegenstelling tot andere oplossingen is Proxmox Extended Sensors gebouwd met een professionele aanpak:

- **Geavanceerde monitoring** van hardware, VMs, CTs, schijven en PBS.  
- **Volledige controle‑acties** (starten, stoppen, uitschakelen, herstarten, resetten, pauzeren, in slaapstand zetten…).  
- **Volledig geïntegreerde back‑upservices**, zowel individueel als massaal.  
- **Volledige PBS‑compatibiliteit**, inclusief deduplicatie en automatische naamgeving.  
- **Veilige token‑gebaseerde authenticatie**.  
- **Schone en georganiseerde structuur** voor entiteiten en apparaten.  
- **Minimaal resourcegebruik** dankzij geoptimaliseerde polling.

Back‑ups die vanuit Home Assistant worden gemaakt, integreren perfect met die vanuit Proxmox VE, met herkenbare namen zoals:  
**HA-{{vmid}}-{{guestname}}**  
en behouden **alle voordelen van PBS**, inclusief deduplicatie en compatibiliteit met bestaande back‑upketens.

Kortom, deze integratie verandert Home Assistant in een **volwaardig controlepaneel voor Proxmox**, met gedetailleerde monitoring, geavanceerde automatisering en volledige infrastructuurcontrole.

---

## 🧩 Ondersteunde Versies

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x of nieuwer

---

## 📑 Inhoudsopgave

- [Belangrijkste Functies](#-belangrijkste-functies-v200)  
- [Node‑status en Prestaties](#-node-status-en-prestaties)  
- [Schijven en SMART](#-schijven-en-smart)  
- [Virtuele Machines (QEMU)](#-virtuele-machines-qemu)  
- [Containers (LXC)](#-containers-lxc)  
- [Back‑upservices](#-backupservices-vms-en-cts)  
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)  
- [Bedieningsacties (PVE en PBS)](#-bedieningsacties-pve-en-pbs)  
- [Installatie](#-installatie)  
- [Visuele Configuratiegids](#-visuele-configuratiegids)  
- [Bijdragen](#-bijdragen-en-community)

---

<details>
  <summary>🖼️ Dashboard Voorbeeld</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox">
  </p>
  *Voorbeeld van een modern dashboard met **Card‑Mod** (Donkere Modus) en onze gestructureerde sensoren:*
</details>

---

## 🔥 Belangrijkste Functies (v2.0.0)

### 🌡️ Geavanceerde Hardware‑Monitoring (PVE en PBS)

- **Temperaturen in realtime:** CPU‑kernen, VRM, chipset, NVMe/SSD/HDD.  
- **Mechanische sensoren:** ventilatorsnelheden (RPM), voltages en andere moederbordsensoren.  
- **Slim filteren:** alleen entiteiten met geldige gegevens worden aangemaakt om je systeem schoon te houden.  
  > Vereist `lm-sensors` op de Proxmox‑host.

---

### 🧠 Node‑status en Prestaties

- CPU‑gebruik, I/O‑wait, load average.  
- RAM totaal/gebruikt/vrij en percentage.  
- Uptime en kernel/PVE‑versie.  
- Netwerk RX/TX‑sensoren voor node, VMs en containers.

<details>
  <summary>🔳 Node‑attributen</summary>
  <p align="center">
    <img src="../../img/pve/node_attr.png" alt="Node Attributen" width="600">
  </p>
</details>

<details>
  <summary>⭕ Node‑bediening</summary>
  <p align="center">
    <img src="../../img/pve/node_controls.png" alt="Node Bediening" width="600">
  </p>
</details>

<details>
  <summary>🌡️ CPU‑temperatuur</summary>
  <p align="center">
    <img src="../../img/pve/cpu_temp_attr.png" alt="CPU Temperatuur" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Chipset‑temperatuur</summary>
  <p align="center">
    <img src="../../img/pve/chipset_temp.png" alt="Chipset Temperatuur" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O‑Wait</summary>
  <p align="center">
    <img src="../../img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Schijven & SMART

- Fysieke schijfsensoren gegroepeerd als aparte apparaten.  
- Totale/gebruikte ruimte, slijtage‑niveau (NVMe wear level) en meer.  
- SMART‑attributen voor HDD/SSD/NVMe (indien beschikbaar).  
- Toegewijde temperatuursensoren per schijftype (SATA, NVMe, enz.).

<details>
  <summary>💾 Schijfsensoren</summary>
  <p align="center">
    <img src="../../img/pve/disks_sensors.png" alt="Schijfsensoren" width="600">
  </p>
</details>

<details>
  <summary>🩺 SMART‑attributen HDD/SSD</summary>
  <p align="center">
    <img src="../../img/pve/disk_hd_smart_attr.png" alt="SMART HDD" width="600">
  </p>
</details>

<details>
  <summary>🩺 SMART‑attributen NVMe</summary>
  <p align="center">
    <img src="../../img/pve/disk_nvme_smart_attr.png" alt="SMART NVMe" width="600">
  </p>
</details>

---

### 🖥️ Virtuele Machines (QEMU)

- Status, CPU‑gebruik, RAM gebruikt/totaal, opslag gebruikt/totaal.  
- Netwerk RX/TX per VM.  
- Uptime en basisinformatiesensoren.  
- Schone apparaatgroepering per VM in Home Assistant.

<details>
  <summary>🖥️ VM‑bediening en sensoren</summary>
  <p align="center">
    <img src="../../img/pve/vm_control.png" alt="VM Bediening" width="600">
  </p>
</details>

---

### 📦 Containers (LXC)

- Status, CPU‑gebruik, RAM gebruikt/totaal, opslag gebruikt/totaal.  
- Netwerk RX/TX per container.  
- Uptime en basisinformatiesensoren.  
- Zelfde nette apparaatstructuur als bij VMs.

<details>
  <summary>📦 Container‑bediening en sensoren</summary>
  <p align="center">
    <img src="../../img/pve/ct_control.png" alt="CT Bediening" width="600">
  </p>
</details>

---

## 💾 Back‑upservices (VMs en CTs)

De integratie bevat twee krachtige back‑upservices waarmee je **Proxmox‑back‑ups rechtstreeks vanuit Home Assistant** kunt maken, volledig compatibel met Proxmox VE en Proxmox Backup Server (PBS).
