# 🔌 Étape 3 : Installation de l'intégration dans Home Assistant

Pour visualiser les données (y compris les températures matérielles), nous utiliserons l'intégration **Proxmox Extended Sensors**.

## 1. Installation via HACS
S'agissant d'une intégration personnalisée, nous devons d'abord l'ajouter à notre boutique HACS :

1. Allez dans **HACS > Intégrations**.
2. Cliquez sur les trois points dans le coin supérieur droit et sélectionnez **Dépôts personnalisés**.
3. Collez l'URL de ce dépôt : `https://github.com/Javisen/proxmox_sensors/`
4. Dans **Catégorie**, sélectionnez `Intégration` et cliquez sur **Ajouter**.
5. Recherchez l'intégration, installez-la et **redémarrez Home Assistant**.

## 2. Configuration de l'intégration
Une fois redémarré, suivez ces étapes :

1. Allez dans **Paramètres > Appareils et services**.
2. Cliquez sur **Ajouter l'intégration** et recherchez `Proxmox Extended Sensors`.

## 3. Données de connexion
Le formulaire de connexion est très simple, mais portez une attention particulière à ces détails :

* **Host :** * Si c'est sur votre réseau local : Indiquez uniquement l'IP (ex. `192.168.1.50`). **Il n'est pas nécessaire de préciser le port**.
    * Si vous y accédez de l'extérieur : Indiquez votre domaine. **N'écrivez ni `http://` ni `https://`**, l'intégration le détecte automatiquement.
* **Type de serveur :** Choisissez entre **PVE** (Proxmox Virtual Environment) ou **PBS** (Proxmox Backup Server).
* **Utiliser un Token :** Sélectionnez si vous allez utiliser le Token API créé à l'Étape 2 ou une connexion traditionnelle.

### Option A : Connexion avec Utilisateur (Sans Token)
Si vous préférez ne pas utiliser de token, remplissez ces champs :
* **User :** Toujours au format `utilisateur@realm` (exemple : `homeassistant@pve` ou `root@pam`).
* **Password :** Le mot de passe de l'utilisateur.
* **Node Name :** Le nom de votre nœud Proxmox (celui qui apparaît dans l'arborescence à gauche sur l'interface web de Proxmox).

### Option B : Connexion avec Token (Obligatoire pour PBS)
Si vous préférez utiliser un token, remplissez ces champs :
* **User :** Toujours au format `utilisateur@realm` (exemple : `homeassistant@pve` ou `root@pam`).
* **token_id :** Le nom identifiant que vous avez donné au token (exemple : `ha-token`). Ne pas confondre avec l'ID complet.
* **Token_secret :** La chaîne de caractères (secret) générée par Proxmox.

---

## ✅ Sélection des entités (ENVIRONNEMENT PVE UNIQUEMENT)
Une fois que vous aurez cliqué sur envoyer, l'intégration (en mode PVE) scannera votre serveur et vous permettra de choisir ce que vous souhaitez surveiller :
* **VMs :** Machines virtuelles spécifiques.
* **CTs :** Conteneurs LXC.
* **Disques physiques :** Disques durs et SSD connectés.
* **Storages :** Partitions de stockage et leur espace libre.

> [!TIP]
> **Ne sélectionnez que ce dont vous avez réellement besoin.** Cela permettra de garder votre Home Assistant propre et performant.

## ⚠️ Note importante pour PBS en environnements partagés (Ex. Tuxis)

Si vous utilisez la version gratuite de **Tuxis** ou des fournisseurs similaires de PBS managé, vous devez comprendre que l'intégration aura des limitations importantes. Cela est dû au fait que votre instance PBS s'exécute dans un **environnement partagé (Multi-tenant)** et non sur un serveur dédié.

### Pourquoi ne verrez-vous pas tous les capteurs ?
Contrairement à un Proxmox local, sur ces services :
* **Pas d'accès au matériel réel :** Vous n'avez pas accès au système de fichiers réel ni au stockage physique direct.
* **Infrastructure cachée :** Vous ne pouvez pas surveiller le backend (Ceph/ZFS) qu'ils utilisent, car il appartient au fournisseur.
* **Confidentialité et sécurité :** Le fournisseur bloque l'accès aux métriques globales du système pour empêcher un client de déduire des informations sur d'autres utilisateurs ou sur la charge totale de l'infrastructure.
* **Sans permissions Root :** N'ayant pas accès à la racine (`/`) du système, il est impossible d'extraire les données des capteurs de température ou de vitesse des ventilateurs du nœud.

**Résultat :** Dans ces cas, l'intégration n'affichera rien, seulement des capteurs sans information. Nous travaillerons pour essayer d'afficher les données du datacenter personnel dans les versions futures.
