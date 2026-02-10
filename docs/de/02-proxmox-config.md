# 🔐 Schritt 2: Benutzer- und Berechtigungskonfiguration

**Damit Home Assistant sicher mit Proxmox kommunizieren kann, wird empfohlen, nicht den root-Benutzer zu verwenden. Wir erstellen einen dedizierten Benutzer und weisen die notwendigen Berechtigungen zu, damit die Integration zu 100% funktioniert.**

> ⚠️ **WICHTIG:**  
> Aufgrund der erweiterten Funktionen der Integration (Steuerung von VMs/CTs, Einzel- und Massen-Backups, PBS-Aktionen…) ist es notwendig, **Administratorberechtigungen** sowohl in PVE als auch in PBS zuzuweisen.

---

## 1. Unterschied zwischen PVE und PBS

### **Proxmox VE (PVE)**
- Sie können **Benutzer/Passwort** oder **API-Token** verwenden.  
- Der Benutzer muss die Rolle **PVEAdmin** haben.

### **Proxmox Backup Server (PBS)**
- Es ist **zwingend erforderlich**, einen **API-Token** zu verwenden.  
- Der Benutzer muss die Rolle **Administrator** haben (PBS verfügt nicht über eine gültige Zwischenrolle).

---

## 2. Benutzererstellung

1. Gehen Sie zu **Datacenter → Permissions → Users**  
2. Klicken Sie auf **Add**  
3. Konfigurieren Sie:  
   - **User:** `homeassistant`  
   - **Realm:** `pve`  
   - **Password:** nur wenn Sie die Passwort-Anmeldung in PVE verwenden möchten  
4. Speichern Sie die Änderungen

---

## 3. Zuweisung der korrekten Rolle

1. Gehen Sie zu **Datacenter → Permissions**  
2. Klicken Sie auf **Add → User Permission**  
3. Konfigurieren Sie die folgenden Felder:

### ✔ Für PVE:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

### ✔ Für PBS:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

> 💡 **Warum `/` notwendig ist:**  
> Die Integration benötigt globalen Zugriff, um Nodes, VMs, CTs, Festplatten, Datastores und Aufgaben zu lesen.

---

## 4. API-Token-Generierung (Obligatorisch für PBS)

1. Gehen Sie zu **Datacenter → Permissions → API Tokens**  
2. Klicken Sie auf **Add**  
3. Konfigurieren Sie:  
   - **User:** `homeassistant@pve`  
   - **Token ID:** `ha-token`  
   - **Privilege Separation:** **nicht angekreuzt**  
   - **Expire:** **Never**  
4. Bei der Erstellung des Tokens zeigt Proxmox an:  
   - **Token ID**  
   - **Secret** (nur einmal angezeigt)

> [!WARNING]
> **Kopieren Sie das "Secret" jetzt und bewahren Sie es an einem sicheren Ort auf.** Sobald Sie dieses Fenster schließen, zeigt Proxmox es aus Sicherheitsgründen nie wieder an.

> [!TIP]
> ### 💡 Haben Sie vergessen, das Secret zu kopieren?
> Keine Sorge. Obwohl Proxmox es aus Sicherheitsgründen nicht wieder anzeigt, müssen Sie den Token nicht löschen und von vorne beginnen:
> 
> 1. Wählen Sie in der **API Tokens**-Liste den bereits erstellten Token aus.
> 2. Klicken Sie auf die Schaltfläche **Regenerate**.
> 3. Das System macht den alten Schlüssel sofort ungültig und gibt Ihnen ein **neues Secret**.
> 
> *Denken Sie daran: Wenn Sie das Secret regenerieren, müssen Sie es in der Home Assistant-Konfiguration aktualisieren, damit die Integration wieder eine Verbindung herstellen kann.*
