# ❓ FAQ — Veelgestelde Vragen

Hier vind je de meest voorkomende vragen en problemen bij het gebruik van de **Proxmox Extended Sensors**‑integratie, samen met snelle oplossingen.

---

## 🔐 Ik kan niet inloggen op de integratie (PVE of PBS)

### ✔ 1. Geen `http://` of `https://` invoeren
Voer alleen het domein of IP‑adres in, bijvoorbeeld:

192.168.1.10  
pve.mijn-domein.com

---

### ✔ 2. Geen poort invoeren
De integratie detecteert automatisch de juiste poort.

---

### ✔ 3. Controleer de rechten van de gebruiker of API‑token
De gebruiker moet beschikken over:

- PVE: `PVEAdmin`  
- PBS: `Administrator`

Rechten moeten worden toegewezen op de root `/`.

---

### ✔ 4. Controleer of het token is ingeschakeld
In Proxmox → Datacenter → Permissions → API Tokens  
Moet **Enabled: Yes** staan.

---

## 🔑 “Permission denied”, zelfs als het token correct is

Dit komt meestal door:

### ✔ 1. Het token heeft geen rechten op `/`
Rechten moeten worden toegewezen op `/ (root)`  
Niet op een specifieke node.

### ✔ 2. Het token behoort tot een gebruiker zonder rechten
De gebruiker moet de rol `PVEAdmin` of `Administrator` hebben.

---

## 🌐 De integratie detecteert mijn Tuxis PBS niet

Dit is normaal.

Tuxis‑PBS‑servers geven **geen interne systeemstatistieken** vrij via de API:

- datastore‑ruimte  
- schijfgebruik  
- RRD‑statistieken  
- node‑hardware  
- temperatuur  
- SMART  
- CPU/RAM  

Dit is geen fout in de integratie.  
Tuxis blokkeert deze endpoints bewust.

De integratie herkent automatisch een Tuxis PBS en verbergt niet‑beschikbare sensoren.

---

## 📦 Ik zie geen datastore‑ruimte sensoren in PBS

### ✔ Als je PBS van Tuxis is → deze gegevens zijn niet beschikbaar
Tuxis blokkeert het endpoint dat de datastore‑status teruggeeft.

Zonder dit endpoint zijn de volgende gegevens niet beschikbaar:

- totale ruimte  
- vrije ruimte  
- gebruikspercentage  
- deduplicatie  
- chunks  
- GC  

---

## 🌡️ Temperatuursensoren verschijnen niet in PVE

### ✔ 1. `lm-sensors` moet op de node zijn geïnstalleerd  
### ✔ 2. `sensors-detect` moet worden uitgevoerd  
### ✔ 3. De aanbevolen modules moeten worden geladen  
Voorbeeld:

modprobe coretemp  
modprobe nct6775  

### ✔ 4. Er moet een systemd‑service worden aangemaakt  
Zodat de sensoren na een reboot blijven werken.

---

## 🖥️ NVMe/SSD/HDD‑sensoren verschijnen niet

### ✔ 1. De schijf moet temperatuurondersteuning bieden  
Sommige OEM‑modellen geven geen sensorgegevens vrij.

### ✔ 2. Virtuele NVMe‑schijven in VM’s hebben geen sensoren  
Alleen fysieke hardware ondersteunt dit.

### ✔ 3. Tuxis PBS toont geen schijfsensoren  
Beperking van de provider.

---

## 🧠 Mijn VM’s of containers verschijnen niet

### ✔ 1. Controleer de gebruikersrechten  
De gebruiker moet de rol `PVEAdmin` hebben.

### ✔ 2. Bij clusters  
Je moet verbinding maken met de **hoofdnodes**, niet met een secundaire node.

---

## 🔄 De integratie werkt langzaam bij het updaten

Dit is normaal.

De integratie gebruikt een interne coördinator om:

- API‑overbelasting te voorkomen  
- de belasting op de node te verminderen  
- de prestaties te verbeteren  

