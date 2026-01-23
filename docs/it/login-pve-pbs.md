# 🔌 Passaggio 3: Installazione dell'Integrazione in Home Assistant

Per visualizzare i dati (comprese le temperature hardware), utilizzeremo l'integrazione **Proxmox Extended Sensors**.

## 1. Installazione tramite HACS
Trattandosi di un'integrazione personalizzata, dobbiamo prima aggiungerla al nostro store HACS:

1. Vai su **HACS > Integrazioni**.
2. Fai clic sui tre puntini nell'angolo in alto a destra e seleziona **Repository personalizzati**.
3. Incolla l'URL di questo repository: `https://github.com/Javisen/proxmox_sensors/`
4. In **Categoria**, seleziona `Integrazione` e fai clic su **Aggiungi**.
5. Cerca l'integrazione, installala e **riavvia Home Assistant**.

## 2. Configurazione dell'Integrazione
Una volta riavviato, segui questi passaggi:

1. Vai su **Impostazioni > Dispositivi e Servizi**.
2. Fai clic su **Aggiungi Integrazione** e cerca `Proxmox Extended Sensors`.

## 3. Dati di Connessione
Il modulo di accesso è molto semplice, ma presta attenzione a questi dettagli:

* **Host:** * Se sei nella tua rete locale: Inserisci solo l'IP (es. `192.168.1.50`). **Non è necessario inserire la porta**.
    * Se accedi dall'esterno: Inserisci il tuo dominio. **Non scrivere `http://` né `https://`**, l'integrazione lo rileva automaticamente.
* **Tipo di server:** Seleziona tra **PVE** (Proxmox Virtual Environment) o **PBS** (Proxmox Backup Server).
* **Usar Token:** Seleziona se intendi utilizzare l'API Token creato nel Passaggio 2 o il login tradizionale.

### Opzione A: Login con Utente (Senza Token)
Se preferisci non usare il token, compila questi campi:
* **User:** Sempre nel formato `utente@realm` (esempio: `homeassistant@pve` o `root@pam`).
* **Password:** La password dell'utente.
* **Node Name:** Il nome del tuo nodo Proxmox (quello che appare nell'albero a sinistra nell'interfaccia web di Proxmox).

### Opzione B: Login con Token (Obbligatorio per PBS)
Se preferisci usare il token, compila questi campi:
* **User:** Sempre nel formato `utente@realm` (esempio: `homeassistant@pve` o `root@pam`).
* **token_id:** Il nome identificativo che hai dato al token (esempio: `ha-token`). Da non confondere con l'ID completo.
* **Token_secret:** La stringa di caratteri (segreto) generata da Proxmox.

---

## ✅ Selezione delle Entità (SOLO PER AMBIENTE PVE)
Dopo aver fatto clic su invia, l'integrazione (in modalità PVE) eseguirà la scansione del server e ti permetterà di scegliere cosa monitorare:
* **VMs:** Macchine virtuali specifiche.
* **CTs:** Container LXC.
* **Dischi Fisici:** Hard disk e SSD collegati.
* **Storages:** Partizioni di archiviazione e relativo spazio libero.

> [!TIP]
> **Seleziona solo ciò di cui hai realmente bisogno.** Questo manterrà il tuo Home Assistant pulito e con prestazioni migliori.

## ⚠️ Nota importante per PBS in ambienti condivisi (Es. Tuxis)

Se utilizzi la versione gratuita di **Tuxis** o fornitori simili di PBS gestito, devi comprendere che l'integrazione avrà limitazioni importanti. Ciò accade perché la tua istanza di PBS gira in un **ambiente condiviso (Multi-tenant)** e non su un server dedicato.

### Perché non vedrai tutti i sensori?
A differenza di un Proxmox locale, in questi servizi:
* **Nessun accesso all'Hardware Reale:** Non hai accesso al filesystem reale né all'archiviazione fisica diretta.
* **Infrastruttura Nascosta:** Non puoi monitorizzare il backend (Ceph/ZFS) utilizzato dal fornitore, poiché è di sua proprietà.
* **Privacy e Sicurezza:** Il fornitore blocca l'accesso alle metriche globali del sistema per evitare che un cliente possa dedurre informazioni su altri utenti o sul carico totale della propria infrastruttura.
* **Senza permessi di Root:** Non avendo accesso alla radice (`/`) del sistema, non è possibile estrarre i dati dei sensori di temperatura o i giri delle ventole del nodo.

**Risultato:** In questi casi, l'integrazione non mostrerà nulla, solo sensori senza informazioni. Lavoreremo per cercare di mostrare i dati del datacenter personale nelle versioni future.
