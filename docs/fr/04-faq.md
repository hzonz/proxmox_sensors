# ❓ FAQ — Foire Aux Questions

Voici les questions et problèmes les plus fréquents lors de l’utilisation de l’intégration **Proxmox Extended Sensors**, accompagnés de leurs solutions rapides.

---

## 🔐 Impossible de se connecter à l’intégration (PVE ou PBS)

### ✔ 1. Ne pas saisir `http://` ou `https://`
Saisis uniquement le domaine ou l’adresse IP, par exemple :

192.168.1.10  
pve.mon-domaine.com

---

### ✔ 2. Ne pas saisir de port
L’intégration détecte automatiquement le port approprié.

---

### ✔ 3. Vérifie les permissions de l’utilisateur ou du Token API
L’utilisateur doit avoir :

- PVE : `PVEAdmin`  
- PBS : `Administrator`

Les permissions doivent être appliquées à la racine `/`.

---

### ✔ 4. Vérifie que le Token est activé
Dans Proxmox → Datacenter → Permissions → API Tokens  
Il doit afficher **Enabled: Yes**.

---

## 🔑 “Permission denied” alors que le Token est correct

Les causes les plus fréquentes :

### ✔ 1. Le Token n’a pas de permissions sur `/`
Les permissions doivent être définies sur `/ (root)`  
Pas sur un nœud spécifique.

### ✔ 2. Le Token appartient à un utilisateur sans permissions
L’utilisateur parent doit avoir le rôle `PVEAdmin` ou `Administrator`.

---

## 🌐 L’intégration ne détecte pas mon PBS Tuxis

C’est normal.

Les serveurs PBS gérés par Tuxis **ne fournissent aucune métrique interne** via l’API :

- espace du datastore  
- utilisation du disque  
- statistiques RRD  
- matériel du nœud  
- température  
- SMART  
- CPU/RAM  

Ce n’est pas un bug de l’intégration.  
Tuxis bloque volontairement ces endpoints.

L’intégration détecte automatiquement un PBS Tuxis et masque les capteurs indisponibles.

---

## 📦 Je ne vois pas les capteurs d’espace du datastore dans PBS

### ✔ Si ton PBS est Tuxis → ces données ne sont pas disponibles
Tuxis bloque l’endpoint qui renvoie l’état du datastore.

Sans cet endpoint, il est impossible d’obtenir :

- espace total  
- espace libre  
- pourcentage d’utilisation  
- déduplication  
- chunks  
- GC  

---

## 🌡️ Les capteurs de température n’apparaissent pas dans PVE

### ✔ 1. `lm-sensors` doit être installé sur le nœud  
### ✔ 2. `sensors-detect` doit être exécuté  
### ✔ 3. Les modules recommandés doivent être chargés  
Exemple :

modprobe coretemp  
modprobe nct6775  

### ✔ 4. Un service systemd doit être créé  
Pour que les capteurs fonctionnent après redémarrage.

---

## 🖥️ Les capteurs NVMe/SSD/HDD n’apparaissent pas

### ✔ 1. Le disque doit supporter la lecture de température  
Certains modèles OEM ne fournissent pas de capteurs.

### ✔ 2. Les NVMe virtualisés dans les VMs n’ont pas de capteurs  
Seul le matériel physique expose ces données.

### ✔ 3. Les PBS Tuxis ne fournissent pas de capteurs de disque  
Limitation du fournisseur.

---

## 🧠 Mes VMs ou conteneurs n’apparaissent pas

### ✔ 1. Vérifie les permissions de l’utilisateur  
Il doit avoir le rôle `PVEAdmin`.

### ✔ 2. En cluster  
Tu dois te connecter au **nœud principal**, pas à un nœud secondaire.

---

## 🔄 L’intégration met du temps à mettre à jour les valeurs

C’est normal.

L’intégration utilise un coordinateur interne pour :

- éviter la surcharge de l’API  
- réduire la charge du nœud  
- améliorer les performances  

