# 📚 Documentazione e Guide

Per garantire una configurazione senza problemi, segui queste guide passo dopo passo:

---

## 🌡️ [01. Configurazione dei Sensori Hardware](01-install-sensors.md)
Come installare e configurare **lm-sensors** sul tuo nodo Proxmox per abilitare il monitoraggio di temperature e ventole.

---

## 🔑 [02. Configurazione di Proxmox](02-proxmox-config.md)
Come creare un **utente** e un **API Token** sicuri in Proxmox (PVE e PBS) con i permessi minimi necessari.

---

## ⚙️ [03. Accesso dell’Integrazione (PVE e PBS)](03-login-pve-pbs.md)
Guida attraverso la configurazione iniziale in Home Assistant e la connessione ai tuoi server.

---

## ❓ [04. Domande Frequenti e Risoluzione dei Problemi](04-faq.md)
Domande comuni, problemi noti e come risolverli.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---

# 🚀 Proxmox Extended Sensors

## Introduzione

**Proxmox Extended Sensors è l’integrazione più completa, efficiente e avanzata per Home Assistant, progettata per offrire un controllo reale e un monitoraggio approfondito di Proxmox VE e Proxmox Backup Server (PBS).**

Questa integrazione va ben oltre la semplice visualizzazione dei dati: offre **visibilità totale** della tua infrastruttura e aggiunge **vere capacità di controllo**, permettendoti di gestire nodi, macchine virtuali, container, dischi, datastores e attività PBS direttamente da Home Assistant.

A differenza di altre soluzioni, Proxmox Extended Sensors è costruita con un approccio professionale:

- **Monitoraggio avanzato** di hardware, VM, CT, dischi e PBS.  
- **Azioni di controllo complete** (avvio, arresto, spegnimento, riavvio, reset, pausa, ibernazione…).  
- **Servizi di backup completamente integrati**, sia singoli che multipli.  
- **Compatibilità totale con PBS**, inclusa deduplicazione e naming automatico.  
- **Autenticazione sicura basata su Token**.  
- **Struttura pulita e organizzata** di entità e dispositivi.  
- **Uso minimo delle risorse** grazie a un polling ottimizzato.

I backup creati da Home Assistant si integrano perfettamente con quelli creati da Proxmox VE, utilizzando nomi identificabili come:  
**HA-{{vmid}}-{{guestname}}**  
e mantengono **tutti i vantaggi di PBS**, inclusa la deduplicazione e la compatibilità con le catene di backup esistenti.

In sintesi, questa integrazione trasforma Home Assistant in un **vero pannello di controllo per Proxmox**, combinando monitoraggio dettagliato, automazione avanzata e controllo totale dell’infrastruttura.

---

## 🧩 Versioni Supportate

- Proxmox VE 7.x / 8.x / 9.x  
- Proxmox Backup Server 3.x / 4.x  
- Home Assistant 2024.x o successivo

---

## 📑 Indice dei Contenuti

