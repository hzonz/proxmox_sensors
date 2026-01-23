# 📚 Documentazione e Guide

Per garantire una configurazione senza problemi, segui queste guide passo dopo passo:

---

## 🌡️ [01. Configurazione dei Sensori Hardware](01-install-sensors.md)
Come installare e configurare **lm-sensors** sul tuo nodo Proxmox per abilitare il monitoraggio di temperature e ventole.

---

## 🔑 [02. Configurazione di Proxmox](02-proxmox-config.md)
Come creare un **utente** e un **API Token** sicuro in Proxmox (PVE & PBS) con i permessi minimi necessari.

---

## ⚙️ [03. Accesso all'Integrazione (PVE & PBS)](03-login-pve-pbs.md)
Guida al processo di configurazione iniziale in Home Assistant e connessione ai tuoi server.

---

## ❓ [04. Domande Frequenti e Risoluzione dei Problemi](04-faq.md)
Domande comuni, problemi noti e come risolverli.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/img/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---
# 🚀 Proxmox Extended Sensors

**L'integrazione più completa, efficiente e organizzata per monitorare Proxmox VE e PBS da Home Assistant.**

Questa integrazione è progettata per utenti avanzati che necessitano di un controllo totale sul proprio hardware senza sovraccaricare il server.
A differenza di altre soluzioni, Proxmox Sensors Extended si concentra sull'efficienza energetica, l'autenticazione sicura tramite Token e un'organizzazione visiva impeccabile.

---

## 🔥 Caratteristiche Principali

### 🌡️ Monitoraggio Hardware Avanzato

**Non accontentarti solo dell'uso della CPU. Guarda cosa succede davvero "sotto il cofano":**

* **Temperature in tempo reale:** Core della CPU, VRM e unità NVMe/SSD/HDD.
* **Sensori meccanici:** Velocità delle ventole (RPM) e voltaggi della scheda madre.
* **Sensori intelligenti:** Vengono create solo le entità che riportano dati validi, mantenendo il sistema pulito.

**(Nota: richiede l'installazione di lm-sensors sull'host Proxmox).**

---

### 🧠 Ottimizzato per le Prestazioni

**Progettato pensando all'hardware con risorse limitate:**

* **DataUpdateCoordinator:** Minimizza le chiamate all'API di Proxmox per evitare di saturare il processore del server.
* **Silent SSL:** Verifica automatica dei certificati SSL (inclusi quelli auto-firmati) senza riempire i log di errori.

---

### 🗄️ Proxmox Backup Server (PBS) Avanzato

* **Modalità Esterna:** Connettiti facilmente a server PBS remoti usando solo il dominio.
* **Monitoraggio delle Attività:** Stato dettagliato dell'ultimo Backup, Garbage Collector o attività di Verifica.

---

### 🎨 Interfaccia Dinamica e Organizzata

* **Smart Dashboard:** I sensori vengono raggruppati automaticamente in dispositivi:
  1. Nodo
  2. Dischi fisici
  3. Macchine virtuali
  4. Container (LXC)
  5. Storage
* **Auto-Naming:** Prefissi automatici (es. `pv1-cpu-temp`) per mantenere i tuoi dashboard ordinati in modo logico.

---

**Esempio di Dashboard**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>

---

## Sensori in Evidenza

## PVE

### 🖥️ Sensori Hardware (PVE & PBS)

Temperature CPU • Temperature VRM • Temperature NVMe/SSD/HDD  
Velocità ventole (RPM) • Voltaggi • Sensori di energia • Entità `pvesensors`  
• Temperatura del chipset

---

### 🧠 Stato del Nodo

Utilizzo CPU (%) • Utilizzo RAM (%) • RAM usata/totale  
Tempo di attività (uptime) • Load average • CPU I/O Wait

---

### 💾 Dischi

Capacità totale • Spazio usato (GB e %)  
Livello di usura (NVMe) • Stato SMART (se disponibile)

---

### 🖥️ Macchine Virtuali (QEMU)

Utilizzo CPU (%) • Utilizzo RAM (%) • Traffico di Rete Tx/Rx  
Stato (acceso/spento) • Selezione automatica/manualamente

---

### 📦 Container (LXC)

Utilizzo CPU (%) • Utilizzo RAM (%) • Traffico di Rete Tx/Rx  
Stato • Selezione automatica/manuale • e molti altri

---

### 🗄️ Proxmox Backup Server (PBS)

Utilizzo datastore (GB e %) • Numero di backup  
Stato del Garbage Collector • Stato dell'ultima attività di backup  
• Informazioni complete sulle attività e altro ancora
