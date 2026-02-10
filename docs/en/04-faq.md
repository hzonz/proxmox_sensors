# ❓ FAQ — Frequently Asked Questions

Below you will find the most common questions and issues when using the **Proxmox Extended Sensors** integration, along with quick solutions.

---

## 🔐 I cannot log in to the integration (PVE or PBS)

### ✔ 1. Do NOT include `http://` or `https://`
Enter only the domain or IP, for example:

192.168.1.10  
pve.my-domain.com

---

### ✔ 2. Do NOT include the port
The integration automatically detects the correct port.

---

### ✔ 3. Check the user or API Token permissions
The user must have:

- PVE: `PVEAdmin`  
- PBS: `Administrator`

Permissions must be assigned at the root `/`.

---

### ✔ 4. Make sure the Token is enabled
In Proxmox → Datacenter → Permissions → API Tokens  
It must show **Enabled: Yes**.

---

## 🔑 It says “Permission denied” even though the Token is correct

This usually happens because:

### ✔ 1. The Token does not have permissions at `/`
Permissions must be assigned at `/ (root)`  
Not on a specific node.

### ✔ 2. The Token belongs to a user without permissions
The parent user must have the correct role (`PVEAdmin` or `Administrator`).

---

## 🌐 The integration does not detect my Tuxis PBS

This is expected.

Tuxis-managed PBS servers do NOT expose internal metrics through the API:

- datastore space  
- disk usage  
- RRD statistics  
- node hardware  
- temperature  
- SMART  
- CPU/RAM  

This is not an integration bug.  
Tuxis blocks these endpoints by design.

The integration automatically detects Tuxis PBS and hides unavailable sensors.

---

## 📦 I cannot see datastore space sensors in PBS

### ✔ If your PBS is from Tuxis → these metrics are not available
Tuxis blocks the endpoint that returns datastore status.

Without that endpoint, it is impossible to obtain:

- total space  
- free space  
- usage percentage  
- deduplication  
- chunks  
- GC  

---

## 🌡️ Temperature sensors do not appear in PVE

### ✔ 1. You must install `lm-sensors` on the node  
### ✔ 2. You must run `sensors-detect`  
### ✔ 3. You must load the recommended modules  
Example:

modprobe coretemp  
modprobe nct6775  

### ✔ 4. You must create the systemd service  
So sensors work after reboot.

---

## 🖥️ NVMe/SSD/HDD sensors do not appear

### ✔ 1. The disk must support temperature reporting  
Some OEM models do not expose sensors.

### ✔ 2. Virtualized NVMe inside VMs do not expose sensors  
Only physical hardware works.

### ✔ 3. Tuxis PBS does not expose disk sensors  
Provider limitation.

---

## 🧠 My VMs or containers do not appear

### ✔ 1. Check user permissions  
The user must have the `PVEAdmin` role.

### ✔ 2. If you use a cluster  
You must connect to the **main node**, not a secondary node.

---

## 🔄 The integration updates slowly

This is normal.

The integration uses an internal coordinator to:

- avoid API overload  
- reduce node load  
- improve performance  

Default update interval is 10 seconds (configurable).

---

## 🧩 Can I use multiple PVE and PBS servers?

Yes.  
The integration allows multiple instances, each with its own Token.

---

## 🔒 Are API Tokens safe?

Yes.

The integration:

- does not store passwords  
- uses Tokens only  
- does not execute commands on the server  
- does not modify Proxmox configuration  
- does not open additional ports  

---

## 🧹 How do I remove old sensors?

Home Assistant automatically removes orphaned entities.

If you want to force cleanup:

1. Remove the integration  
2. Restart Home Assistant  
3. Add it again  

---

## 🛠️ Where can I report issues?

You can open an issue on GitHub including:

- HA version  
- Proxmox version  
- relevant logs  
- steps to reproduce  
- server type (PVE, PBS, Tuxis, etc.)  

---

# 🧾 Checklist before opening an Issue

Before reporting a problem, check this quick list.  
90% of issues are solved here:

### ✔ 1. Can you access Proxmox from your browser?  
If you cannot access the PVE/PBS web UI, the integration cannot either.

### ✔ 2. Are you using only the domain/IP?  
Do not include `http://`, `https://` or ports.

### ✔ 3. Is the API Token enabled?  
It must show **Enabled: Yes**.

### ✔ 4. Does the user have permissions at `/`?  
Permissions must be assigned at `/ (root)`.

### ✔ 5. Have you installed and configured `lm-sensors` on PVE?  
Without this, hardware sensors will not appear.

### ✔ 6. Is your PBS from Tuxis?  
If so, remember it does not expose internal metrics.

### ✔ 7. Have you restarted Home Assistant after changing permissions?  
HA caches old permissions.

### ✔ 8. Are there errors in Home Assistant logs?  
Check the Integrations log section.

### ✔ 9. Have you tried incognito mode?  
HA frontend caches resources for weeks.

---

# 🚫 Known Limitations

These limitations are not integration bugs, but restrictions from Proxmox or the provider.

---

### 🔒 1. Tuxis PBS

Tuxis-managed PBS servers do not expose:

- datastore space  
- disk usage  
- deduplication  
- chunks  
- RRD statistics  
- node hardware  
- temperature  
- SMART  
- CPU/RAM  

The integration automatically hides unavailable sensors.

---

### 🧊 2. Hardware sensors inside virtual machines

VMs do not expose real sensors:

- temperatures  
- fans  
- voltages  
- SMART  

Only physical hardware works.

---

### 📦 3. NVMe/SSD without sensors

Some OEM models or RAID controllers do not expose temperature or SMART.

---

### 🔐 4. Tokens without permissions at `/`

If permissions are assigned to a node instead of `/`, Proxmox blocks the API.

---

### 🕒 5. Update intervals

The integration uses a minimum update interval to avoid API overload.  
It is normal for values to take a few seconds to refresh.

---

### 🧩 6. Proxmox clusters

You must connect to the **main node** of the cluster.  
Secondary nodes do not expose the full API.

---

### 🌐 7. Self-signed SSL certificates

The integration accepts them automatically, but some browsers may show warnings.
