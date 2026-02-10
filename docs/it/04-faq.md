# ❓ FAQ — Domande Frequenti

Qui trovi le domande e i problemi più comuni relativi all’integrazione **Proxmox Extended Sensors**, insieme alle soluzioni rapide.

---

## 🔐 Non riesco ad accedere all’integrazione (PVE o PBS)

### ✔ 1. Non inserire `http://` o `https://`
Inserisci solo il dominio o l’indirizzo IP, ad esempio:

192.168.1.10  
pve.mio-dominio.com

---

### ✔ 2. Non inserire la porta
L’integrazione rileva automaticamente la porta corretta.

---

### ✔ 3. Controlla i permessi dell’utente o del Token API
L’utente deve avere:

- PVE: `PVEAdmin`  
- PBS: `Administrator`

I permessi devono essere assegnati alla root `/`.

---

### ✔ 4. Assicurati che il Token sia attivo
In Proxmox → Datacenter → Permissions → API Tokens  
Deve mostrare **Enabled: Yes**.

---

## 🔑 Dice “Permission denied” anche se il Token è corretto

Le cause più comuni:

### ✔ 1. Il Token non ha permessi sulla root `/`
I permessi devono essere assegnati a `/ (root)`  
Non a un nodo specifico.

### ✔ 2. Il Token appartiene a un utente senza permessi
L’utente deve avere il ruolo `PVEAdmin` o `Administrator`.

---

## 🌐 L’integrazione non rileva il mio PBS Tuxis

È normale.

I server PBS gestiti da Tuxis **non espongono metriche interne** tramite API:

- spazio del datastore  
- utilizzo del disco  
- statistiche RRD  
- hardware del nodo  
- temperatura  
- SMART  
- CPU/RAM  

Non è un bug dell’integrazione.  
Tuxis blocca intenzionalmente questi endpoint.

L’integrazione rileva automaticamente un PBS Tuxis e nasconde i sensori non disponibili.

---

## 📦 Non vedo i sensori dello spazio del datastore in PBS

### ✔ Se il tuo PBS è Tuxis → questi dati non sono disponibili
Tuxis blocca l’endpoint che restituisce lo stato del datastore.

Senza questo endpoint non è possibile ottenere:

- spazio totale  
- spazio libero  
- percentuale di utilizzo  
- deduplicazione  
- chunks  
- GC  

---

## 🌡️ I sensori di temperatura non compaiono in PVE

### ✔ 1. `lm-sensors` deve essere installato sul nodo  
### ✔ 2. Devi eseguire `sensors-detect`  
### ✔ 3. Devi caricare i moduli consigliati  
Esempio:

modprobe coretemp  
modprobe nct6775  

### ✔ 4. Devi creare un servizio systemd  
Per mantenere i sensori attivi dopo il riavvio.

---

## 🖥️ I sensori NVMe/SSD/HDD non compaiono

### ✔ 1. Il disco deve supportare la lettura della temperatura  
Alcuni modelli OEM non espongono sensori.

### ✔ 2. Gli NVMe virtualizzati nelle VM non hanno sensori  
Solo l’hardware fisico li espone.

### ✔ 3. I PBS Tuxis non espongono sensori dei dischi  
Limitazione del provider.

---

## 🧠 Le mie VM o i miei container non compaiono

### ✔ 1. Controlla i permessi dell’utente  
Deve avere il ruolo `PVEAdmin`.

### ✔ 2. Se usi un cluster  
Devi collegarti al **nodo principale**, non a un nodo secondario.

---

## 🔄 L’integrazione aggiorna i valori lentamente

È normale.

L’integrazione utilizza un coordinatore interno per:

- evitare sovraccarichi dell’API  
- ridurre il carico sul nodo  
- migliorare le prestazioni  

L’intervallo predefinito è 10 secondi (modificabile).

---

## 🧩 Posso usare più server PVE e PBS?

Sì.  
L’integrazione supporta più istanze, ognuna con il proprio Token.

---

## 🔒 Gli API Token sono sicuri?

Sì.

L’integrazione:

- non memorizza password  
- utilizza solo Token  
- non esegue comandi sul server  
- non modifica la configurazione di Proxmox  
- non apre porte aggiuntive  

---

## 🧹 Come elimino vecchi sensori?

Home Assistant rimuove automaticamente le entità orfane.

Per forzare la pulizia:

1. Rimuovi l’integrazione  
2. Riavvia Home Assistant  
3. Aggiungila di nuovo  

---

## 🛠️ Dove posso segnalare problemi?

Apri un issue su GitHub includendo:

- versione di HA  
- versione di Proxmox  
- log rilevanti  
- passaggi per riprodurre  
- tipo di server (PVE, PBS, Tuxis, ecc.)  

---

# 🧾 Checklist prima di aprire un Issue

Questa lista risolve il 90% dei problemi:

### ✔ 1. Puoi accedere a Proxmox dal browser?  
Se l’interfaccia web PVE/PBS non è accessibile, l’integrazione non funzionerà.

### ✔ 2. Stai usando solo dominio/IP?  
Niente `http://`, `https://` o porte.

### ✔ 3. Il Token API è attivo?  
Deve mostrare **Enabled: Yes**.

### ✔ 4. L’utente ha permessi sulla root `/`?  
I permessi devono essere assegnati a `/ (root)`.

### ✔ 5. `lm-sensors` è installato e configurato?  
Senza questo pacchetto non appariranno sensori hardware.

### ✔ 6. Il tuo PBS è Tuxis?  
In tal caso, le metriche interne non sono disponibili.

### ✔ 7. Hai riavviato Home Assistant dopo aver modificato i permessi?  
HA memorizza in cache i permessi precedenti.

### ✔ 8. Ci sono errori nei log di HA?  
Controlla la sezione “Integrazioni”.

### ✔ 9. Hai provato la modalità in incognito?  
Il frontend di HA memorizza le risorse per molto tempo.

---

# 🚫 Limitazioni Conosciute

Queste limitazioni non sono bug dell’integrazione, ma restrizioni di Proxmox o del provider.

---

### 🔒 1. PBS Tuxis

I PBS Tuxis non espongono:

- spazio del datastore  
- utilizzo del disco  
- deduplicazione  
- chunks  
- statistiche RRD  
- hardware del nodo  
- temperatura  
- SMART  
- CPU/RAM  

L’integrazione nasconde automaticamente questi sensori.

---

### 🧊 2. Sensori hardware nelle macchine virtuali

Le VM non espongono sensori reali:

- temperature  
- ventole  
- tensioni  
- SMART  

Solo l’hardware fisico li supporta.

---

### 📦 3. NVMe/SSD senza sensori

Alcuni modelli OEM o controller RAID non espongono temperatura o SMART.

---

### 🔐 4. Token senza permessi su `/`

Se i permessi vengono assegnati a un nodo invece che alla root, Proxmox blocca l’API.

---

### 🕒 5. Intervalli di aggiornamento

L’integrazione utilizza un intervallo minimo per evitare sovraccarichi dell’API.  
È normale che i valori impieghino qualche secondo ad aggiornarsi.

---

### 🧩 6. Cluster Proxmox

Devi collegarti al **nodo principale** del cluster.  
I nodi secondari non espongono l’intera API.

---

### 🌐 7. Certificati SSL autofirmati

L’integrazione li accetta automaticamente, ma alcuni browser possono mostrare avvisi.
