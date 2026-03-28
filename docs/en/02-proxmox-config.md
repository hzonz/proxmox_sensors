# 🔐 Step 2: User and Permission Configuration

For Home Assistant to communicate with Proxmox securely, it is recommended **not to use the root user**.

Instead, we will create a dedicated user with the necessary permissions for the integration to work correctly.

---

> ⚠️ **IMPORTANT**  
> Due to the advanced features of the integration (VM/CT control, backups, PBS actions, etc.), it is necessary to assign elevated permissions in Proxmox.
>
> These permissions allow:
> - Control virtual machines and containers  
> - Run backups (individual and bulk)  
> - Access node, disk, and task information  
> - Interact with Proxmox Backup Server (PBS)  
>
> Although these are broad permissions, using a **dedicated user + API Token** keeps access isolated and controlled.

---

## 1. Difference between PVE and PBS

### 🖥️ Proxmox VE (PVE)
- Allows authentication via:
  - Username/Password  
  - API Token  
- The user must have the **PVEAdmin** role  

---

### 🗄️ Proxmox Backup Server (PBS)
- Requires an **API Token** (mandatory)  
- The user must have the **Administrator** role  
- There is no intermediate role compatible with all functions  

---

## 2. Creating the user

1. Go to **Datacenter → Permissions → Users**  
2. Click **Add**  
3. Configure:

- **User:** `homeassistant`  
- **Realm:** `pve`  
- **Password:** (only if you will use password login for PVE)

4. Save the changes  

---

## 3. Assigning permissions

1. Go to **Datacenter → Permissions**  
2. Click **Add → User Permission**  

---

### ✔ For Proxmox VE (PVE)

- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

---

### ✔ For Proxmox Backup Server (PBS)

- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

---

> 💡 **Why use `/` (global access)**  
> The integration needs access to the entire infrastructure:
> nodes, VMs, containers, disks, storages, and tasks.

---

## 4. Creating the API Token

1. Go to **Datacenter → Permissions → API Tokens**  
2. Click **Add**  
3. Configure:

- **User:** `homeassistant@pve`  
- **Token ID:** `ha-token`  
- **Privilege Separation:** ❌ Unchecked  
- **Expire:** Never  

---

### 🔍 Why disable "Privilege Separation"?

Because the token needs to inherit the user's full permissions.

If this option is enabled:
- the token will have limited permissions  
- some functions (backups, control, PBS) will not work correctly  

---

4. When creating the token, Proxmox will display:

- **Token ID**  
- **Secret** (only visible once)

---

> [!WARNING]
> Save the **Secret** in a safe place.  
> It will not be viewable again once you close this window.

---

> [!TIP]
> ### 💡 Did you forget to copy the Secret?
> There is no need to delete the token:
>
> 1. Select the token in the list  
> 2. Click **Regenerate**  
> 3. A new Secret will be generated immediately  
>
> ⚠️ Remember to update it in Home Assistant.

---

## ✔ Conclusion

Once configured:

- Dedicated user  
- Permissions correctly assigned  
- API Token created  

The integration will be able to connect to Proxmox securely and with full access to all its features.