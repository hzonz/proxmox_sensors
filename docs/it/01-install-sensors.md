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

## 🚀 Passaggio 5: Installazione del Server Sensori (API Bridge)
**Poiché l'API ufficiale di Proxmox non espone tutti i dati hardware, è necessario installare questo piccolo script "ponte" sull'host Proxmox.**

1. **Download e installazione dello script**
Esegui questi comandi nel terminale del tuo server Proxmox:
```bash
# Scarica lo script dal repository
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Assegna i permessi di esecuzione
chmod +x /usr/local/bin/pve-sensors-api.py
```

2. **Configurazione come servizio di sistema**
Per fare in modo che lo script si avvii automaticamente con il server, crea il file di servizio:
```bash
cat <<EOF > /etc/systemd/system/pve-sensors.service
[Unit]
Description=PVE Sensors API
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

3. **Attivazione immediata**
Attiva e avvia il servizio con questi comandi:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
```

4. **Verifica finale**
Puoi verificare che il server sia in funzione aprendo questo indirizzo nel tuo browser (sostituendolo con l'IP del tuo Proxmox): `http://TUO_IP_PROXMOX:9000/sensors`

Se vedi un testo in formato JSON con le temperature, l'integrazione sarà ora in grado di leggere i dati correttamente.

---
**Fatto! Una volta che il comando `sensors` restituisce i dati nel terminale, la tua integrazione di Home Assistant sarà in grado di leggerli automaticamente tramite l'API di Proxmox.**
