# ❓ FAQ — Frequently Asked Questions

Below you will find the most common questions and issues when using the **Proxmox Sensors Extended** integration, along with their quick solutions.

---

## 🔐 I cannot log in to the integration (PVE or PBS)

### ✔ 1. Do not use `http://` or `https://`
Enter **only the domain or IP**, for example:

`192.168.1.10`
`pve.my-domain.com`

---

### ✔ 2. Do not include the port
The integration automatically detects the correct port.

### ✔ 3. Check API Token permissions
The user must have:

- **PVE:** - `Sys.Audit`  
  - `VM.Audit`  
  - `Datastore.Audit`  
  - `Permissions.Modify` (only if using automatic VM/LXC selection)

- **PBS:** - `Datastore.Audit`  
  - `Datastore.Read`  
  - `Sys.Audit`

---

### ✔ 4. Ensure the Token is active
In Proxmox → Datacenter → Permissions → API Tokens  
It must show **Enabled: Yes**.

---

## 🔑 It says “Permission denied” even though the Token is correct

This is usually due to:

### ✔ 1. The Token lacks permissions at the root `/`
In Proxmox, permissions must be assigned at: `/ (root)` **Not on a specific node.**

### ✔ 2. The Token belongs to a user without permissions
The parent user must have permissions, not just the Token itself.

---

## 🌐 The integration does not detect my Tuxis PBS

This is normal.

PBS instances managed by Tuxis **do not allow access to internal metrics** via API:

- Datastore space  
- Disk usage  
- RRD statistics  
- Node hardware  
- Temperature  
- SMART  
- CPU/RAM  

This is not a bug in the integration:  
Tuxis blocks these endpoints by design.

The integration automatically detects if it is a Tuxis PBS and hides unavailable sensors.

---

## 📦 I don't see datastore space sensors in PBS

### ✔ If your PBS is from Tuxis → **they are not available**
For security reasons, Tuxis blocks: `/api2/json/admin/datastore/<name>/status`

Without that endpoint, it is not possible to obtain:

- Total space  
- Free space  
- Usage percentage  
- Deduplication  
- Chunks  
- GC (Garbage Collection)  

---

## 🌡️ Temperature sensors are not appearing in PVE

### ✔ 1. You must install `lm-sensors` on the node
Full guide: [01. Hardware Sensor Configuration](01-install-sensors.md)

### ✔ 2. You must run `sensors-detect`
And accept all safe options.

### ✔ 3. You must load the recommended modules
Example:

```bash
modprobe coretemp
modprobe nct6775
```
### ✔ 4. You must create the systemd service
To ensure sensors work after a reboot.

---

## 🖥️ NVMe/SSD/HDD disk sensors are not appearing
### ✔ 1. The disk must support temperature reading
Some OEM models do not expose sensors.

### ✔ 2. Virtualized NVMe (VMs) do not have sensors
They only work on physical hardware.

### ✔ 3. Tuxis PBS does not expose disk sensors
This is a provider limitation.

## 🧠 My VMs or containers are not appearing

### ✔ 1. Check Token permissions
It must have: `VM.Audit`

### ✔ 2. If using automatic selection
The integration requires: `Permissions.Modify`

### ✔ 3. If using a cluster
You must connect to the main node, not a secondary node.

---

## 🔄 The integration takes time to update values
This is normal.

The integration uses `DataUpdateCoordinator` to:

* Avoid overwhelming the API
* Reduce load on the node
* Improve performance

**The default interval is 10 seconds and is configurable.**

---

## 🧩 Can I use multiple PVE and PBS instances at once?
### Yes.
The integration allows you to add multiple instances, each with its own Token.

---

## 🔒 Is it safe to use API Tokens?
### Yes.

The integration:
* Does not store passwords.
* Uses only Tokens with minimum permissions.
* Does not execute commands on the server.
* Does not modify Proxmox configuration.
* Does not open additional ports.

---

## 🧹 How do I remove old sensors?
**Home Assistant automatically removes orphaned entities.**

**If you want to force a cleanup:**
* Delete the integration.
* Restart Home Assistant.
* Add it again.

---

## 🛠️ Where can I report bugs?
**You can open an issue on GitHub including:**
* HA version.
* Proxmox version.
* Relevant logs.
* Steps to reproduce.
* Server type (PVE, PBS, Tuxis, etc.).

---

# 🧾 Checklist before opening an Issue

Before reporting a problem, check this quick list. 
90% of errors are solved here:

### ✔ 1. Can you access Proxmox from your browser?
If you cannot log in to the PVE/PBS web interface, the integration won't be able to either.

### ✔ 2. Are you using only the domain/IP?
Do not include `http://`, `https://`, or ports.

### ✔ 3. Is the API Token active?
In Proxmox → Datacenter → Permissions → API Tokens  
It must show **Enabled: Yes**.

### ✔ 4. Does the user have permissions at the root `/`?
Permissions must be assigned at: `/ (root)`, not on a specific node.

### ✔ 5. Have you installed and configured `lm-sensors` on PVE?
Without this, hardware sensors will not appear.

### ✔ 6. Is it a Tuxis PBS?
If so, remember that it **does not expose internal metrics** (space, hardware, RRD).

### ✔ 7. Have you restarted Home Assistant after changing permissions?
HA caches old permissions.

### ✔ 8. Are there errors in the Home Assistant logs?
Go to:  
**Settings → Logs → Integrations**

### ✔ 9. Have you tried incognito mode?
The HA frontend caches resources for weeks.

---

# 🚫 Known Limitations

These limitations are not bugs within the integration but rather restrictions imposed by Proxmox or the service provider:

### 🔒 1. Tuxis PBS
PBS servers managed by Tuxis **do not allow access to:**

- Datastore space  
- Disk usage  
- Deduplication  
- Chunks  
- RRD statistics  
- Node hardware  
- Temperature  
- SMART data  
- CPU/RAM usage  

The integration automatically detects this limitation and hides the unavailable sensors.

---

### 🧊 2. Hardware Sensors in Virtual Machines
VMs **do not expose real sensors**:

- Temperatures  
- Fans  
- Voltages  
- SMART status  

These only function on physical hardware.

---

### 📦 3. NVMe/SSD Disks without Sensors
Some OEM models or RAID controllers **do not expose temperature** or SMART status.

---

### 🔐 4. Tokens without Permissions on `/`
If permissions are assigned to a specific node instead of the root, Proxmox will block API access.

---

### 🕒 5. Update Intervals
To avoid overwhelming the API, the integration uses a minimum update interval.  
It is not an error if values take a few seconds to refresh.

---

### 🧩 6. Proxmox Clusters
You must connect to the **main node** of the cluster.  
Secondary nodes do not expose the full API.

---

### 🌐 7. Self-Signed SSL Certificates
The integration accepts them automatically, but some browsers may still display warnings.

---