- [Funzionalità Chiave](#-caratteristiche-chiave-v200)  
- [Stato e Prestazioni del Nodo](#-stato-e-prestazioni-del-nodo)  
- [Dischi e SMART](#-dischi-e-smart)  
- [Macchine Virtuali (QEMU)](#-macchine-virtuali-qemu)  
- [Container (LXC)](#-container-lxc)  
- [Servizi di Backup](#-servizi-di-backup-vms-e-cts)  
- [Proxmox Backup Server (PBS)](#-proxmox-backup-server-pbs)  
- [Azioni di Controllo (PVE e PBS)](#-azioni-di-controllo-pve-e-pbs)  
- [Installazione](#-installazione)  
- [Guida Visiva alla Configurazione](#-guida-visiva-alla-configurazione)  
- [Contributi](#-contributi-e-community)

---

<details>
  <summary>🖼️ Anteprima Dashboard</summary>
  <p align="center">
  <img src="/img/Dashboard.png" alt="Login Proxmox">
  </p>
  *Esempio di un dashboard moderno con **Card-Mod** (Modalità Scura) e i nostri sensori strutturati:*
</details>

---

## 🔥 Funzionalità Chiave (v2.0.0)

### 🌡️ Monitoraggio Hardware Avanzato (PVE e PBS)

- **Temperature in tempo reale:** core CPU, VRM, chipset, NVMe/SSD/HDD.  
- **Sensori meccanici:** velocità delle ventole (RPM), voltaggi e altri sensori della scheda madre.  
- **Filtraggio intelligente:** vengono create solo entità con dati validi per mantenere il sistema pulito.  
  > Richiede `lm-sensors` sull’host Proxmox.

---

### 🧠 Stato e Prestazioni del Nodo

- Utilizzo CPU, I/O wait, load average.  
- RAM totale/usata/libera e percentuale.  
- Uptime e versione del kernel/PVE.  
- Sensori di rete RX/TX per nodo, VM e container.

<details>
  <summary>🔳 Attributi del Nodo</summary>
  <p align="center">
    <img src="../../img/pve/node_attr.png" alt="Attributi del Nodo" width="600">
  </p>
</details>

<details>
  <summary>⭕ Controlli del Nodo</summary>
  <p align="center">
    <img src="../../img/pve/node_controls.png" alt="Controlli del Nodo" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Temperatura CPU</summary>
  <p align="center">
    <img src="../../img/pve/cpu_temp_attr.png" alt="Temperatura CPU" width="600">
  </p>
</details>

<details>
  <summary>🌡️ Temperatura Chipset</summary>
  <p align="center">
    <img src="../../img/pve/chipset_temp.png" alt="Temperatura Chipset" width="600">
  </p>
</details>

<details>
  <summary>⏳ CPU I/O Wait</summary>
  <p align="center">
    <img src="../../img/pve/cpu_wait.png" alt="CPU I/O Wait" width="600">
  </p>
</details>

---

### 💾 Dischi & SMART

- Sensori dei dischi fisici raggruppati come dispositivi dedicati.  
- Spazio totale/usato, livello di usura (NVMe wear level) e altro.  
- Attributi SMART per HDD/SSD/NVMe (se disponibili).  
- Sensori di temperatura dedicati per tipo di disco (SATA, NVMe, ecc.).

<details>
  <summary>💾 Sensori Disco</summary>
  <p align="center">
    <img src="../../img/pve/disks_sensors.png" alt="Sensori Disco" width="600">
  </p>
</details>

<details>
  <summary>🩺 Attributi SMART HDD/SSD</summary>
  <p align="center">
    <img src="../../img/pve/disk_hd_smart_attr.png" alt="SMART HDD" width="600">
  </p>
</details>

<details>
  <summary>🩺 Attributi SMART NVMe</summary>
  <p align="center">
    <img src="../../img/pve/disk_nvme_smart_attr.png" alt="SMART NVMe" width="600">
  </p>
</details>

---

### 🖥️ Macchine Virtuali (QEMU)

- Stato, utilizzo CPU, RAM usata/totale, disco usato/totale.  
- Rete RX/TX per VM.  
- Uptime e sensori informativi di base.  
- Raggruppamento pulito dei dispositivi per VM in Home Assistant.

<details>
  <summary>🖥️ Controlli e Sensori VM</summary>
  <p align="center">
    <img src="../../img/pve/vm_control.png" alt="Controllo VM" width="600">
  </p>
</details>

---

### 📦 Container (LXC)

- Stato, utilizzo CPU, RAM usata/totale, disco usato/totale.  
- Rete RX/TX per container.  
- Uptime e sensori informativi di base.  
- Stessa struttura pulita delle VM.

<details>
  <summary>📦 Controlli e Sensori Container</summary>
  <p align="center">
    <img src="../../img/pve/ct_control.png" alt="Controllo CT" width="600">
  </p>
</details>

---

## 💾 Servizi di Backup (VM e CT)

L’integrazione include due potenti servizi di backup che permettono di creare **backup Proxmox direttamente da Home Assistant**, completamente compatibili con Proxmox VE e Proxmox Backup Server (PBS).
