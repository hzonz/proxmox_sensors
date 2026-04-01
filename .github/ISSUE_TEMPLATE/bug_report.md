---
name: 🐛 Bug Report
about: Report a problem with the integration
title: "[BUG] "
labels: bug
---

## 📋 Describe the issue
A clear and concise description of the problem.

---

## 🧱 Environment

- Home Assistant version:
- Proxmox VE version:
- Proxmox Backup Server version (if applicable):
- Installation type:
  - [ ] Home Assistant OS
  - [ ] Supervised
  - [ ] Container
  - [ ] Core

---

## 🔌 Connection details

- Are you using:
  - [ ] Username + Password
  - [ ] API Token

- Host used (IP / hostname):
- Verify SSL enabled:
  - [ ] Yes
  - [ ] No

---

## 🔐 Permissions

- User role:
  - [ ] PVEAdmin (PVE)
  - [ ] Administrator (PBS)

- Permissions assigned at:
  - [ ] `/` (root)
  - [ ] Node level (❌ not recommended)

---

## 🧠 Node detection

- Auto detect node:
  - [ ] Yes
  - [ ] No

- If manual:
  - Selected node:
  - Node IP:

---

## 📸 Screenshots

Please include screenshots of:
- Login screen
- Error message
- Node selection (if shown)

---

## 📜 Logs

Paste relevant logs from Home Assistant:

(Settings → System → Logs → Filter: proxmox)


---

## ⚠️ Common issues checklist

Before submitting, confirm:

- [ ] I am using the correct IP (not hostname)
- [ ] I did NOT include http/https or port
- [ ] The user/token has permissions on `/`
- [ ] I restarted Home Assistant after changes
- [ ] I reviewed the documentation

---

## 📝 Additional context

Add any other context here.
