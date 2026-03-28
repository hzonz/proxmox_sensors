# 🔐 Schritt 2: Benutzer- und Berechtigungskonfiguration

Damit Home Assistant sicher mit Proxmox kommunizieren kann, wird empfohlen, **nicht den Root-Benutzer zu verwenden**.

Stattdessen erstellen wir einen dedizierten Benutzer mit den erforderlichen Berechtigungen, damit die Integration ordnungsgemäß funktioniert.

---

> ⚠️ **WICHTIG**  
> Aufgrund der erweiterten Funktionen der Integration (VM/CT-Steuerung, Backups, PBS-Aktionen usw.) ist es erforderlich, erhöhte Berechtigungen in Proxmox zu vergeben.
>
> Diese Berechtigungen ermöglichen:
> - Steuerung von virtuellen Maschinen und Containern  
> - Durchführung von Backups (einzeln und massenhaft)  
> - Zugriff auf Knoten-, Festplatten- und Aufgabeninformationen  
> - Interaktion mit Proxmox Backup Server (PBS)  
>
> Auch wenn es sich um umfangreiche Berechtigungen handelt, hält die Verwendung eines **dedizierten Benutzers + API-Tokens** den Zugriff isoliert und kontrolliert.

---

## 1. Unterschied zwischen PVE und PBS

### 🖥️ Proxmox VE (PVE)
- Ermöglicht Authentifizierung über:
  - Benutzername/Passwort  
  - API-Token  
- Der Benutzer muss die Rolle **PVEAdmin** haben  

---

### 🗄️ Proxmox Backup Server (PBS)
- Erfordert zwingend einen **API-Token**  
- Der Benutzer muss die Rolle **Administrator** haben  
- Es gibt keine mittlere Rolle, die mit allen Funktionen kompatibel ist  

---

## 2. Erstellen des Benutzers

1. Gehe zu **Datacenter → Permissions → Users**  
2. Klicke auf **Add**  
3. Konfiguriere:

- **User:** `homeassistant`  
- **Realm:** `pve`  
- **Password:** (nur wenn du Passwort-Login für PVE verwenden möchtest)

4. Speichere die Änderungen  

---

## 3. Zuweisen der Berechtigungen

1. Gehe zu **Datacenter → Permissions**  
2. Klicke auf **Add → User Permission**  

---

### ✔ Für Proxmox VE (PVE)

- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

---

### ✔ Für Proxmox Backup Server (PBS)

- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

---

> 💡 **Warum `/` (globaler Zugriff) verwenden?**  
> Die Integration benötigt Zugriff auf die gesamte Infrastruktur:
> Knoten, VMs, Container, Festplatten, Speicher und Aufgaben.

---

## 4. Erstellen des API-Tokens

1. Gehe zu **Datacenter → Permissions → API Tokens**  
2. Klicke auf **Add**  
3. Konfiguriere:

- **User:** `homeassistant@pve`  
- **Token ID:** `ha-token`  
- **Privilege Separation:** ❌ Deaktiviert  
- **Expire:** Never  

---

### 🔍 Warum "Privilege Separation" deaktivieren?

Weil das Token die vollständigen Berechtigungen des Benutzers erben muss.

Wenn diese Option aktiviert ist:
- hat das Token eingeschränkte Berechtigungen  
- funktionieren einige Funktionen (Backups, Steuerung, PBS) nicht korrekt  

---

4. Beim Erstellen des Tokens zeigt Proxmox an:

- **Token ID**  
- **Secret** (nur einmal sichtbar)

---

> [!WARNING]
> Speichere das **Secret** an einem sicheren Ort.  
> Es kann nach dem Schließen dieses Fensters nicht mehr eingesehen werden.

---

> [!TIP]
> ### 💡 Hast du vergessen, das Secret zu kopieren?
> Es ist nicht nötig, das Token zu löschen:
>
> 1. Wähle das Token in der Liste aus  
> 2. Klicke auf **Regenerate**  
> 3. Ein neues Secret wird sofort generiert  
>
> ⚠️ Denke daran, es in Home Assistant zu aktualisieren.

---

## ✔ Fazit

Nach der Konfiguration:

- Dedizierter Benutzer  
- Berechtigungen korrekt zugewiesen  
- API-Token erstellt  

Kann sich die Integration sicher mit Proxmox verbinden und hat vollen Zugriff auf alle Funktionen.