# 🔐 Stap 2: Configuratie van gebruikers en machtigingen
**Om Home Assistant veilig met Proxmox te laten communiceren, is het raadzaam om niet de root-gebruiker te gebruiken. In deze handleiding maken we een toegang aan met "alleen-lezen" machtigingen.**

## 1. Verschil tussen PVE en PBS
Voordat je begint, moet je rekening houden met het volgende:

* **Proxmox VE (PVE): Je kunt een conventionele gebruikersnaam/wachtwoord of een API-token gebruiken.**

* **Proxmox Backup Server (PBS): Het is essentieel om een API-token te gebruiken. Traditionele inlogmethoden falen vaak vanwege beveiligingsbeperkingen of machtigingen op de Datastore.**

---

## 2. Aanmaken van de Rol (Machtigingen)
**Een "Rol" definieert wat de integratie mag doen.**

1. Ga naar Datacenter > Permissions > Roles.

2. Klik op Create en geef het de naam HA-Monitor.

---

## 3. Aanmaken van de Rol (Machtigingen)
Een "Rol" definieert wat de integratie mag doen.
1. Ga naar **Datacenter > Permissions > Roles**.
2. Klik op **Create** en geef het de naam `HA-Monitor`.
3. Selecteer de volgende privileges (**Privileges**):
    * `Sys.Audit`: Hiermee kan de status van de node worden bekeken (CPU, RAM).
    * `VM.Audit`: Hiermee kan de status van de VM's en containers worden bekeken.
    * `Datastore.Audit`: Hiermee kan de schijfruimte worden bekeken.

---

## 4. Aanmaken van de Gebruiker
1. **Ga naar Datacenter > Permissions > Users.**

2. **Klik op Add.**

3. **User: homeassistant (je kunt het realm op pve laten staan).**

4. **Geef het een veilig wachtwoord als je deze methode voor PVE gaat gebruiken.**

---

## 5. Toewijzen van de Rol
**Je moet Proxmox vertellen dat die gebruiker de rol heeft die we hebben aangemaakt:**

1. Ga naar **Datacenter > Permissions**.
2. Klik op **Add > User Permission**.
3. Configureer de volgende velden:
    * **Path:** `/` (Dit is erg belangrijk zodat de integratie de hele server kan zien).
    * **User:** `homeassistant@pve` (of de gebruiker die je hebt aangemaakt).
    * **Role:** `HA-Monitor`.

---

## 6. Genereren van de API-token (Verplicht voor PBS)
**Als je een PBS gaat monitoren of liever geen wachtwoorden gebruikt in PVE, volg dan deze stappen:**

1. Ga naar **Datacenter > Permissions > API Tokens**.
2. Klik op **Add** en vul het formulier in:
    * **User:** Selecteer de gebruiker `homeassistant`.
    * **Token ID:** `ha-token` (je kunt elke gewenste naam kiezen).
    * **Privilege Separation:** ⚠️ **VINK DIT VAKJE UIT**. Als je dit aangevinkt laat, erft de Token de machtigingen van de gebruiker niet en zal de integratie falen.
3. Wanneer je op **Add** klikt, opent er een venster met twee belangrijke gegevens:
    * **Token ID:** (Voorbeeld: `homeassistant@pve!ha-token`).
    * **Secret:** (Een lange reeks letters en cijfers).

> [!WARNING]
> **Kopieer de "Secret" nu en bewaar deze op een veilige plek.** Zodra je dit venster sluit, zal Proxmox deze om veiligheidsredenen nooit meer laten zien.


> [!TIP]
> ### 💡 Ben je vergeten de Secret te kopiëren?
> Maak je geen zorgen. Hoewel Proxmox het om veiligheidsredenen niet meer laat zien, is het niet nodig om de token te verwijderen en opnieuw te beginnen:
> 
> 1. Selecteer in de lijst met **API Tokens** de token die je al had aangemaakt.
> 2. Klik op de knop **Regenerate**.
> 3. Het systeem zal de oude sleutel onmiddellijk ongeldig maken en je een **nieuwe Secret** geven.
> 
> *Vergeet niet dat als je de Secret regenereert, je deze moet bijwerken in de configuratie van Home Assistant zodat de integratie opnieuw verbinding kan maken.*
