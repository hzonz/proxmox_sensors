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



**Terminé ! Une fois que la commande `sensors` renvoie des données dans le terminal, votre intégration Home Assistant pourra les lire automatiquement via l'API de Proxmox.**
