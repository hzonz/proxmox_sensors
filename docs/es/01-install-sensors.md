# 🚀 Paso 1: Instalación y automatización de sensores
**Esta guía explica cómo preparar el nodo Proxmox para que exponga los datos de hardware y asegure que el servicio de telemetría arranque automáticamente con el sistema.**

## 1. Instalación de dependencias
* **Primero, instalamos las herramientas necesarias para leer los sensores integrados en la placa base y la CPU:**

```bash
apt update && apt install lm-sensors -y
```
