# 🔐 Schritt 2: Benutzer- und Berechtigungskonfiguration
**Damit Home Assistant sicher mit Proxmox kommunizieren kann, ist es empfehlenswert, nicht den Benutzer root zu verwenden. In dieser Anleitung erstellen wir einen Zugriff mit „Nur-Lesen“-Rechten.**

## 1. Unterschied zwischen PVE und PBS
Bevor du beginnst, solltest du Folgendes beachten:

* **Proxmox VE (PVE): Du kannst einen normalen Benutzer/Passwort-Zugang oder ein API-Token verwenden.**

* **Proxmox Backup Server (PBS): Hier ist ein API-Token zwingend erforderlich. Herkömmliche Login-Methoden schlagen oft aufgrund von Sicherheitsbeschränkungen oder fehlenden Berechtigungen im Datastore fehl.**

---

## 2. Erstellung der Rolle (Berechtigungen)
**Eine „Rolle“ definiert, was die Integration tun darf.**

1. Gehe zu **Datacenter > Permissions > Roles**.
2. Klicke auf **Create** und gib der Rolle den Namen `HA-Monitor`.

---

## 3. Rollenerstellung (Berechtigungen)
Eine „Rolle“ definiert, was die Integration tun darf.

1. Gehe zu **Datacenter > Permissions > Roles**.  
2. Klicke auf **Create** und gib der Rolle den Namen `HA-Monitor`.  
3. Wähle folgende Privilegien (**Privileges**) aus:
    * `Sys.Audit`: Ermöglicht das Anzeigen des Node-Status (CPU, RAM).
    * `VM.Audit`: Ermöglicht das Anzeigen des Status von VMs und Containern.
    * `Datastore.Audit`: Ermöglicht das Anzeigen des Speicherplatzes.

---

## 4. Benutzererstellung
1. Gehe zu **Datacenter > Permissions > Users**.
2. Klicke auf **Add**.
3. **User:** `homeassistant` (Realm kann auf `pve` bleiben).
4. Vergib ein sicheres Passwort, falls du diese Methode für PVE verwenden möchtest.

---

## 5. Zuweisung der Rolle
**Jetzt musst du Proxmox mitteilen, dass dieser Benutzer die erstellte Rolle besitzt:**

1. Gehe zu **Datacenter > Permissions**.  
2. Klicke auf **Add > User Permission**.  
3. Konfiguriere folgende Felder:
    * **Path:** `/` (Sehr wichtig, damit die Integration den gesamten Server sehen kann).
    * **User:** `homeassistant@pve` (oder der Benutzer, den du erstellt hast).
    * **Role:** `HA-Monitor`.

---

## 6. Erstellung des API-Tokens (Pflicht für PBS)
**Wenn du einen PBS überwachen möchtest oder keine Passwörter in PVE verwenden willst, führe diese Schritte aus:**

1. Gehe zu **Datacenter > Permissions > API Tokens**.
2. Klicke auf **Add** und fülle das Formular aus:
    * **User:** Wähle den Benutzer `homeassistant`.
    * **Token ID:** `ha-token` (oder ein beliebiger Name).
    * **Privilege Separation:** ⚠️ **DEAKTIVIERE dieses Kontrollkästchen**.  
      Wenn es aktiviert bleibt, erbt das Token die Benutzerrechte nicht und die Integration schlägt fehl.
3. Nach dem Klick auf **Add** erscheint ein Fenster mit zwei wichtigen Informationen:
    * **Token ID:** (Beispiel: `homeassistant@pve!ha-token`)
    * **Secret:** (Eine lange Zeichenkette aus Buchstaben und Zahlen)

> [!WARNING]
> **Kopiere das „Secret“ jetzt und bewahre es sicher auf.**  
> Sobald du das Fenster schließt, zeigt Proxmox es aus Sicherheitsgründen nie wieder an.

---

> [!TIP]
> ### 💡 Secret vergessen?
> Kein Problem. Auch wenn Proxmox das Secret aus Sicherheitsgründen nicht erneut anzeigt, musst du das Token nicht löschen:
> 
> 1. Wähle in der Liste der **API Tokens** das bereits erstellte Token aus.  
> 2. Klicke auf **Regenerate**.  
> 3. Das alte Secret wird sofort ungültig und du erhältst ein **neues Secret**.  
> 
> *Denke daran: Wenn du das Secret regenerierst, musst du es auch in Home Assistant aktualisieren, damit die Integration wieder funktioniert.*
