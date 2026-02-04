# 🚀 Étape 1 : Installation et configuration des capteurs

**Ce guide explique comment préparer le nœud Proxmox pour qu'il expose les données matérielles et garantisse que les lectures de température soient disponibles pour Home Assistant.**


## 1. Installation des dépendances

* **Tout d'abord, nous installons les outils nécessaires pour lire los capteurs intégrés à la carte mère et au processeur :**


```bash

apt update && apt install lm-sensors -y

```

## 2. Détection du matériel

* **Pour que le système identifie les pilotes (drivers) dont il a besoin, nous exécutons l'assistant de détection :**


```bash

sensors-detect

```

**Répondez YES (ou appuyez sur Entrée) à toutes les questions. À la fin, le système identifiera les modules nécessaires (par exemple : `coretemp` pour les processeurs Intel).**


## 3. Persistance des modules

**Pour que les capteurs s'activent d'eux-mêmes au redémarrage du serveur, l'assistant `sensors-detect` vous posera une question clé à la fin du processus :**


`Do you want to add these lines automatically to /etc/modules? (yes/NO)`



> [!CAUTION]
> **Vous devez écrire `yes` manuellement et appuyer sur Entrée.** Si vous appuyez seulement sur Entrée sans rien écrire, le système sélectionnera `NO` par défaut. Si cela se produit, les capteurs ne seront pas chargés après un redémarrage et Home Assistant cessera de recevoir les données de température.



## 4. Vérification immédiate

**Pour activer les capteurs dès maintenant sans avoir à redémarrer, exécutez :**



```bash

# Charge les modules détectés (exemple pour Intel)

modprobe coretemp

# Vérifie que les températures s'affichent

sensors

```
## 🚀 Étape 5 : Installation du serveur de capteurs (API Bridge)
**L'API officielle de Proxmox n'exposant pas toutes les données matérielles, il est nécessaire d'installer ce petit script "pont" sur l'hôte Proxmox.**

1. **Téléchargement et installation du script**
Exécutez ces commandes dans le terminal de votre serveur Proxmox :
```bash
# Télécharger le script depuis le dépôt
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Donner les permissions d'exécution
chmod +x /usr/local/bin/pve-sensors-api.py
```

2. **Configuration en tant que service système**
Pour que le script démarre automatiquement avec le serveur, créez le fichier de service :
```bash
cat <<EOF > /etc/systemd/system/pve-sensors.service
[Unit]
Description=PVE Sensors API
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

3. **Activation immédiate**
Activez et démarrez le service avec ces commandes :
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
```

4. **Vérification finale**
Vous pouvez vérifier que le serveur fonctionne en ouvrant cette adresse dans votre navigateur (en remplaçant par l'IP de votre Proxmox) : `http://VOTRE_IP_PROXMOX:9000/sensors`

Si vous voyez un texte au format JSON avec les températures, l'intégration pourra désormais lire les données correctement.

---

**Terminé ! Une fois que la commande `sensors` renvoie des données dans le terminal, votre intégration Home Assistant pourra les lire automatiquement via l'API de Proxmox.**
