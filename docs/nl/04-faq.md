# ❓ FAQ — Veelgestelde Vragen

Hieronder vind je de meest voorkomende vragen en problemen bij het gebruik van de **Proxmox Sensors Extended** integratie, samen met hun snelle oplossingen.

---

## 🔐 Ik kan niet inloggen op de integratie (PVE of PBS)

### ✔ 1. Gebruik geen `http://` of `https://`
Voer **alleen het domein of IP-adres** in, bijvoorbeeld:

`192.168.1.10`
`pve.mijn-domein.com`

---

### ✔ 2. Voer het poortnummer niet in
De integratie detecteert automatisch de juiste poort.

### ✔ 3. Controleer de machtigingen van de API Token
De gebruiker moet de volgende rechten hebben:

- **PVE:** - `Sys.Audit`  
  - `VM.Audit`  
  - `Datastore.Audit`  
  - `Permissions.Modify` (alleen bij gebruik van automatische selectie van VM's/LXC's)

- **PBS:** - `Datastore.Audit`  
  - `Datastore.Read`  
  - `Sys.Audit`

---

### ✔ 4. Zorg dat de Token actief is
In Proxmox → Datacenter → Permissions → API Tokens  
Er moet staan **Enabled: Yes**.

---

## 🔑 Ik krijg de melding "Permission denied" hoewel de Token correct is

Dit komt meestal door:

### ✔ 1. De Token heeft geen rechten op de root `/`
In Proxmox moeten machtigingen worden toegewezen op: `/ (root)` **Niet op een specifieke node.**

### ✔ 2. De Token behoort tot een gebruiker zonder rechten
De bovenliggende gebruiker moet ook de juiste rechten hebben, niet alleen de Token.

---

## 🌐 De integratie detecteert mijn Tuxis PBS niet

Dit is normaal.

Door Tuxis beheerde PBS-servers **staan geen toegang tot interne statistieken toe** via de API:

- datastore ruimte  
- schijfgebruik  
- RRD-statistieken  
- node hardware  
- temperatuur  
- SMART  
- CPU/RAM  

Dit is geen fout in de integratie:  
Tuxis blokkeert deze endpoints standaard in hun ontwerp.

De integratie detecteert automatisch dat het om een Tuxis PBS gaat en verbergt de niet-beschikbare sensoren.

---

## 📦 Ik zie geen datastore ruimte-sensoren in PBS

### ✔ Als je PBS van Tuxis is → **deze zijn niet beschikbaar**
Om veiligheidsredenen blokkeert Tuxis: `/api2/json/admin/datastore/<name>/status`

Zonder dit endpoint is het niet mogelijk om de volgende gegevens op te halen:

- totale ruimte  
- vrije ruimte  
- gebruikspercentage  
- deduplicatie  
- chunks  
- GC (Garbage Collector)

---

## 🌡️ Er verschijnen geen temperatuursensoren in PVE

### ✔ 1. Je moet `lm-sensors` op de node installeren
Volledige gids: [01. Hardware Sensoren Configureren](01-install-sensors.md)

### ✔ 2. Je moet `sensors-detect` uitvoeren
En alle veilige opties accepteren.

### ✔ 3. Je moet de aanbevolen modules laden
Voorbeeld:

```bash
modprobe coretemp
modprobe nct6775
```
### ✔ 4. Je moet de systemd-service aanmaken
Zodat de sensoren blijven werken na een herstart.

---

## 🖥️ Er verschijnen geen sensoren voor NVMe/SSD/HDD schijven
### ✔ 1. de schijf moet het uitlezen van temperatuur ondersteunen
Sommige OEM-modellen geven geen sensorgegevens vrij.

### ✔ 2. Geen sensoren op gevirtualiseerde NVMe (VM's)
Deze werken alleen op echte hardware.

### ✔ 3. Op Tuxis PBS worden schijfsensoren niet vrijgegeven
Beperking van de provider.

## 🧠 Mijn VM's of containers verschijnen niet

### ✔ 1. Controleer de Token-machtigingen
Deze moet hebben: `VM.Audit`

### ✔ 2. Als je automatische selectie gebruikt
De integratie heeft nodig: `Permissions.Modify`

### ✔ 3. Als je een cluster gebruikt
Je moet verbinding maken met de hoofdnode (master node), niet met een secundaire node.

---

## 🔄 De integratie doet er lang over om waarden bij te werken
Dit is normaal.

De integratie gebruikt 'DataUpdateCoordinator' om:

