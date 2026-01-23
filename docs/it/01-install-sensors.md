# 🚀 Passaggio 1: Installazione e configurazione dei sensori
**Questa guida spiega come preparare il nodo Proxmox affinché esponga i dati hardware e assicuri che le letture della temperatura siano disponibili per Home Assistant.**

## 1. Installazione delle dipendenze
* **Per prima cosa, installiamo gli strumenti necessari per leggere i sensori integrati nella scheda madre e nella CPU:**

```bash
apt update && apt install lm-sensors -y
```

## 2. Rilevamento dell'hardware
* **Affinché il sistema identifichi quali driver sono necessari, eseguiamo l'assistente di rilevamento:**

```bash
sensors-detect
```
**Rispondi YES (o premi Invio) a tutte le domande. Al termine, il sistema identificherà i moduli necessari (ad esempio: `coretemp` per le CPU Intel).**

## 3. Persistenza dei moduli
**Per far sì che i sensori si attivino automaticamente al riavvio del server, l'assistente `sensors-detect` ti porrà una domanda fondamentale alla fine del processo:**

```text
Do you want to add these lines automatically to /etc/modules? (yes/NO)
```

> [!CAUTION]
> **Devi scrivere `yes` manualmente e premere Invio.** Se premi solo Invio senza scrivere nulla, il sistema selezionerà `NO` per impostazione predefinita. Se ciò accade, i sensori non verranno caricati dopo il riavvio e Home Assistant smetterà di ricevere i dati sulla temperatura.

## 4. Verifica immediata
**Per attivare i sensori subito senza dover riavviare, esegui:**

```bash
# Carica i moduli rilevati (esempio per Intel)
modprobe coretemp

# Verifica che vengano mostrate le temperature
sensors
```

**Fatto! Una volta che il comando `sensors` restituisce i dati nel terminale, la tua integrazione di Home Assistant sarà in grado di leggerli automaticamente tramite l'API di Proxmox.**
