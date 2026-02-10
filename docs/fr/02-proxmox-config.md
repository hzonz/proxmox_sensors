# 🔐 Étape 2 : Configuration des utilisateurs et des permissions

**Pour qu'Home Assistant communique avec Proxmox de manière sécurisée, il est recommandé de ne pas utiliser l'utilisateur root. Nous allons créer un utilisateur dédié et lui attribuer les permissions nécessaires pour que l'intégration fonctionne à 100%.**

> ⚠️ **IMPORTANT :**  
> En raison des fonctions avancées de l'intégration (contrôle des VM/CT, sauvegardes individuelles et massives, actions PBS…), il est nécessaire d'attribuer **des permissions d'administrateur** à la fois dans PVE et dans PBS.

---

## 1. Différence entre PVE et PBS

### **Proxmox VE (PVE)**
- Vous pouvez utiliser **Utilisateur/Mot de passe** ou **Jeton API**.  
- L'utilisateur doit avoir le rôle **PVEAdmin**.

### **Proxmox Backup Server (PBS)**
- Il est **obligatoire** d'utiliser un **Jeton API**.  
- L'utilisateur doit avoir le rôle **Administrator** (PBS ne dispose pas d'un rôle intermédiaire valide).

---

## 2. Création de l'utilisateur

1. Allez dans **Datacenter → Permissions → Users**  
2. Cliquez sur **Add**  
3. Configurez :  
   - **User :** `homeassistant`  
   - **Realm :** `pve`  
   - **Password :** uniquement si vous allez utiliser la connexion par mot de passe dans PVE  
4. Enregistrez les modifications

---

## 3. Attribution du rôle correct

1. Allez dans **Datacenter → Permissions**  
2. Cliquez sur **Add → User Permission**  
3. Configurez les champs suivants :

### ✔ Pour PVE :
- **Path :** `/`  
- **User :** `homeassistant@pve`  
- **Role :** `PVEAdmin`  

### ✔ Pour PBS :
- **Path :** `/`  
- **User :** `homeassistant@pve`  
- **Role :** `Administrator`  

> 💡 **Pourquoi `/` est nécessaire :**  
> L'intégration a besoin d'un accès global pour lire les nœuds, VM, CT, disques, datastores et tâches.

---

## 4. Génération du jeton API (Obligatoire pour PBS)

1. Allez dans **Datacenter → Permissions → API Tokens**  
2. Cliquez sur **Add**  
3. Configurez :  
   - **User :** `homeassistant@pve`  
   - **Token ID :** `ha-token`  
   - **Privilege Separation :** **décoché**  
   - **Expire :** **Never**  
4. Lors de la création du jeton, Proxmox affichera :  
   - **Token ID**  
   - **Secret** (affiché une seule fois)

> [!WARNING]
> **Copiez le "Secret" maintenant et sauvegardez-le dans un endroit sûr.** Une fois que vous fermez cette fenêtre, Proxmox ne vous le montrera plus jamais pour des raisons de sécurité.

> [!TIP]
> ### 💡 Avez-vous oublié de copier le Secret ?
> Ne vous inquiétez pas. Bien que Proxmox ne vous le montre plus pour des raisons de sécurité, vous n'avez pas besoin de supprimer le jeton et de recommencer :
> 
> 1. Dans la liste **API Tokens**, sélectionnez le jeton que vous avez déjà créé.
> 2. Cliquez sur le bouton **Regenerate**.
> 3. Le système invalidera immédiatement l'ancienne clé et vous donnera un **nouveau Secret**.
> 
> *N'oubliez pas que si vous régénérez le Secret, vous devez le mettre à jour dans la configuration d'Home Assistant pour que l'intégration puisse se reconnecter.*
