# 🔌 Stap 3: Installatie van de integratie in Home Assistant

Om de gegevens (inclusief hardwaretemperaturen) te visualiseren, gebruiken we de integratie **Proxmox Extended Sensors**.

## 1. Installatie via HACS
Aangezien dit een aangepaste integratie is, moeten we deze eerst toevoegen aan onze HACS-winkel:

1. Ga naar **HACS > Integraties**.
2. Klik op de drie puntjes in de rechterbovenhoek en selecteer **Aangepaste repositories**.
3. Plak de URL van deze repository: `https://github.com/Javisen/proxmox_sensors/`
4. Selecteer bij **Categorie** `Integratie` en klik op **Toevoegen**.
5. Zoek de integratie, installeer deze en **herstart Home Assistant**.

## 2. Configuratie van de integratie
Volg na het herstarten deze stappen:

1. Ga naar **Instellingen > Apparaten & diensten**.
2. Klik op **Integratie toevoegen** en zoek naar `Proxmox Extended Sensors`.

## 3. Verbindingsgegevens
Het inlogformulier is heel eenvoudig, maar let op deze details:

* **Host:** * Indien in je lokale netwerk: Vul alleen het IP-adres in (bijv. `192.168.1.50`). **Het poortnummer is niet nodig**.
    * Indien toegang van buitenaf: Vul je domein in. **Schrijf geen `http://` of `https://`**, de integratie detecteert dit automatisch.
* **Servertype:** Kies tussen **PVE** (Proxmox Virtual Environment) of **PBS** (Proxmox Backup Server).
* **Token gebruiken:** Selecteer of je de API-token gebruikt die in Stap 2 is aangemaakt of de traditionele login.

### Optie A: Inloggen met gebruiker (Zonder Token)
Als je liever geen token gebruikt, vul dan deze velden in:
* **User:** Altijd in het formaat `gebruiker@realm` (bijvoorbeeld: `homeassistant@pve` of `root@pam`).
* **Password:** Het wachtwoord van de gebruiker.
* **Node Name:** De naam van je Proxmox-node (zoals deze verschijnt in de boomstructuur aan de linkerkant in de Proxmox-webinterface).

### Optie B: Inloggen met Token (Verplicht voor PBS)
Als je liever een token gebruikt, vul dan deze velden in:
* **User:** Altijd in het formaat `gebruiker@realm` (bijvoorbeeld: `homeassistant@pve` of `root@pam`).
* **token_id:** De identificatienaam die je aan de token hebt gegeven (bijvoorbeeld: `ha-token`). Niet te verwarren met de volledige ID.
* **Token_secret:** de tekenreeks (secret) die Proxmox heeft gegenereerd.

---

## ✅ Selectie van entiteiten (ALLEEN IN PVE-OMGEVING)
Zodra je op verzenden klikt, scant de integratie (in PVE-modus) je server en kun je kiezen wat je wilt monitoren:
* **VM's:** Specifieke virtuele machines.
* **CT's:** LXC-containers.
* **Fysieke schijven:** Aangesloten harde schijven en SSD's.
* **Storages:** Opslagpartities en hun vrije ruimte.

> [!TIP]
> **Selecteer alleen wat je echt nodig hebt.** Dit houdt je Home Assistant schoon en zorgt voor betere prestaties.

## ⚠️ Belangrijke opmerking voor PBS in gedeelde omgevingen (bijv. Tuxis)

Als je de gratis versie van **Tuxis** of soortgelijke providers van managed PBS gebruikt, moet je begrijpen dat de integratie belangrijke beperkingen zal hebben. Dit komt doordat je PBS-instantie draait in een **gedeelde omgeving (Multi-tenant)** en niet op een dedicated server.

### Waarom zie je niet alle sensoren?
In tegenstelling tot een lokale Proxmox, geldt bij deze diensten:
* **Geen toegang tot echte hardware:** Je hebt geen toegang tot het echte bestandssysteem of de directe fysieke opslag.
* **Verborgen infrastructuur:** Je kunt de backend (Ceph/ZFS) die zij gebruiken niet monitoren, aangezien deze eigendom is van de provider.
* **Privacy en beveiliging:** De provider blokkeert de toegang tot globale systeemstatistieken om te voorkomen dat een klant informatie kan afleiden over andere gebruikers of over de totale belasting van hun infrastructuur.
* **Geen Root-rechten:** Omdat er geen toegang is tot de root (`/`) van het systeem, kunnen er geen gegevens worden opgehaald van temperatuursensoren of ventilatorsnelheden van de node.

**Resultaat:** In deze gevallen zal de integratie niets tonen, enkel sensoren zonder informatie. We zullen eraan werken om in toekomstige versies te proberen de gegevens van het persoonlijke datacenter weer te geven.
