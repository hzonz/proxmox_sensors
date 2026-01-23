# ❓ FAQ — Domande Frequenti

Di seguito troverai i dubbi e i problemi più comuni riscontrati durante l'uso dell'integrazione **Proxmox Sensors Extended**, insieme alle relative soluzioni rapide.

---

## 🔐 Non riesco a loggarmi nell'integrazione (PVE o PBS)

### ✔ 1. Non inserire `http://` né `https://`
Inserisci **solo il dominio o l'IP**, ad esempio:

`192.168.1.10`
`pve.mio-dominio.com`

---

### ✔ 2. Non inserire la porta
L'integrazione rileva automaticamente la porta corretta.

### ✔ 3. Controlla i permessi del Token API
L'utente deve avere:

- **PVE:** - `Sys.Audit`  
  - `VM.Audit`  
  - `Datastore.Audit`  
  - `Permissions.Modify` (solo se utilizzi la selezione automatica di VM/LXC)

- **PBS:** - `Datastore.Audit`  
  - `Datastore.Read`  
  - `Sys.Audit`

---

### ✔ 4. Assicurati che il Token sia attivo
In Proxmox → Datacenter → Permissions → API Tokens  
Deve apparire **Enabled: Yes**.

---

## 🔑 Ricevo "Permesso negato" anche se il Token è corretto

Questo di solito è dovuto a:

### ✔ 1. Il Token non ha permessi nella radice `/`
In Proxmox, i permessi devono essere assegnati in: `/ (root)`. **Non su un nodo specifico.**

### ✔ 2. Il Token appartiene a un utente senza permessi
L'utente padre deve avere i permessi, non solo il Token.

---

## 🌐 L'integrazione non rileva il mio PBS di Tuxis

Questo è normale.

I server PBS gestiti da Tuxis **non permettono l'accesso alle metriche interne** tramite API:

- spazio del datastore  
- utilizzo del disco  
- statistiche RRD  
- hardware del nodo  
- temperatura  
- SMART  
- CPU/RAM  

Non si tratta di un errore dell'integrazione:  
Tuxis blocca questi endpoint per progettazione.

L'integrazione rileva automaticamente che si tratta di un PBS di Tuxis e nasconde i sensori non disponibili.

---

## 📦 Non vedo i sensori dello spazio del datastore in PBS

### ✔ Se il tuo PBS è di Tuxis → **non sono disponibili**
Per motivi di sicurezza, Tuxis blocca: `/api2/json/admin/datastore/<name>/status`

Senza questo endpoint, non è possibile ottenere:

- spazio totale  
- spazio libero  
- percentuale di utilizzo  
- deduplicazione  
- chunks  
- GC (Garbage Collector)

---

## 🌡️ Non appaiono i sensori di temperatura in PVE

### ✔ 1. Devi installare `lm-sensors` sul nodo
Guida completa: [01. Configurazione dei Sensori Hardware](01-install-sensors.md)

### ✔ 2. Devi eseguire `sensors-detect`
E accettare tutte le opzioni sicure.

### ✔ 3. Devi caricare i moduli raccomandati
Esempio:

```bash
modprobe coretemp
modprobe nct6775
```
### ✔ 4. Assicurati della persistenza dei sensori
Affinché i sensori funzionino dopo il riavvio, assicurati di aver seguito i passaggi per aggiungere i moduli necessari al file `/etc/modules`.

---

## 🖥️ Non appaiono i sensori dei dischi NVMe/SSD/HDD
### ✔ 1. Il disco deve supportare la lettura della temperatura
Alcuni modelli OEM non espongono i sensori.

### ✔ 2. Nei dischi NVMe virtualizzati (VM) non ci sono sensori
Funzionano solo su hardware reale.

### ✔ 3. In PBS di Tuxis non vengono esposti i sensori del disco
Si tratta di una limitazione del fornitore.

## 🧠 Non appaiono le mie VM o i miei container

### ✔ 1. Controlla i permessi del Token
Deve avere il privilegio: `VM.Audit`

### ✔ 2. Se usi la selezione automatica
L'integrazione richiede il privilegio: `Permissions.Modify`

### ✔ 3. Se usi un cluster
Devi connetterti al nodo principale, non a un nodo secondario.

---

## 🔄 L'integrazione impiega tempo ad aggiornare i valori
Questo è normale.

