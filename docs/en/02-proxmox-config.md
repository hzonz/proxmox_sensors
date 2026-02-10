# 🔐 Step 2: User and Permissions Configuration

**For Home Assistant to communicate with Proxmox securely, it is recommended not to use the root user. We will create a dedicated user and assign the necessary permissions for the integration to function at 100%.**

> ⚠️ **IMPORTANT:**  
> Due to the advanced functions of the integration (control of VMs/CTs, individual and mass backups, PBS actions…), it is necessary to assign **administrator permissions** in both PVE and PBS.

---

## 1. Difference between PVE and PBS

### **Proxmox VE (PVE)**
- You can use **User/Password** or **API Token**.  
- The user must have the **PVEAdmin** role.

### **Proxmox Backup Server (PBS)**
- It is **mandatory** to use an **API Token**.  
- The user must have the **Administrator** role (PBS does not have a valid intermediate role).

---

## 2. User Creation

1. Go to **Datacenter → Permissions → Users**  
2. Click on **Add**  
3. Configure:  
   - **User:** `homeassistant`  
   - **Realm:** `pve`  
   - **Password:** only if you are going to use password login in PVE  
4. Save changes

---

## 3. Assigning the Correct Role

1. Go to **Datacenter → Permissions**  
2. Click on **Add → User Permission**  
3. Configure the following fields:

### ✔ For PVE:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

### ✔ For PBS:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

> 💡 **Why `/` is necessary:**  
> The integration needs global access to read nodes, VMs, CTs, disks, datastores, and tasks.

---

## 4. API Token Generation (Mandatory for PBS)

1. Go to **Datacenter → Permissions → API Tokens**  
2. Click on **Add**  
3. Configure:  
   - **User:** `homeassistant@pve`  
   - **Token ID:** `ha-token`  
   - **Privilege Separation:** **unchecked**  
   - **Expire:** **Never**  
4. When creating the token, Proxmox will display:  
   - **Token ID**  
   - **Secret** (only shown once)

> [!WARNING]
> **Copy the "Secret" now and save it in a safe place.** Once you close this window, Proxmox will never show it to you again for security reasons.

> [!TIP]
> ### 💡 Did you forget to copy the Secret?
> Don't worry. Although Proxmox won't show it to you again for security reasons, you don't need to delete the token and start over:
> 
> 1. In the **API Tokens** list, select the token you had already created.
> 2. Click the **Regenerate** button.
> 3. The system will immediately invalidate the old key and give you a **new Secret**.
> 
> *Remember that if you regenerate the Secret, you must update it in the Home Assistant configuration for the integration to reconnect.*