De standaard update‑interval is 10 seconden (aanpasbaar).

---

## 🧩 Kan ik meerdere PVE‑ en PBS‑servers gebruiken?

Ja.  
De integratie ondersteunt meerdere instanties, elk met een eigen token.

---

## 🔒 Zijn API‑tokens veilig?

Ja.

De integratie:

- slaat geen wachtwoorden op  
- gebruikt alleen tokens  
- voert geen commando’s uit op de server  
- wijzigt geen Proxmox‑configuratie  
- opent geen extra poorten  

---

## 🧹 Hoe verwijder ik oude sensoren?

Home Assistant verwijdert automatisch verweesde entiteiten.

Wil je handmatig opschonen:

1. Verwijder de integratie  
2. Herstart Home Assistant  
3. Voeg de integratie opnieuw toe  

---

## 🛠️ Waar kan ik problemen melden?

Open een issue op GitHub met:

- HA‑versie  
- Proxmox‑versie  
- relevante logs  
- stappen om het probleem te reproduceren  
- servertype (PVE, PBS, Tuxis, enz.)  

---

# 🧾 Checklist voordat je een issue opent

Deze lijst lost 90% van de problemen op:

### ✔ 1. Kun je Proxmox openen in je browser?  
Zo niet, dan kan de integratie dat ook niet.

### ✔ 2. Gebruik je alleen domein/IP?  
Geen `http://`, `https://` of poorten.

### ✔ 3. Is het API‑token ingeschakeld?  
Moet **Enabled: Yes** tonen.

### ✔ 4. Heeft de gebruiker rechten op `/`?  
Rechten moeten op `/ (root)` worden toegewezen.

### ✔ 5. Is `lm-sensors` geïnstalleerd en geconfigureerd?  
Zonder dit pakket verschijnen er geen hardware‑sensoren.

### ✔ 6. Is je PBS van Tuxis?  
Dan zijn interne statistieken niet beschikbaar.

### ✔ 7. Heb je Home Assistant herstart na het wijzigen van rechten?  
HA gebruikt oude rechten uit cache.

### ✔ 8. Zijn er fouten in de HA‑logs?  
Controleer het gedeelte “Integraties”.

### ✔ 9. Heb je de incognito‑modus geprobeerd?  
Het HA‑frontend cachet bestanden zeer lang.

---

# 🚫 Bekende Beperkingen

Deze beperkingen zijn geen fouten van de integratie, maar beperkingen van Proxmox of de provider.

---

### 🔒 1. Tuxis PBS

Tuxis‑PBS‑servers geven geen:

- datastore‑ruimte  
- schijfgebruik  
- deduplicatie  
- chunks  
- RRD‑statistieken  
- hardware‑informatie  
- temperatuur  
- SMART  
- CPU/RAM  

De integratie verbergt deze sensoren automatisch.

---

### 🧊 2. Hardware‑sensoren in virtuele machines

VM’s geven geen echte sensorgegevens vrij:

- temperaturen  
- ventilatoren  
- spanningen  
- SMART  

Alleen fysieke hardware ondersteunt dit.

---

### 📦 3. NVMe/SSD zonder sensoren

Sommige OEM‑modellen of RAID‑controllers geven geen temperatuur‑ of SMART‑gegevens vrij.

---

### 🔐 4. Tokens zonder rechten op `/`

Als rechten op een node worden toegewezen in plaats van op `/`, blokkeert Proxmox de API.

---

### 🕒 5. Update‑intervallen

De integratie gebruikt een minimuminterval om API‑overbelasting te voorkomen.  
Het is normaal dat waarden enkele seconden vertraagd worden bijgewerkt.

---

### 🧩 6. Proxmox‑clusters

Je moet verbinding maken met de **hoofdnodes** van het cluster.  
Secundaire nodes bieden niet de volledige API.

---

### 🌐 7. Zelfondertekende SSL‑certificaten

De integratie accepteert deze automatisch, maar sommige browsers tonen waarschuwingen.
