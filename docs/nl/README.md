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

---

### 🟦 1. Individuele Back-upservice  
Maakt een back-up van een specifieke VM of CT.

**Service:** `proxmox_sensors.create_vzdump_backup`

**Beschikbare opties:**

- **Node** – Selecteer de Proxmox‑node.  
- **Doelopslag** – Elke opslag die back-ups ondersteunt (local, NFS, PBS, enz.).  
- **VM/CT‑ID** – ID van de machine waarvan een back-up moet worden gemaakt.  
- **Back-upmodus:**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Compressie:**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

Back-ups die vanuit Home Assistant worden gemaakt, krijgen automatisch de naam:  
**HA-{{vmid}}-{{guestname}}**

Dit zorgt ervoor dat ze gemakkelijk te herkennen zijn en **volledig compatibel blijven met bestaande Proxmox‑back-ups**.

<details>
  <summary>📦 Individuele Back-upservice</summary>
  <p align="center">
    <img src="../../img/pve/single_backup.png" alt="Individuele Back-upservice" width="600">
  </p>
</details>

---

### 🟩 2. Massale Back-upservice  
Maakt back-ups van **alle VMs en/of CTs** op een geselecteerde node.

**Service:** `proxmox_sensors.backup_all`

**Beschikbare opties:**

- **Node** – Selecteer de node waarvan een back-up moet worden gemaakt.  
- **Doelopslag** – Elke opslag die back-ups ondersteunt.  
- **Back-upmodus:** snapshot / suspend / stop.  
- **Compressie:** zstd / gzip / lzo / none.  
- **Maximaal aantal gelijktijdige back-ups** – Bepaalt parallelle uitvoering.  
- **Vertraging tussen back-ups** – Seconden tussen elke back-up.  
- **VMs opnemen** – Schakelaar (Ja/Nee).  
- **CTs opnemen** – Schakelaar (Ja/Nee).

Deze service is ideaal voor geplande nachtelijke back-ups of geautomatiseerde onderhoudsroutines.

<details>
  <summary>📦 Massale Back-upservice</summary>
  <p align="center">
    <img src="../../img/pve/massive_backups.png" alt="Massale Back-upservice" width="600">
  </p>
</details>

---

### 🟧 PBS‑compatibiliteit & Deduplicatie

Back-ups die via deze services worden gemaakt:

- Worden exact opgeslagen zoals back-ups vanuit Proxmox VE  
- Gebruiken dezelfde naamgevings- en metadata‑structuur  
- Ondersteunen automatisch **PBS‑deduplicatie**  
- Integreren naadloos met bestaande back-upketens  
- Verschijnen volledig compatibel in de PBS‑datastore  

Er is geen speciale configuratie nodig — PBS verwerkt deduplicatie en indexering precies zoals wanneer de back-up via de Proxmox‑GUI of CLI wordt gemaakt.

---

### 🗄️ Proxmox Backup Server (PBS)

**Diepgaande monitoring van datastore en taken:**

- Datastoregebruik (GB en %), totaal, gebruikt en vrij.  
- Deduplicatieratio en aantal back-ups.  
- Tijdstip, grootte en status van de laatste back-up.  
- Back-upfouten en taakoverzicht.  
- Status van de Garbage Collector (GC) en gerelateerde sensoren.  
- Laatste taak: type, status, bericht en duur.

<details>
  <summary>🗄️ Datastore-overzicht</summary>
  <p align="center">
    <img src="../../img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ PBS‑server</summary>
  <p align="center">
    <img src="../../img/pbs/pbs_server.png" alt="PBS Server" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Taakdetails</summary>
  <p align="center">
    <img src="../../img/pbs/task.png" alt="PBS Taak" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Garbage Collector‑status</summary>
  <p align="center">
    <img src="../../img/pbs/gc_status_attr.png" alt="GC Status" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Datastore‑onderhoud</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Datastore Onderhoud" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Samenvatting van de laatste taak</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Laatste Taak" width="600">
  </p>
