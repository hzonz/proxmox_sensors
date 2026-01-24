# ❓ FAQ — Foire Aux Questions

Vous trouverez ci-dessous les doutes et les problèmes les plus courants lors de l'utilisation de l'intégration **Proxmox Sensors Extended**, ainsi que leurs solutions rapides.

---

## 🔐 Je ne peux pas me connecter à l'intégration (PVE ou PBS)

### ✔ 1. Ne mettez ni `http://` ni `https://`
Saisissez **uniquement le domaine ou l'IP**, par exemple :

`192.168.1.10`
`pve.mon-domaine.com`

---

### ✔ 2. Ne mettez pas le port
L'intégration détecte automatiquement le port correct.

### ✔ 3. Vérifiez les permissions du Token API
L'utilisateur doit avoir :

- **PVE :** - `Sys.Audit`  
  - `VM.Audit`  
  - `Datastore.Audit`  
  - `Permissions.Modify` (uniquement si vous utilisez la sélection automatique des VMs/LXCs)

- **PBS :** - `Datastore.Audit`  
  - `Datastore.Read`  
  - `Sys.Audit`

---

### ✔ 4. Assurez-vous que le Token est actif
Dans Proxmox → Datacenter → Permissions → API Tokens  
La mention **Enabled: Yes** doit apparaître.

---

## 🔑 Le message "Permission denied" s'affiche alors que le Token est correct

Cela est généralement dû à :

### ✔ 1. Le Token n'a pas de permissions sur la racine `/`
Dans Proxmox, les permissions doivent être assignées sur : `/ (root)` **et non sur un nœud spécifique.**

### ✔ 2. Le Token appartient à un utilisateur sans permissions
L'utilisateur parent doit avoir les permissions, pas seulement le Token.

---

## 🌐 L'intégration ne détecte pas mon PBS de chez Tuxis

C'est normal.

Les PBS gérés par Tuxis **ne permettent pas d'accéder aux métriques internes** via l'API :

- espace du datastore  
- utilisation du disque  
- statistiques RRD  
- matériel du nœud  
- température  
- SMART  
- CPU/RAM  

Ce n'est pas une erreur de l'intégration :  
Tuxis bloque ces points d'accès (endpoints) par conception.

L'intégration détecte automatiquement qu'il s'agit d'un PBS Tuxis et masque les capteurs non disponibles.

---

## 📦 Je ne vois pas les capteurs d'espace du datastore sur PBS

### ✔ Si votre PBS vient de Tuxis → **ils ne sont pas disponibles**
Pour des raisons de sécurité, Tuxis bloque : `/api2/json/admin/datastore/<name>/status`

Sans ce point d'accès, il est impossible d'obtenir :

- l'espace total  
- l'espace libre  
- le pourcentage d'utilisation  
- la déduplication  
- les chunks  
- le GC (Garbage Collector)

---

## 🌡️ Les capteurs de température n'apparaissent pas dans PVE

### ✔ 1. Vous devez installer `lm-sensors` sur le nœud
Guide complet : [01. Configuration des Capteurs Matériels](01-install-sensors.md)

### ✔ 2. Vous devez exécuter `sensors-detect`
Et accepter toutes les options sûres.

### ✔ 3. Vous devez charger les modules recommandados
Exemple :

```bash
modprobe coretemp
modprobe nct6775
```
### ✔ 4. Vous devez créer le service systemd
Pour que les capteurs fonctionnent après le redémarrage.

---

## 🖥️ Les capteurs de disques NVMe/SSD/HDD n'apparaissent pas
### ✔ 1. Le disque doit supporter la lecture de température
Certains modèles OEM n'exposent pas de capteurs.

### ✔ 2. Pas de capteurs sur les NVMe virtualisés (VMs)
Ils ne fonctionnent que sur le matériel réel.

### ✔ 3. Sur les PBS Tuxis, les capteurs de disque ne sont pas exposés
Limitation du fournisseur.

## 🧠 Mes VMs ou conteneurs n'apparaissent pas

### ✔ 1. Vérifiez les permissions du Token
Il doit avoir : `VM.Audit`

### ✔ 2. Si vous utilisez la sélection automatique
L'intégration nécessite : `Permissions.Modify`

### ✔ 3. Si vous utilisez un cluster
Vous devez vous connecter au nœud principal, et non à un nœud secondaire.

---

## 🔄 L'intégration met du temps à mettre à jour les valeurs
C'est normal.

L'intégration utilise le `DataUpdateCoordinator` pour :

* éviter de saturer l'API
* réduire la charge sur le nœud
* améliorer les performances