L'integrazione utilizza il `DataUpdateCoordinator` per:

* evitare di saturare l'API
* ridurre il carico sul nodo
* migliorare le prestazioni

**L'intervallo predefinito è di 10 secondi ed è configurabile.**

---

## 🧩 Posso usare più PVE e PBS contemporaneamente?
### Sì.
L'integrazione permette di aggiungere più istanze, ognuna con il proprio Token.

---

## 🔒 È sicuro usare i Token API?
### Sì.

L'integrazione:

* non memorizza password
* usa solo Token con permessi minimi
* non esegue comandi sul server
* non modifica la configurazione di Proxmox
* non apre porte aggiuntive

---

## 🧹 Come elimino i vecchi sensori?
**Home Assistant elimina automaticamente le entità orfane.**

**Se vuoi forzare la pulizia:**

* Rimuovi l'integrazione
* Riavvia Home Assistant
* Aggiungila di nuovo

---

## 🛠️ Dove posso segnalare errori?
**Puoi aprire una "issue" su GitHub indicando:**

* versione di HA
* versione di Proxmox
* log rilevanti
* passaggi per riprodurre l'errore
* tipo di server (PVE, PBS, Tuxis, ecc.)

---

# 🧾 Checklist prima di aprire una Issue

Prima di segnalare un problema, controlla questa lista rapida.
Il 90% degli errori si risolve qui:

### ✔ 1. Riesci ad accedere a Proxmox dal browser?
Se non riesci a entrare nell'interfaccia web di PVE/PBS, nemmeno l'integrazione potrà farlo.

### ✔ 2. Stai usando solo il dominio/IP?
Non inserire `http://`, `https://` né porte.

### ✔ 3. Il Token API è attivo?
In Proxmox → Datacenter → Permissions → API Tokens
Deve apparire **Enabled: Yes**.

### ✔ 4. L'utente ha i permessi nella radice `/`?
I permessi devono essere assegnati in: `/ (root)`. Non su un nodo specifico.

### ✔ 5. Hai installato e configurato `lm-sensors` in PVE?
Senza questo, i sensori hardware non appariranno.

### ✔ 6. Il PBS è di Tuxis?
In tal caso, ricorda che **non espone metriche interne** (spazio, hardware, RRD).

### ✔ 7. Hai riavviato Home Assistant dopo aver cambiato i permessi?
HA mantiene in cache i vecchi permessi.

### ✔ 8. Ci sono errori nei log di Home Assistant?
Vai su:
**Impostazioni → Sistema → Registri**

### ✔ 9. Hai provato in modalità incognito?
Il frontend di HA mantiene le risorse in cache per settimane.

---

# 🚫 Limitazioni Note

Queste limitazioni non sono errori dell'integrazione, ma restrizioni di Proxmox o del fornitore:

### 🔒 1. PBS di Tuxis
I server PBS gestiti da Tuxis **non permettono di accedere a:**

- spazio del datastore
- utilizzo del disco
- deduplicazione
- chunks
- statistiche RRD
- hardware del nodo
- temperatura
- SMART
- CPU/RAM

L'integrazione rileva automaticamente questa limitazione e nasconde i sensori non disponibili.

---

### 🧊 2. Sensori hardware nelle macchine virtuali
Le VM **non espongono sensori reali**:

- temperature
- ventole
- voltaggi
- SMART

Funzionano solo su hardware fisico.

---

### 📦 3. Dischi NVMe/SSD senza sensori
Alcuni modelli OEM o controller RAID **non espongono la temperatura** né lo stato SMART.

---

### 🔐 4. Token senza permessi in `/`
Se i permessi sono assegnati a un nodo invece che alla radice, Proxmox blocca l'API.

---

### 🕒 5. Intervalli di aggiornamento
Per evitare di saturare l'API, l'integrazione utilizza un intervallo minimo di aggiornamento. Non è un errore se i valori impiegano alcuni secondi per aggiornarsi.

---

### 🧩 6. Cluster Proxmox
Devi connetterti al **nodo principale** del cluster. I nodi secondari non espongono l'intera API.

---

### 🌐 7. Certificati SSL auto-firmati
L'integrazione li accetta automaticamente, ma alcuni browser potrebbero mostrare avvisi.

---
