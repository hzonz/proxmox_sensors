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

---

### 🟦 1. Servizio di Backup Singolo  
Crea un backup di una VM o di un CT specifico.

**Servizio:** `proxmox_sensors.create_vzdump_backup`

**Opzioni disponibili:**

- **Nodo** – Seleziona il nodo Proxmox.  
- **Storage di destinazione** – Qualsiasi storage che supporti i backup (local, NFS, PBS, ecc.).  
- **ID VM/CT** – ID della macchina da salvare.  
- **Modalità di backup:**  
  - `snapshot`  
  - `suspend`  
  - `stop`  
- **Compressione:**  
  - `zstd`  
  - `gzip`  
  - `lzo`  
  - `none`

I backup creati da Home Assistant vengono nominati automaticamente usando:  
**HA-{{vmid}}-{{guestname}}**

Questo garantisce che siano facilmente identificabili mantenendo **piena compatibilità con i backup già esistenti di Proxmox**.

<details>
  <summary>📦 Servizio di Backup Singolo</summary>
  <p align="center">
    <img src="../../img/pve/single_backup.png" alt="Servizio di Backup Singolo" width="600">
  </p>
</details>

---

### 🟩 2. Servizio di Backup Massivo  
Esegue il backup di **tutte le VM e/o CT** presenti in un nodo selezionato.

**Servizio:** `proxmox_sensors.backup_all`

**Opzioni disponibili:**

- **Nodo** – Seleziona il nodo da cui eseguire il backup.  
- **Storage di destinazione** – Qualsiasi storage compatibile con i backup.  
- **Modalità di backup:** snapshot / suspend / stop.  
- **Compressione:** zstd / gzip / lzo / none.  
- **Numero massimo di backup simultanei** – Controlla l’esecuzione in parallelo.  
- **Ritardo tra i backup** – Secondi tra una copia e l’altra.  
- **Includi VM** – Interruttore (Sì/No).  
- **Includi CT** – Interruttore (Sì/No).

Questo servizio è ideale per backup notturni programmati o routine di manutenzione automatizzate.

<details>
  <summary>📦 Servizio di Backup Massivo</summary>
  <p align="center">
    <img src="../../img/pve/massive_backups.png" alt="Servizio di Backup Massivo" width="600">
  </p>
</details>

---

### 🟧 Compatibilità PBS e Deduplicazione

Le copie di sicurezza create tramite questi servizi:

- Sono archiviate esattamente come quelle create da Proxmox VE  
- Usano la stessa struttura di nomi e metadati  
- Supportano automaticamente la **deduplicazione PBS**  
- Si integrano perfettamente con le catene di backup esistenti  
- Appaiono nel datastore PBS con piena compatibilità  

Non è richiesta alcuna configurazione speciale: PBS gestisce deduplicazione e indicizzazione esattamente come se il backup fosse stato creato dalla GUI o dalla CLI di Proxmox.

---

### 🗄️ Proxmox Backup Server (PBS)

**Monitoraggio avanzato del datastore e delle attività:**

- Utilizzo del datastore (GB e %), totale, usato e libero.  
- Rapporto di deduplicazione e numero di backup.  
- Ora, dimensione e stato dell’ultimo backup.  
- Errori di backup e riepilogo delle attività.  
- Stato del Garbage Collector (GC) e sensori correlati.  
- Ultima attività: tipo, stato, messaggio e durata.

<details>
  <summary>🗄️ Panoramica del Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore.png" alt="Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Server PBS</summary>
  <p align="center">
    <img src="../../img/pbs/pbs_server.png" alt="Server PBS" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Dettagli delle Attività</summary>
  <p align="center">
    <img src="../../img/pbs/task.png" alt="Attività PBS" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Stato del Garbage Collector</summary>
  <p align="center">
    <img src="../../img/pbs/gc_status_attr.png" alt="GC Status" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Manutenzione del Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Manutenzione Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Riepilogo dell’Ultima Attività</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Ultima Attività" width="600">
  </p>
