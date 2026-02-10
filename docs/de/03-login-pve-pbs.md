# 🔌 Schritt 3: Installation der Integration in Home Assistant

Um die Daten (einschließlich Temperaturen, Hardware-Sensoren, Festplatten, PBS, VMs und CTs) anzuzeigen, verwenden wir die Integration **Proxmox Extended Sensors**.

[Visuelle Installationsanleitung](#-Visuelle-Installationsanleitung)

---

## 1. Installation über HACS

Da es sich um eine benutzerdefinierte Integration handelt, müssen wir sie zuerst zu HACS hinzufügen:

1. Gehen Sie zu **HACS → Integrationen**  
2. Klicken Sie auf die **drei Punkte** (oben rechts)  
3. Wählen Sie **Benutzerdefinierte Repositorys**  
4. Fügen Sie dieses Repository hinzu: `https://github.com/Javisen/proxmox_sensors/`
5. Wählen Sie in **Kategorie** `Integration`  
6. Installieren Sie sie und **starten Sie Home Assistant neu**

---

## 2. Konfiguration der Integration

Nach dem Neustart:

1. Gehen Sie zu **Einstellungen → Geräte & Dienste**  
2. Klicken Sie auf **Integration hinzufügen**  
3. Suchen Sie nach **Proxmox Extended Sensors**

---

## 3. Verbindungsdaten

Das Formular ist einfach, aber es gibt wichtige Details:

### 🔹 Host
- **Im lokalen Netzwerk:** nur die IP → `192.168.1.50`  
*(Keinen Port oder http/https angeben)*  
- **Von außen:** Ihre Domain → `proxmox.meinedomain.com`  
*(Die Integration erkennt http/https automatisch)*

### 🔹 Servertyp
- **PVE** → Proxmox Virtual Environment  
- **PBS** → Proxmox Backup Server  

### 🔹 Authentifizierungsmethode
- **Traditionelle Anmeldung** (nur PVE)  
- **API-Token** (obligatorisch für PBS)

---

## 🔐 Option A: Anmeldung mit Benutzer (ohne Token)

Nur gültig für **PVE**.

Felder:

- **Benutzer:** `benutzer@realm`  
Beispiele:  
- `homeassistant@pve`  
- `root@pam`  
- **Passwort:** das Passwort des Benutzers  
- **Knotenname:** Knotenname (wie in Proxmox angezeigt)

---

## 🔐 Option B: Anmeldung mit Token (empfohlen und obligatorisch für PBS)

Felder:

- **Benutzer:** `benutzer@realm`  
- **token_id:** nur der Token-Name → `ha-token`  
*(Nicht `benutzer@pve!token` angeben)*  
- **Token_secret:** das von Proxmox generierte Secret  

---

## ✅ Auswahl der Entitäten (nur in PVE)

Nach der Verbindung scannt die Integration Ihren Server und Sie können auswählen, was überwacht werden soll:

- **VMs**  
- **CTs**  
- **Physische Festplatten**  
- **Speicher**

> [!TIP]  
> Wählen Sie nur das aus, was Sie benötigen, um Home Assistant sauber und schnell zu halten.

---

## 🧭 Visuelle Installationsanleitung

**Unten finden Sie eine vollständige visuelle Schritt-für-Schritt-Anleitung des Konfigurationsprozesses, einschließlich Anmeldemethoden, Ressourcenauswahl und Konfigurationsschritte.**

<details>
  <summary>🪪 Screenshot: Serververbindung</summary>
  <p align="center">
    <img src="../../img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > Verwenden Sie nicht "http://" oder "https://". Das übernehmen wir bereits für Sie.
</details>

<details>
  <summary>🪪 Screenshot: Anmeldung über Benutzer und Passwort (nur PVE)</summary>
  <p align="center">
    <img src="../../img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Stellen Sie sicher, dass Sie die Realm `pam` oder `pve` entsprechend Ihrer Benutzerkonfiguration verwenden.
</details>

<details> 
  <summary>🪪 Screenshot: Anmeldung über Benutzer und Token (PVE und PBS)</summary>
  <p align="center">
    <img src="../../img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **Im Feld Token_id wird nur der Token-Name eingegeben**
</details>

<details>
  <summary>⚙️ Screenshot: Ressourcenauswahl</summary>
  <p align="center">
    <img src="../../img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Hinweis: Wählen Sie die CTs, VMs und Speicher aus, die Sie hinzufügen möchten, sowie die Optionen*
</details>

---

## ⚠️ Wichtiger Hinweis für PBS in gemeinsam genutzten Umgebungen (Tuxis, Hetzner usw.)

Wenn Sie einen **verwalteten** oder **Multi‑Tenant** PBS verwenden, wie z.B. Tuxis Free PBS:

- Sie werden keine Hardware-Sensoren sehen  
- Sie werden keine Temperaturen sehen  
- Sie werden keine physischen Festplatten sehen  
- Sie werden keine Knotenmetriken sehen  

Das ist normal, weil:

- Sie keinen Zugriff auf die tatsächliche Hardware haben  
- Der Anbieter die Infrastruktur verbirgt  
- Sie keine Root-Berechtigungen haben  
- Sie nicht auf das echte Dateisystem zugreifen können  

**Ergebnis:**  
Die Integration zeigt nur leere Sensoren oder keine Daten an.  
In zukünftigen Versionen werden wir versuchen, benutzerdefinierte Datastore-Metriken anzuzeigen.