</details>

---

## PBS‑bedieningsacties:

- **Garbage Collector (GC)** uitvoeren  
- **Prune** uitvoeren  
- **Verify** uitvoeren  
- **Sync** uitvoeren  

<details>
  <summary>🗄️ Datastore‑onderhoud</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Datastore Onderhoud" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Laatste Taak</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Laatste Taak" width="600">
  </p>
</details>

---

### 🎛️ Bedieningsacties (PVE & PBS)

**Node‑bediening:**

- Node uitschakelen  
- Node herstarten  

**VM‑bediening (QEMU):**

- Starten, Stoppen, Uitschakelen, Herstarten, Reset  
- Pauzeren, Hervatten, Slaapstand  

**Container‑bediening (LXC):**

- Starten, Stoppen, Uitschakelen, Herstarten  

**PBS‑bediening:**

- GC, Prune, Verify, Sync (per datastore)

---

### 🎨 Visuele Organisatie & Naamgeving

- Sensoren worden automatisch gegroepeerd in logische apparaten:
  1. Node  
  2. Fysieke schijven  
  3. Virtuele machines  
  4. Containers  
  5. Storages / Datastores  
  6. PBS‑server en taken  

- Consistente en duidelijke naamgeving voor entiteiten en apparaten, waardoor dashboards overzichtelijk en schaalbaar blijven.

---

## 🧩 Installatie

### 🔹 Via HACS (aanbevolen)

1. Open **HACS → Integraties**  
2. Klik op de drie puntjes (⋮) → **Custom repositories**  
3. Voeg deze repository toe:  
   - URL: `https://github.com/Javisen/proxmox_sensors`  
   - Categorie: **Integration**  
4. Zoek **“Proxmox Extended Sensors”** in HACS en installeer het  
5. Herstart Home Assistant  
6. Ga naar **Instellingen → Apparaten & Diensten → Integratie toevoegen** en zoek **Proxmox Extended Sensors**

### 🔹 Handmatige installatie

1. Kopieer de map `custom_components/proxmox_sensors` naar:  
   - `/config/custom_components/proxmox_sensors`  
2. Herstart Home Assistant  
3. Voeg de integratie toe via **Instellingen → Apparaten & Diensten**

---

## 🧭 Visuele Configuratiegids

Hieronder vind je een volledige visuele walkthrough van het installatieproces, inclusief inlogmethoden, resource‑selectie en configuratiestappen.

<details>
  <summary>🪪 Serververbinding</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Proxmox Login" width="600">
  </p>
  > Je hoeft geen "http://" of "https://" in te voeren — dat doen wij automatisch.
</details>

<details>
  <summary>🪪 Inloggen met Gebruiker en Wachtwoord (alleen PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Proxmox Login" width="600">
  </p>
  > Zorg dat je het juiste realm gebruikt (`pam` of `pve`).
</details>

<details> 
  <summary>🪪 Inloggen met Gebruiker en Token (PVE en PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Proxmox Login" width="600">
  </p>
  **In het veld Token_id moet je alleen de tokennaam invoeren.**
</details>

<details>
  <summary>⚙️ Resource‑selectie</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Resource Selectie" width="600">
  </p>
  *Opmerking: selecteer de CTs, VMs en Storages die je wilt toevoegen, samen met de gewenste opties.*
</details>

---

**Als je deze integratie waardeert of nuttig vindt, overweeg dan een ⭐ op GitHub te geven.**  
**Het helpt de zichtbaarheid, motiveert de ontwikkeling en ondersteunt toekomstige functies.**

## 🤝 Bijdragen & Community

Bijdragen zijn welkom! Je kunt issues of pull requests openen.  
**[Bezoek de GitHub‑repository](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Onderhouden door Javisen – MIT‑licentie</i></p>