L’intervalle par défaut est de 10 secondes (modifiable).

---

## 🧩 Puis‑je utiliser plusieurs serveurs PVE et PBS ?

Oui.  
L’intégration permet plusieurs instances, chacune avec son propre Token.

---

## 🔒 Les Tokens API sont‑ils sûrs ?

Oui.

L’intégration :

- ne stocke pas de mots de passe  
- utilise uniquement des Tokens  
- n’exécute aucune commande sur le serveur  
- ne modifie pas la configuration Proxmox  
- n’ouvre aucun port supplémentaire  

---

## 🧹 Comment supprimer d’anciens capteurs ?

Home Assistant supprime automatiquement les entités orphelines.

Pour forcer un nettoyage :

1. Supprime l’intégration  
2. Redémarre Home Assistant  
3. Ajoute‑la à nouveau  

---

## 🛠️ Où signaler un problème ?

Ouvre un ticket GitHub avec :

- version de HA  
- version de Proxmox  
- logs pertinents  
- étapes pour reproduire  
- type de serveur (PVE, PBS, Tuxis, etc.)  

---

# 🧾 Checklist avant d’ouvrir un ticket

Cette liste résout 90 % des problèmes :

### ✔ 1. Peux‑tu accéder à Proxmox via ton navigateur ?  
Si l’interface web PVE/PBS est inaccessible, l’intégration le sera aussi.

### ✔ 2. Utilises‑tu uniquement le domaine/IP ?  
Pas de `http://`, `https://` ni de ports.

### ✔ 3. Le Token API est‑il activé ?  
Il doit afficher **Enabled: Yes**.

### ✔ 4. L’utilisateur a‑t‑il des permissions sur `/` ?  
Les permissions doivent être définies sur `/ (root)`.

### ✔ 5. `lm-sensors` est‑il installé et configuré ?  
Sans cela, aucun capteur matériel n’apparaîtra.

### ✔ 6. Ton PBS est‑il un Tuxis ?  
Dans ce cas, les métriques internes ne sont pas disponibles.

### ✔ 7. As‑tu redémarré Home Assistant après avoir modifié les permissions ?  
HA met en cache les anciennes permissions.

### ✔ 8. Y a‑t‑il des erreurs dans les logs HA ?  
Consulte la section « Intégrations ».

### ✔ 9. As‑tu essayé le mode navigation privée ?  
Le frontend HA met en cache les ressources pendant longtemps.

---

# 🚫 Limitations connues

Ces limitations ne sont pas des bugs de l’intégration, mais des restrictions de Proxmox ou du fournisseur.

---

### 🔒 1. PBS Tuxis

Les PBS Tuxis ne fournissent pas :

- espace du datastore  
- utilisation du disque  
- déduplication  
- chunks  
- statistiques RRD  
- matériel du nœud  
- température  
- SMART  
- CPU/RAM  

L’intégration masque automatiquement ces capteurs.

---

### 🧊 2. Capteurs matériels dans les machines virtuelles

Les VMs n’exposent pas de capteurs réels :

- températures  
- ventilateurs  
- tensions  
- SMART  

Seul le matériel physique fournit ces données.

---

### 📦 3. NVMe/SSD sans capteurs

Certains modèles OEM ou contrôleurs RAID ne fournissent pas de température ni de SMART.

---

### 🔐 4. Tokens sans permissions sur `/`

Si les permissions sont appliquées à un nœud au lieu de `/`, Proxmox bloque l’API.

---

### 🕒 5. Intervalles de mise à jour

L’intégration utilise un intervalle minimal pour éviter la surcharge de l’API.  
Il est normal que les valeurs mettent quelques secondes à se mettre à jour.

---

### 🧩 6. Clusters Proxmox

Tu dois te connecter au **nœud principal** du cluster.  
Les nœuds secondaires n’exposent pas l’API complète.

---

### 🌐 7. Certificats SSL auto‑signés

L’intégration les accepte automatiquement, mais certains navigateurs peuvent afficher des avertissements.
