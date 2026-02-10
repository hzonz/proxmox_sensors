# 🔐 Stap 2: Gebruikers- en Machtigingsconfiguratie

**Om Home Assistant veilig met Proxmox te laten communiceren, wordt aanbevolen niet de root-gebruiker te gebruiken. We maken een speciale gebruiker aan en kennen de benodigde machtigingen toe zodat de integratie voor 100% werkt.**

> ⚠️ **BELANGRIJK:**  
> Vanwege de geavanceerde functies van de integratie (beheer van VM's/CT's, individuele en massale backups, PBS-acties…) is het nodig om **beheerdersmachtigingen** toe te kennen in zowel PVE als PBS.

---

## 1. Verschil tussen PVE en PBS

### **Proxmox VE (PVE)**
- Je kunt **Gebruiker/Wachtwoord** of **API Token** gebruiken.  
- De gebruiker moet de rol **PVEAdmin** hebben.

### **Proxmox Backup Server (PBS)**
- Het is **verplicht** om een **API Token** te gebruiken.  
- De gebruiker moet de rol **Administrator** hebben (PBS heeft geen geldige tussenliggende rol).

---

## 2. Aanmaken van de Gebruiker

1. Ga naar **Datacenter → Permissions → Users**  
2. Klik op **Add**  
3. Configureer:  
   - **User:** `homeassistant`  
   - **Realm:** `pve`  
   - **Password:** alleen als je wachtwoordlogin in PVE gaat gebruiken  
4. Sla de wijzigingen op

---

## 3. Toekennen van de Juiste Rol

1. Ga naar **Datacenter → Permissions**  
2. Klik op **Add → User Permission**  
3. Configureer de volgende velden:

### ✔ Voor PVE:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

### ✔ Voor PBS:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

> 💡 **Waarom `/` nodig is:**  
> De integratie heeft wereldwijde toegang nodig om nodes, VM's, CT's, schijven, datastores en taken te lezen.

---

## 4. Genereren van API Token (Verplicht voor PBS)

1. Ga naar **Datacenter → Permissions → API Tokens**  
2. Klik op **Add**  
3. Configureer:  
   - **User:** `homeassistant@pve`  
   - **Token ID:** `ha-token`  
   - **Privilege Separation:** **uitgevinkt**  
   - **Expire:** **Never**  
4. Bij het aanmaken van het token laat Proxmox zien:  
   - **Token ID**  
   - **Secret** (slechts één keer getoond)

> [!WARNING]
> **Kopieer het "Secret" nu en bewaar het op een veilige plek.** Zodra je dit venster sluit, laat Proxmox het om veiligheidsredenen nooit meer zien.

> [!TIP]
> ### 💡 Ben je vergeten het Secret te kopiëren?
> Geen zorgen. Hoewel Proxmox het om veiligheidsredenen niet meer laat zien, hoef je het token niet te verwijderen en opnieuw te beginnen:
> 
> 1. Selecteer in de **API Tokens**-lijst het token dat je al had aangemaakt.
> 2. Klik op de knop **Regenerate**.
> 3. Het systeem maakt de oude sleutel direct ongeldig en geeft je een **nieuw Secret**.
> 
> *Onthoud dat als je het Secret regenereert, je dit moet bijwerken in de Home Assistant-configuratie zodat de integratie weer kan verbinden.*
