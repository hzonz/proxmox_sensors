# 🔌 Stap 3: Installatie van de Integratie in Home Assistant

Om de gegevens te bekijken (inclusief temperaturen, hardware-sensoren, schijven, PBS, VM's en CT's), gebruiken we de integratie **Proxmox Extended Sensors**.

[Visuele Installatiegids](#-Visuele-Installatiegids)

---

## 1. Installatie via HACS

Omdat het een aangepaste integratie is, moeten we deze eerst toevoegen aan HACS:

1. Ga naar **HACS → Integraties**  
2. Klik op de **drie puntjes** (rechtsboven)  
3. Selecteer **Aangepaste repositories**  
4. Voeg deze repository toe: `https://github.com/Javisen/proxmox_sensors/`
5. Bij **Categorie**, selecteer `Integratie`  
6. Installeer het en **herstart Home Assistant**

---

## 2. Configuratie van de Integratie

Na het herstarten:

1. Ga naar **Instellingen → Apparaten & Diensten**  
2. Klik op **Integratie toevoegen**  
3. Zoek naar **Proxmox Extended Sensors**

---

## 3. Verbindingsgegevens

Het formulier is eenvoudig, maar er zijn belangrijke details:

### 🔹 Host
- **Op lokaal netwerk:** alleen het IP-adres → `192.168.1.50`  
*(Voeg geen poort of http/https toe)*  
- **Van buitenaf:** je domein → `proxmox.mijndomein.com`  
*(De integratie detecteert automatisch http/https)*

### 🔹 Servertype
- **PVE** → Proxmox Virtual Environment  
- **PBS** → Proxmox Backup Server  

### 🔹 Authenticatiemethode
- **Traditionele login** (alleen PVE)  
- **API Token** (verplicht voor PBS)

---

## 🔐 Optie A: Inloggen met Gebruiker (zonder Token)

Alleen geldig voor **PVE**.

Velden:

- **Gebruiker:** `gebruiker@realm`  
Voorbeelden:  
- `homeassistant@pve`  
- `root@pam`  
- **Wachtwoord:** het wachtwoord van de gebruiker  
- **Node Name:** naam van de node (zoals deze in Proxmox verschijnt)

---

## 🔐 Optie B: Inloggen met Token (aanbevolen en verplicht voor PBS)

Velden:

- **Gebruiker:** `gebruiker@realm`  
- **token_id:** alleen de token-naam → `ha-token`  
*(Voeg niet `gebruiker@pve!token` in)*  
- **Token_secret:** het door Proxmox gegenereerde Secret  

---

## ✅ Selectie van Entiteiten (alleen in PVE)

Na het verbinden scant de integratie je server en kun je kiezen wat je wilt monitoren:

- **VM's**  
- **CT's**  
- **Fysieke schijven**  
- **Storage**

> [!TIP]  
> Selecteer alleen wat je nodig hebt om Home Assistant schoon en snel te houden.

---

## 🧭 Visuele Installatiegids

**Hieronder vind je een complete visuele rondleiding door het configuratieproces, inclusief inlogmethoden, resource-selectie en configuratiestappen.**

<details>
  <summary>🪪 Schermafbeelding: Serververbinding</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Gebruik geen "http://" of "https://". We regelen dat al voor je.
</details>

<details>
  <summary>🪪 Schermafbeelding: Inloggen via Gebruiker en Wachtwoord (alleen PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Zorg ervoor dat je het realm `pam` of `pve` gebruikt volgens je gebruikersconfiguratie.
</details>

<details> 
  <summary>🪪 Schermafbeelding: Inloggen via Gebruiker en Token (PVE en PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **In het veld Token_id alleen de token-naam invoeren**
</details>

<details>
  <summary>⚙️ Schermafbeelding: Resource-selectie</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Opmerking: Selecteer de CT's, VM's en Storage die je wilt toevoegen, evenals de opties*
</details>

---

## ⚠️ Belangrijke opmerking voor PBS in gedeelde omgevingen (Tuxis, Hetzner, etc.)

Als je een **beheerde** of **multi‑tenant** PBS gebruikt, zoals Tuxis Free PBS:

- Je zult geen hardware-sensoren zien  
- Je zult geen temperaturen zien  
- Je zult geen fysieke schijven zien  
- Je zult geen node-metrics zien  

Dit is normaal omdat:

- Je geen toegang hebt tot de werkelijke hardware  
- De provider de infrastructuur verbergt  
- Je geen root-rechten hebt  
- Je geen toegang hebt tot het echte bestandssysteem  

**Resultaat:**  
De integratie toont alleen lege sensoren of geen gegevens.  
In toekomstige versies zullen we proberen aangepaste datastore-metrics te tonen.
