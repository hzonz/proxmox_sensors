# 🔐 Passaggio 2: Configurazione di Utenti e Permessi
**Affinché Home Assistant comunichi con Proxmox in modo sicuro, si raccomanda di non utilizzare l'utente root. In questa guida creeremo un accesso con permessi di "sola lettura".**

## 1. Differenza tra PVE e PBS
Prima di iniziare, tieni presente che:

* **Proxmox VE (PVE):** Puoi usare un Nome Utente/Password convenzionale o un API Token.

* **Proxmox Backup Server (PBS):** È indispensabile usare un API Token. I metodi di login tradizionali spesso falliscono a causa di restrizioni di sicurezza o permessi nel Datastore.

---

## 2. Creazione del Ruolo (Permessi)
**Un "Ruolo" definisce cosa può fare l'integrazione.**

1. Vai su **Datacenter > Permissions > Roles**.
2. Fai clic su **Create** e nominalo `HA-Monitor`.
3. Seleziona i seguenti privilegi (**Privileges**):
    * `Sys.Audit`: Permette di vedere lo stato del nodo (CPU, RAM).
    * `VM.Audit`: Permette di vedere lo stato delle VM e dei container.
    * `Datastore.Audit`: Permette di vedere lo spazio su disco.

---
  
## 3. Creazione dell'Utente
1. Vai su **Datacenter > Permissions > Users**.
2. Fai clic su **Add**.
3. **User:** `homeassistant` (puoi lasciare il realm come `pve`).
4. Inserisci una password sicura se intendi usare questo metodo per PVE.

---

## 4. Assegnazione del Ruolo
**Devi comunicare a Proxmox che l'utente ha il ruolo che abbiamo creato:**

1. Vai su **Datacenter > Permissions**.
2. Fai clic su **Add > User Permission**.
3. Configura i seguenti campi:
    * **Path:** `/` (Molto importante affinché l'integrazione possa vedere l'intero server).
    * **User:** `homeassistant@pve` (o l'utente che hai creato).
    * **Role:** `HA-Monitor`.

---

## 5. Generazione dell'API Token (Obbligatorio per PBS)
**Se desideri monitorare un PBS o preferisci non usare password in PVE, segui questi passaggi:**

1. Vai su **Datacenter > Permissions > API Tokens**.
2. Fai clic su **Add** e compila il modulo:
    * **User:** Seleziona l'utente `homeassistant`.
    * **Token ID:** `ha-token` (puoi scegliere il nome che preferisci).
    * **Privilege Separation:** ⚠️ **DESELEZIONA questa casella**. Se la lasci selezionata, il Token non erediterà i permessi dell'utente e l'integrazione fallirà.
3. Dopo aver cliccato su **Add**, si aprirà una finestra con due dati fondamentali:
    * **Token ID:** (Esempio: `homeassistant@pve!ha-token`).
    * **Secret:** (Una lunga stringa di lettere e numeri).

> [!WARNING]
> **Copia il "Secret" adesso e conservalo in un luogo sicuro.** Una volta chiusa questa finestra, Proxmox non te lo mostrerà mai più per motivi di sicurezza.


> [!TIP]
> ### 💡 Hai dimenticato di copiare il Secret?
> Non preoccuparti. Anche se Proxmox non lo mostra più per sicurezza, non è necessario eliminare il token e ricominciare da capo:
> 
> 1. Nella lista degli **API Tokens**, seleziona il token che avevi creato.
> 2. Fai clic sul pulsante **Regenerate**.
> 3. Il sistema invaliderà immediatamente la vecchia chiave e ti fornirà un **nuovo Secret**.
> 
> *Ricorda che se rigeneri il Secret, dovrai aggiornarlo nella configurazione di Home Assistant affinché l'integrazione possa connettersi di nuovo.*
