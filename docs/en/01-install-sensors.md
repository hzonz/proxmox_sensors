# 🚀 Step 1: Sensor Installation and Configuration
**This guide explains how to prepare the Proxmox node to expose hardware data and ensure temperature readings are available for Home Assistant.**

## 1. Installing Dependencies
* **First, we install the necessary tools to read the sensors integrated into the motherboard and CPU:**

apt update && apt install lm-sensors -y

## 2. Hardware Detection
* **To allow the system to identify which drivers it needs, we run the detection assistant:**

sensors-detect

**Answer YES (or press Enter) to all questions. Once finished, the system will identify the required modules (e.g., coretemp for Intel CPUs).**

## 3. Module Persistence
**To ensure the sensors activate automatically when the server reboots, the sensors-detect wizard will ask a key question at the very end:**

Do you want to add these lines automatically to /etc/modules? (yes/NO)

> [!CAUTION]
> **You must manually type yes and press Enter.** If you just press Enter without typing anything, the system will select NO by default. If this happens, the sensors will not load after a reboot, and Home Assistant will stop receiving temperature data.

## 4. Immediate Verification
**To activate the sensors right now without rebooting, run:**

# Load the detected modules (example for Intel)
modprobe coretemp

# Verify that temperatures are being displayed
sensors

**Done! Once the sensors command returns data in the terminal, your Home Assistant integration will be able to read them automatically through the Proxmox API.**
