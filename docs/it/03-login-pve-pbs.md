# 🔌 Passo 3: Installazione dell'Integrazione in Home Assistant

Per visualizzare i dati (incluse temperature, sensori hardware, dischi, PBS, VM e CT), utilizzeremo l'integrazione **Proxmox Extended Sensors**.

[Guida Visiva di Installazione](#-Guida-Visiva-di-Installazione)

---

## 1. Installazione tramite HACS

Essendo un'integrazione personalizzata, dobbiamo prima aggiungerla a HACS:

1. Vai su **HACS → Integrazioni**  
2. Clicca sui **tre punti** (in alto a destra)  
3. Seleziona **Repository personalizzati**  
4. Aggiungi questo repository: `https://github.com/Javisen/proxmox_sensors/`
5. In **Categoria**, seleziona `Integrazione`  
6. Installala e **riavvia Home Assistant**

---

## 2. Configurazione dell'Integrazione

Dopo il riavvio:

1. Vai su **Impostazioni → Dispositivi e Servizi**  
2. Clicca su **Aggiungi integrazione**  
3. Cerca **Proxmox Extended Sensors**

---

## 3. Dati di Connessione

Il modulo è semplice, ma ci sono dettagli importanti:

### 🔹 Host
- **In rete locale:** solo l'IP → `192.168.1.50`  
*(Non aggiungere porta o http/https)*  
- **Dall'esterno:** il tuo dominio → `proxmox.miodominio.com`  
*(L'integrazione rileva automaticamente http/https)*

### 🔹 Tipo di server
- **PVE** → Proxmox Virtual Environment  
- **PBS** → Proxmox Backup Server  

### 🔹 Metodo di autenticazione
- **Login tradizionale** (solo PVE)  
- **Token API** (obbligatorio per PBS)

---

## 🔐 Opzione A: Accesso con Utente (senza Token)

Valida solo per **PVE**.

Campi:

- **Utente:** `utente@realm`  
Esempi:  
- `homeassistant@pve`  
- `root@pam`  
- **Password:** la password dell'utente  
- **Nome Nodo:** nome del nodo (come appare in Proxmox)

---

## 🔐 Opzione B: Accesso con Token (consigliato e obbligatorio per PBS)

Campi:

- **Utente:** `utente@realm`  
- **token_id:** solo il nome del token → `ha-token`  
*(Non inserire `utente@pve!token`)*  
- **Token_secret:** il Secret generato da Proxmox  

---

## ✅ Selezione delle Entità (solo in PVE)

Dopo la connessione, l'integrazione scannerizzerà il tuo server e potrai scegliere cosa monitorare:

- **VM**  
- **CT**  
- **Dischi fisici**  
- **Storage**

> [!TIP]  
> Seleziona solo ciò di cui hai bisogno per mantenere Home Assistant pulito e veloce.

---

## 🧭 Guida Visiva di Installazione

**Di seguito troverai una guida visiva completa del processo di configurazione, inclusi i metodi di accesso, la selezione delle risorse e i passaggi di configurazione.**

<details>
  <summary>🪪 Screenshot: Connessione al Server</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Non usare "http://" o "https://". Lo gestiamo già per te.
</details>

<details>
  <summary>🪪 Screenshot: Accesso tramite Utente e Password (solo PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Assicurati di usare il realm `pam` o `pve` in base alla configurazione dell'utente.
</details>

<details> 
  <summary>🪪 Screenshot: Accesso tramite Utente e Token (PVE e PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **Nel campo Token_id inserire solo il nome del token**
</details>

<details>
  <summary>⚙️ Screenshot: Selezione delle Risorse</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Nota: Seleziona i CT, VM e Storage che desideri aggiungere così come le opzioni*
</details>

---

## ⚠️ Nota importante per PBS in ambienti condivisi (Tuxis, Hetzner, ecc.)

Se usi un PBS **gestito** o **multi‑tenant**, come Tuxis Free PBS:

- Non vedrai sensori hardware  
- Non vedrai temperature  
- Non vedrai dischi fisici  
- Non vedrai metriche del nodo  

Questo è normale perché:

- Non hai accesso all'hardware reale  
- Il provider nasconde l'infrastruttura  
- Non hai permessi root  
- Non puoi accedere al filesystem reale  

**Risultato:**  
L'integrazione mostrerà solo sensori vuoti o nessun dato.  
Nelle versioni future cercheremo di visualizzare metriche personalizzate del datastore.
