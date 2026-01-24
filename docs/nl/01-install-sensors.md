# 🚀 Stap 1: Installatie en configuratie van sensoren

**Deze handleiding legt uit hoe je de Proxmox-node voorbereidt om hardwaregegevens bloot te stellen en ervoor te zorgen dat temperatuurmetingen beschikbaar zijn voor Home Assistant.**


## 1. Installatie van afhankelijkheden

* **Eerst installeren we de benodigde tools om de sensoren uit te lezen die zijn ingebouwd in het moederbord en de CPU:**


```bash

apt update && apt install lm-sensors -y

```

## 2. Hardware detectie

* **Om het systeem te laten identificeren welke stuurprogramma's (drivers) het nodig heeft, voeren we de detectie-assistent uit:**


```bash

sensors-detect

```

**Antwoord YES (of druk op Enter) op alle vragen. Aan het einde van het proces identificeert het systeem de benodigde modules (bijvoorbeeld: `coretemp` voor Intel CPU's).**


## 3. Persistentie van modules

**Om ervoor te zorgen dat de sensoren automatisch worden geactiveerd bij het herstarten van de server, stelt de assistent `sensors-detect` aan het einde van het proces een cruciale vraag:**


`Do you want to add these lines automatically to /etc/modules? (yes/NO)`



> [!CAUTION]
> **Je moet handmatig `yes` typen en op Enter drukken.** Als je alleen op Enter drukt zonder iets te typen, selecteert het systeem standaard `NO`. Als dit gebeurt, worden de sensoren na een herstart niet geladen en ontvangt Home Assistant geen temperatuurgegevens meer.



## 4. Onmiddellijke verificatie

**Om de sensoren nu direct te activeren zonder te herstarten, voer je het volgende uit:**



```bash

# Laad de gedetecteerde modules (voorbeeld voor Intel)

modprobe coretemp

# Controleer of de temperaturen worden weergegeven

sensors

```



**Klaar! Zodra het commando `sensors` gegevens teruggeeft in de terminal, kan je Home Assistant-integratie deze automatisch uitlezen via de Proxmox API.**
