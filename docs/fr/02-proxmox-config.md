# 🔐 Étape 2 : Configuration des utilisateurs et des permissions
**Pour que Home Assistant communique avec Proxmox de manière sécurisée, il est recommandé de ne pas utiliser l'utilisateur root. Dans ce guide, nous allons créer un accès avec des permissions de "lecture seule".**

## 1. Différence entre PVE et PBS
Avant de commencer, vous devez prendre en compte :

* **Proxmox VE (PVE) : Vous pouvez utiliser un nom d'utilisateur/mot de passe conventionnel ou un Token API.**

* **Proxmox Backup Server (PBS) : Il est indispensable d'utiliser un Token API. Les méthodes de connexion traditionnelles échouent souvent en raison de restrictions de sécurité ou de permissions sur le Datastore.**

---

## 2. Création du Rôle (Permissions)
**Un "Rôle" définit ce que l'intégration peut faire.**

1. Allez dans Datacenter > Permissions > Roles.

2. Cliquez sur Create et donnez-lui le nom HA-Monitor.

---

## 3. Création du Rôle (Permissions)
Un "Rôle" définit ce que l'intégration peut faire.
1. Allez dans **Datacenter > Permissions > Roles**.
2. Cliquez sur **Create** et donnez-lui le nom `HA-Monitor`.
3. Sélectionnez les privilèges suivants (**Privileges**) :
    * `Sys.Audit` : Permet de voir l'état du nœud (CPU, RAM).
    * `VM.Audit` : Permet de voir l'état des VMs et des conteneurs.
    * `Datastore.Audit` : Permet de voir l'espace disque.

---

## 4. Création de l'utilisateur
1. **Allez dans Datacenter > Permissions > Users.**

2. **Cliquez sur Add.**

3. **Utilisateur : homeassistant (vous pouvez laisser le domaine comme pve).**

4. **Donnez-lui un mot de passe sécurisé si vous allez utiliser cette méthode pour PVE.**

---

## 5. Assignation du Rôle
**Vous devez dire à Proxmox que cet utilisateur possède le rôle que nous avons créé :**

1. Allez dans **Datacenter > Permissions**.
2. Cliquez sur **Add > User Permission**.
3. Configurez les champs suivants :
    * **Path :** `/` (C'est très important pour que l'intégration puisse voir tout le serveur).
    * **User :** `homeassistant@pve` (ou l'utilisateur que vous avez créé).
    * **Role :** `HA-Monitor`.

---

## 6. Génération du Token API (Obligatoire pour PBS)
**Si vous allez surveiller un PBS ou si vous préférez ne pas utiliser de mots de passe sur PVE, suivez ces étapes :**

1. Allez dans **Datacenter > Permissions > API Tokens**.
2. Cliquez sur **Add** et remplissez le formulaire :
    * **User :** Sélectionnez l'utilisateur `homeassistant`.
    * **Token ID :** `ha-token` (vous pouvez choisir le nom que vous voulez).
    * **Privilege Separation :** ⚠️ **DÉCOCHEZ cette case**. Si vous la laissez cochée, le Token n'héritera pas des permissions de l'utilisateur et l'intégration échouera.
3. En cliquant sur **Add**, une fenêtre s'ouvrira avec deux données clés :
    * **Token ID :** (Exemple : `homeassistant@pve!ha-token`).
    * **Secret :** (Une longue chaîne de lettres et de chiffres).

> [!WARNING]
> **Copiez le "Secret" maintenant et gardez-le en lieu sûr.** Une fois cette fenêtre fermée, Proxmox ne vous le montrera plus jamais pour des raisons de sécurité.


> [!TIP]
> ### 💡 Vous avez oublié de copier le Secret ?
> Ne vous inquiétez pas. Même si Proxmox ne vous le remontre pas par sécurité, il n'est pas nécessaire de supprimer le token et de recommencer de zéro :
> 
> 1. Dans la liste des **API Tokens**, sélectionnez le token que vous aviez déjà créé.
> 2. Cliquez sur le bouton **Regenerate**.
> 3. Le système invalidera immédiatement l'ancienne clé et vous donnera un **nouveau Secret**.
> 
> *N'oubliez pas que si vous régénérez le Secret, vous devrez le mettre à jour dans la configuration de Home Assistant pour que l'intégration se reconnecte.*
