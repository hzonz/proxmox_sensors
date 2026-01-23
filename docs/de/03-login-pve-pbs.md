# 🔌 Schritt 3: Installation der Integration in Home Assistant

Um die Daten anzuzeigen (einschließlich der Hardware‑Temperaturen), verwenden wir die Integration **Proxmox Extended Sensors**.

## 1. Installation über HACS
Da es sich um eine benutzerdefinierte Integration handelt, müssen wir sie zuerst zu unserem HACS‑Store hinzufügen:

1. Gehe zu **HACS > Integrationen**.  
2. Klicke auf die drei Punkte oben rechts und wähle **Benutzerdefinierte Repositories**.  
3. Füge die URL dieses Repositories ein: `https://github.com/Javisen/proxmox_sensors/`  
4. Wähle unter **Kategorie** den Eintrag `Integration` und klicke auf **Hinzufügen**.  
5. Suche die Integration, installiere sie und **starte Home Assistant neu**.

## 2. Konfiguration der Integration
Nach dem Neustart folge diesen Schritten:

1. Gehe zu **Einstellungen > Geräte & Dienste**.  
2. Klicke auf **Integration hinzufügen** und suche nach `Proxmox Extended Sensors`.

## 3. Verbindungsdaten
Das Login‑Formular ist sehr einfach, aber achte auf folgende Punkte:

* **Host:**  
  * Im lokalen Netzwerk: Gib nur die IP ein (z. B. `192.168.1.50`). **Der Port ist nicht erforderlich**.  
  * Von außen: Gib deine Domain ein. **Schreibe kein `http://` oder `https://`**, die Integration erkennt dies automatisch.
* **Servertyp:** Wähle zwischen **PVE** (Proxmox Virtual Environment) oder **PBS** (Proxmox Backup Server).  
* **Token verwenden:** Wähle aus, ob du das im Schritt 2 erstellte API‑Token oder ein klassisches Login verwenden möchtest.

### Option A: Login mit Benutzer (ohne Token)
Wenn du kein Token verwenden möchtest, fülle diese Felder aus:

* **User:** Immer im Format `benutzer@realm` (z. B. `homeassistant@pve` oder `root@pam`).  
* **Password:** Das Passwort des Benutzers.  
* **Node Name:** Der Name deines Proxmox‑Nodes (der im linken Baum der Proxmox‑Weboberfläche erscheint).

### Option B: Login mit Token (Pflicht bei PBS)
Wenn du ein Token verwenden möchtest, fülle diese Felder aus:

* **User:** Immer im Format `benutzer@realm` (z. B. `homeassistant@pve` oder `root@pam`).  
* **token_id:** Der Name, den du dem Token gegeben hast (z. B. `ha-token`). Nicht mit der vollständigen Token‑ID verwechseln.  
* **Token_secret:** Die geheime Zeichenkette, die Proxmox generiert hat.

---

## ✅ Auswahl der Entitäten (NUR IN PVE‑UMGEBUNGEN)
Nachdem du auf „Senden“ klickst, scannt die Integration (im PVE‑Modus) deinen Server und lässt dich auswählen, was du überwachen möchtest:

* **VMs:** Bestimmte virtuelle Maschinen.  
* **CTs:** LXC‑Container.  
* **Physische Festplatten:** Angeschlossene HDDs und SSDs.  
* **Storages:** Speicherbereiche und deren freien Platz.

> [!TIP]
> **Wähle nur das aus, was du wirklich benötigst.**  
> Das hält dein Home Assistant sauber und verbessert die Leistung.

---

## ⚠️ Wichtiger Hinweis für PBS in Shared‑Hosting‑Umgebungen (z. B. Tuxis)

Wenn du die kostenlose Version von **Tuxis** oder ähnliche Managed‑PBS‑Anbieter nutzt, musst du verstehen, dass die Integration dort wichtige Einschränkungen hat.  
Der Grund: Deine PBS‑Instanz läuft in einer **Shared‑Hosting‑Umgebung (Multi‑Tenant)** und nicht auf einem dedizierten Server.

### Warum wirst du nicht alle Sensoren sehen?
Im Gegensatz zu einem lokalen Proxmox‑Server gilt hier:

* **Kein Zugriff auf echte Hardware:** Kein Zugriff auf das reale Dateisystem oder physische Datenträger.  
* **Versteckte Infrastruktur:** Das Backend (Ceph/ZFS), das der Anbieter nutzt, ist nicht einsehbar.  
* **Privatsphäre & Sicherheit:** Der Anbieter blockiert globale Systemmetriken, damit Kunden keine Rückschlüsse auf andere Nutzer oder die Gesamtlast ziehen können.  
* **Keine Root‑Rechte:** Ohne Zugriff auf `/` können keine Temperatur‑ oder Lüftersensoren des Nodes ausgelesen werden.

**Ergebnis:** In diesen Fällen zeigt die Integration keine Hardwaredaten an, sondern nur leere Sensoren.  
Wir arbeiten daran, in zukünftigen Versionen zumindest die persönlichen Datacenter‑Informationen anzuzeigen.