</details>

---

## Azioni di controllo PBS:

- Eseguire **Garbage Collector (GC)**  
- Eseguire **Prune**  
- Eseguire **Verify**  
- Eseguire **Sync**  

<details>
  <summary>🗄️ Manutenzione del Datastore</summary>
  <p align="center">
    <img src="../../img/pbs/datastore_maintenance.png" alt="Manutenzione Datastore" width="600">
  </p>
</details>

<details>
  <summary>🗄️ Ultima Attività</summary>
  <p align="center">
    <img src="../../img/pbs/last_task_stat.png" alt="Ultima Attività" width="600">
  </p>
</details>

---

### 🎛️ Azioni di Controllo (PVE & PBS)

**Controlli del nodo:**

- Spegnere nodo  
- Riavviare nodo  

**Controlli delle macchine virtuali (QEMU):**

- Avvia, Ferma, Spegni, Riavvia, Reset  
- Pausa, Riprendi, Iberna  

**Controlli dei container (LXC):**

- Avvia, Ferma, Spegni, Riavvia  

**Controlli PBS:**

- GC, Prune, Verify, Sync (per datastore)

---

### 🎨 Organizzazione Visiva e Nomenclatura

- I sensori vengono raggruppati automaticamente in dispositivi logici:
  1. Nodo  
  2. Dischi fisici  
  3. Macchine virtuali  
  4. Container  
  5. Storage / Datastore  
  6. Server PBS e attività  

- Nomi coerenti e puliti per entità e dispositivi, mantenendo dashboard leggibili e scalabili.

---

## 🧩 Installazione

### 🔹 Tramite HACS (consigliato)

1. Apri **HACS → Integrazioni**  
2. Clicca sui tre puntini (⋮) → **Custom repositories**  
3. Aggiungi questo repository:  
   - URL: `https://github.com/Javisen/proxmox_sensors`  
   - Categoria: **Integration**  
4. Cerca **“Proxmox Extended Sensors”** in HACS e installalo  
5. Riavvia Home Assistant  
6. Vai su **Impostazioni → Dispositivi e Servizi → Aggiungi Integrazione** e cerca **Proxmox Extended Sensors**

### 🔹 Installazione manuale

1. Copia la cartella `custom_components/proxmox_sensors` in:  
   - `/config/custom_components/proxmox_sensors`  
2. Riavvia Home Assistant  
3. Aggiungi l’integrazione da **Impostazioni → Dispositivi e Servizi**

---

## 🧭 Guida Visiva alla Configurazione

Di seguito trovi una guida visiva completa al processo di configurazione, incluse modalità di accesso, selezione delle risorse e passaggi di installazione.

<details>
  <summary>🪪 Connessione al Server</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Non serve inserire "http://" o "https://". Lo facciamo automaticamente.
</details>

<details>
  <summary>🪪 Login con Utente e Password (solo PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Assicurati di usare il realm corretto (`pam` o `pve`).
</details>

<details> 
  <summary>🪪 Login con Utente e Token (PVE e PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **Nel campo Token_id devi inserire solo il nome del token.**
</details>

<details>
  <summary>⚙️ Selezione delle Risorse</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Selezione Risorse" width="600">
  </p>
  *Nota: seleziona i CT, le VM e gli storage che vuoi aggiungere, insieme alle opzioni desiderate.*
</details>

---

**Se apprezzi questa integrazione o la trovi utile, considera di lasciare una ⭐ su GitHub.**  
**Aiuta la visibilità, motiva lo sviluppo e supporta le funzionalità future.**

## 🤝 Contributi e Community

I contributi sono benvenuti! Puoi aprire issue o pull request.  
**[Visita il repository GitHub](https://github.com/Javisen/proxmox_sensors)**

---

<p align="center"><i>Manutenuto da Javisen – Licenza MIT</i></p>