**L'intervalle par défaut est de 10 secondes, configurable.**

---

## 🧩 Puis-je utiliser plusieurs PVE et PBS en même temps ?
### Oui.
L'intégration permet d'ajouter plusieurs instances, chacune avec son propre Token.

---

## 🔒 Est-il sûr d'utiliser des Tokens API ?
### Oui.

L'intégration :

* ne stocke pas de mots de passe
* utilise uniquement des Tokens avec des permissions minimales
* n'exécute pas de commandes sur le serveur
* ne modifie pas la configuration de Proxmox
* n'ouvre pas de ports supplémentaires

---

## 🧹 Comment supprimer les anciens capteurs ?
**Home Assistant supprime automatiquement les entités orphelines.**

**Si vous souhaitez forcer le nettoyage :**

* Supprimez l'intégration
* Redémarrez Home Assistant
* Ajoutez-la de nouveau

---

## 🛠️ Où puis-je signaler des erreurs ?
**Vous pouvez ouvrir un "issue" sur GitHub en indiquant :**

* version de HA
* version de Proxmox
* logs pertinents
* étapes pour reproduire l'erreur
* type de serveur (PVE, PBS, Tuxis, etc.)

---

# 🧾 Checklist avant d'ouvrir un Issue

Avant de signaler un problème, vérifiez cette liste rapide.
90 % des erreurs sont résolues ici :

### ✔ 1. Pouvez-vous accéder à Proxmox depuis votre navigateur ?
Si vous ne pouvez pas entrer sur l'interface web de PVE/PBS, l'intégration ne le pourra pas non plus.

### ✔ 2. Utilisez-vous uniquement le domaine ou l'IP ?
Ne mettez pas `http://`, `https://` ni de ports.

### ✔ 3. Le Token API est-il actif ?
Dans Proxmox → Datacenter → Permissions → API Tokens
La mention **Enabled: Yes** doit apparaître.

### ✔ 4. L'utilisateur a-t-il des permissions sur la racine `/` ?
Les permissions doivent être assignées sur : `/ (root)` et non sur un nœud spécifique.

### ✔ 5. Avez-vous installé et configuré `lm-sensors` sur PVE ?
Sans cela, les capteurs matériels n'apparaîtront pas.

### ✔ 6. Le PBS est-il chez Tuxis ?
Si c'est le cas, rappelez-vous qu'il **n'expose pas de métriques internes** (espace, matériel, RRD).

### ✔ 7. Avez-vous redémarré Home Assistant après avoir modifié les permissions ?
HA met en cache les anciennes permissions.

### ✔ 8. Y a-t-il des erreurs dans les logs de Home Assistant ?
Allez dans :
**Paramètres → Journaux → Intégrations**

### ✔ 9. Avez-vous essayé en mode incognito ?
Le frontend de HA met en cache les ressources pendant des semaines.

---

# 🚫 Limitations Connues

Ces limitations ne sont pas des erreurs de l'intégration, mais des restrictions de Proxmox ou du fournisseur :

### 🔒 1. PBS de Tuxis
Les serveurs PBS gérés par Tuxis **ne permettent pas d'accéder à :**

- l'espace du datastore
- l'utilisation du disque
- la déduplication
- les chunks
- les statistiques RRD
- le matériel du nœud
- la température
- SMART
- CPU/RAM

L'intégration détecte automatiquement cette limitation et masque les capteurs non disponibles.

---

### 🧊 2. Capteurs matériels dans les machines virtuelles
Les VMs **n'exposent pas de capteurs réels :**

- températures
- ventilateurs
- tensions
- SMART

Cela ne fonctionne que sur le matériel physique.

---

### 📦 3. Disques NVMe/SSD sans capteurs
Certains modèles OEM ou contrôleurs RAID **n'exposent pas la température** ni l'état SMART.

---

### 🔐 4. Tokens sans permissions sur `/`
Si les permissions sont assignées à un nœud au lieu de la racine, Proxmox bloque l'API.

---

### 🕒 5. Intervalles de mise à jour
Pour éviter de saturer l'API, l'intégration utilise un intervalle de mise à jour minimal.
Ce n'est pas une erreur si les valeurs mettent quelques secondes à se mettre à jour.

---

### 🧩 6. Clusters Proxmox
Vous devez vous connecter au **nœud principal** du cluster.
Les nœuds secondaires n'exposent pas toute l'API.

---

### 🌐 7. Certificats SSL auto-signés
L'intégration les accepte automatiquement, mais certains navigateurs peuvent afficher des avertissements.