* te voorkomen dat de API overbelast raakt
* de belasting op de node te verminderen
* prestaties te verbeteren

**Het standaardinterval is 10 seconden en is configureerbaar.**

---

## 🧩 Kan ik meerdere PVE's en PBS'en tegelijk gebruiken?
### Ja.
De integratie staat toe om meerdere instanties toe te voegen, elk met een eigen Token.

---

## 🔒 Is het veilig om API Tokens te gebruiken?
### Ja.

De integratie:

* slaat geen wachtwoorden op
* gebruikt alleen Tokens met minimale rechten
* voert geen commando's uit op de server
* wijzigt de Proxmox-configuratie niet
* opent geen extra poorten

---

## 🧹 Hoe verwijder ik oude sensoren?
**Home Assistant verwijdert automatisch "verweesde" entiteiten.**

**Als je een schoonmaak wilt forceren:**

* Verwijder de integratie
* Herstart Home Assistant
* Voeg de integratie opnieuw toe

---

## 🛠️ Waar kan ik fouten rapporteren?
**Je kunt een issue openen op GitHub met:**

* HA-versie
* Proxmox-versie
* relevante logs
* stappen om de fout te reproduceren
* type server (PVE, PBS, Tuxis, etc.)

---

# 🧾 Checklist voordat je een Issue opent

Controleer deze korte lijst voordat je een probleem meldt.  
90% van de fouten wordt hier opgelost:

### ✔ 1. Heb je toegang tot Proxmox via de browser?
Als je niet kunt inloggen op de webinterface van PVE/PBS, kan de integratie dat ook niet.

### ✔ 2. Gebruik je alleen het domein of IP-adres?
Gebruik geen `http://`, `https://` of poortnummers.

### ✔ 3. Is de API Token actief?
In Proxmox → Datacenter → Permissions → API Tokens  
Er moet staan **Enabled: Yes**.

### ✔ 4. Heeft de gebruiker rechten op de root `/`?
Machtigingen moeten worden toegewezen op: `/ (root)`, niet op een specifieke node.

### ✔ 5. Heb je `lm-sensors` geïnstalleerd en geconfigureerd in PVE?
Zonder dit verschijnen er geen hardware-sensoren.

### ✔ 6. Is de PBS van Tuxis?
Houd er dan rekening mee dat deze **geen interne statistieken** vrijgeeft (ruimte, hardware, RRD).

### ✔ 7. Heb je Home Assistant herstart na het wijzigen van de machtigingen?
HA slaat oude machtigingen op in het cachegeheugen.

### ✔ 8. Staan er fouten in de Home Assistant logs?
Ga naar:  
**Instellingen → Systeem → Logs**

### ✔ 9. Heb je de incognito-modus geprobeerd?
De frontend van HA slaat gegevens soms wekenlang op in de cache.

---

# 🚫 Bekende Beperkingen

Deze beperkingen zijn geen fouten in de integratie, maar restricties van Proxmox of de provider:

### 🔒 1. Tuxis PBS
Door Tuxis beheerde PBS-servers **staan geen toegang toe tot:**

- datastore ruimte
- schijfgebruik
- deduplicatie
- chunks
- RRD-statistieken
- node hardware
- temperatuur
- SMART
- CPU/RAM

De integratie detecteert deze beperking automatisch en verbergt de niet-beschikbare sensoren.

---

### 🧊 2. Hardware-sensoren in virtuele machines
VM's **geven geen echte sensorgegevens vrij:**

- temperaturen
- ventilatoren
- spanningen
- SMART

Dit werkt alleen op fysieke hardware.

---

### 📦 3. NVMe/SSD schijven zonder sensoren
Sommige OEM-modellen of RAID-controllers **geven geen temperatuur** of SMART-status door.

---

### 🔐 4. Tokens zonder rechten op `/`
Als machtigingen aan een node zijn toegewezen in plaats van aan de root, blokkeert Proxmox de API.

---

### 🕒 5. Update-intervallen
Om overbelasting van de API te voorkomen, gebruikt de integratie een minimaal update-interval.  
Het is geen fout als het enkele seconden duurt voordat waarden worden bijgewerkt.

---

### 🧩 6. Proxmox Clusters
Je moet verbinding maken met de **hoofdnode** van het cluster.  
Secundaire nodes geven niet de volledige API vrij.

---

### 🌐 7. Zelfondertekende SSL-certificaten
De integratie accepteert deze automatisch, maar sommige browsers kunnen waarschuwingen tonen.
