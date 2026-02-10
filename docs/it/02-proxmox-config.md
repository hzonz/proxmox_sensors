# 🔐 Passo 2: Configurazione Utenti e Permessi

**Affinché Home Assistant comunichi con Proxmox in modo sicuro, si consiglia di non utilizzare l'utente root. Creeremo un utente dedicato e gli assegneremo i permessi necessari affinché l'integrazione funzioni al 100%.**

> ⚠️ **IMPORTANTE:**  
> A causa delle funzioni avanzate dell'integrazione (controllo di VM/CT, backup individuali e di massa, azioni PBS…), è necessario assegnare **permessi di amministratore** sia in PVE che in PBS.

---

## 1. Differenza tra PVE e PBS

### **Proxmox VE (PVE)**
- Puoi utilizzare **Utente/Password** o **Token API**.  
- L'utente deve avere il ruolo **PVEAdmin**.

### **Proxmox Backup Server (PBS)**
- È **obbligatorio** utilizzare un **Token API**.  
- L'utente deve avere il ruolo **Administrator** (PBS non dispone di un ruolo intermedio valido).

---

## 2. Creazione dell'Utente

1. Vai su **Datacenter → Permissions → Users**  
2. Clicca su **Add**  
3. Configura:  
   - **User:** `homeassistant`  
   - **Realm:** `pve`  
   - **Password:** solo se intendi utilizzare il login tramite password in PVE  
4. Salva le modifiche

---

## 3. Assegnazione del Ruolo Corretto

1. Vai su **Datacenter → Permissions**  
2. Clicca su **Add → User Permission**  
3. Configura i seguenti campi:

### ✔ Per PVE:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

### ✔ Per PBS:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

> 💡 **Perché `/` è necessario:**  
> L'integrazione necessita di accesso globale per leggere nodi, VM, CT, dischi, datastore e task.

---

## 4. Generazione del Token API (Obbligatorio per PBS)

1. Vai su **Datacenter → Permissions → API Tokens**  
2. Clicca su **Add**  
3. Configura:  
   - **User:** `homeassistant@pve`  
   - **Token ID:** `ha-token`  
   - **Privilege Separation:** **deselezionato**  
   - **Expire:** **Never**  
4. Durante la creazione del token, Proxmox mostrerà:  
   - **Token ID**  
   - **Secret** (mostrato una sola volta)

> [!WARNING]
> **Copia il "Secret" ora e conservalo in un posto sicuro.** Una volta chiusa questa finestra, Proxmox non te lo mostrerà mai più per motivi di sicurezza.

> [!TIP]
> ### 💡 Hai dimenticato di copiare il Secret?
> Non preoccuparti. Sebbene Proxmox non te lo mostri più per motivi di sicurezza, non è necessario eliminare il token e ricominciare da zero:
> 
> 1. Nell'elenco **API Tokens**, seleziona il token che hai già creato.
> 2. Clicca sul pulsante **Regenerate**.
> 3. Il sistema invalidera immediatamente la vecchia chiave e ti fornirà un **nuovo Secret**.
> 
> *Ricorda che se rigeneri il Secret, devi aggiornarlo nella configurazione di Home Assistant affinché l'integrazione possa riconnettersi.*
