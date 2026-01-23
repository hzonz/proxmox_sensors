# 🔐 Step 2: User and Permissions Configuration
**To allow Home Assistant to communicate with Proxmox securely, it is recommended not to use the root user. In this guide, we will create an access with "read-only" permissions.**

## 1. Difference between PVE and PBS
Before starting, keep the following in mind:

* **Proxmox VE (PVE): You can use a standard Username/Password or an API Token.**

* **Proxmox Backup Server (PBS): Using an API Token is essential. Traditional login methods often fail due to security restrictions or permissions on the Datastore.**

---

## 2. Role Creation (Permissions)
**A "Role" defines what the integration is allowed to do.**

1. Go to **Datacenter > Permissions > Roles**.
2. Click **Create** and name it `HA-Monitor`.
3. Select the following **Privileges**:
    * `Sys.Audit`: Allows viewing node status (CPU, RAM).
    * `VM.Audit`: Allows viewing the status of VMs and containers.
    * `Datastore.Audit`: Allows viewing disk space.

---

## 3. User Creation
1. Go to **Datacenter > Permissions > Users**.
2. Click **Add**.
3. **User:** `homeassistant` (you can leave the realm as `pve`).
4. Give it a secure password if you plan to use this method for PVE.

---

## 4. Role Assignment
**You must tell Proxmox that this user has the role we just created:**

1. Go to **Datacenter > Permissions**.
2. Click **Add > User Permission**.
3. Configure the following fields:
    * **Path:** `/` (This is very important so the integration can see the entire server).
    * **User:** `homeassistant@pve` (or the user you created).
    * **Role:** `HA-Monitor`.

---

## 5. API Token Generation (Mandatory for PBS)
**If you are monitoring a PBS or prefer not to use passwords in PVE, follow these steps:**

1. Go to **Datacenter > Permissions > API Tokens**.
2. Click **Add** and fill out the form:
    * **User:** Select the `homeassistant` user.
    * **Token ID:** `ha-token` (you can choose any name).
    * **Privilege Separation:** ⚠️ **UNCHECK this box**. If left checked, the Token will not inherit the user's permissions, and the integration will fail.
3. Upon clicking **Add**, a window will open with two key pieces of data:
    * **Token ID:** (Example: `homeassistant@pve!ha-token`).
    * **Secret:** (A long string of letters and numbers).

> [!WARNING]
> **Copy the "Secret" now and save it in a safe place.** Once you close this window, Proxmox will never show it to you again for security reasons.

> [!TIP]
> ### 💡 Forgot to copy the Secret?
> Don't worry. Although Proxmox won't show it again for security reasons, you don't need to delete the token and start over:
> 
> 1. In the **API Tokens** list, select the token you previously created.
> 2. Click the **Regenerate** button.
> 3. The system will immediately invalidate the old key and provide you with a **new Secret**.
> 
> *Remember that if you regenerate the Secret, you must update it in your Home Assistant configuration for the integration to reconnect.*
