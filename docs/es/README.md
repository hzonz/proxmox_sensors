# 📚 Documentación y Guías

Para garantizar una configuración sin problemas, sigue estas guías paso a paso:

---

## 🌡️ [01. Configuración de Sensores de Hardware](01-install-sensors.md)
Cómo instalar y configurar **lm-sensors** en tu nodo Proxmox para habilitar la monitorización de temperaturas y ventiladores.

---

## 🔑 [02. Configuración de Proxmox](02-proxmox-config.md)
Cómo crear un **usuario** y **Token API** seguro en Proxmox (PVE & PBS) con los permisos mínimos necesarios.

---

## ⚙️ [03. Inicio de Sesión en la Integración (PVE & PBS)](03-login-pve-pbs.md)
Guía del proceso de configuración inicial en Home Assistant y conexión con tus servidores.

---

## ❓ [04. Preguntas Frecuentes y Solución de Problemas](04-faq.md)
Preguntas comunes, problemas conocidos y cómo resolverlos.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/imag/logo_int.png" alt="Proxmox Extended Sensors Logo" width="600"/>
</p>

---
# 🚀 Proxmox Extended Sensors

**La integración más completa, eficiente y organizada para monitorizar Proxmox VE y PBS desde Home Assistant.**

Esta integración está diseñada para usuarios avanzados que necesitan un control total sobre su hardware sin sobrecargar el servidor.  
A diferencia de otras soluciones, Proxmox Sensors Extended se centra en la eficiencia energética, autenticación segura mediante Tokens y una organización visual impecable.

---

## 🔥 Características Principales

### 🌡️ Monitorización Avanzada de Hardware

**No te conformes solo con el uso de CPU. Ve lo que realmente ocurre “bajo el capó”:**

* **Temperaturas en tiempo real:** Núcleos de CPU, VRM y unidades NVMe/SSD/HDD.
* **Sensores mecánicos:** Velocidad de ventiladores (RPM) y voltajes de la placa base.
* **Sensores inteligentes:** Solo se crean entidades que reportan datos válidos, manteniendo tu sistema limpio.

**(Nota: Requiere instalar lm-sensors en el host Proxmox).**

---

### 🧠 Optimizado para el Rendimiento

**Diseñado pensando en hardware con recursos limitados:**

* **DataUpdateCoordinator:** Minimiza las llamadas a la API de Proxmox para evitar saturar el procesador del servidor.
* **Silent SSL:** Verificación automática de certificados SSL (incluidos los autofirmados) sin llenar tus logs de errores.

---

### 🗄️ Proxmox Backup Server (PBS) Avanzado

* **Modo Externo:** Conéctate fácilmente a servidores PBS remotos usando solo el dominio.
* **Monitorización de Tareas:** Estado detallado del último Backup, Garbage Collector o tarea de Verify.

---

### 🎨 Interfaz Dinámica y Organizada

* **Smart Dashboard:** Los sensores se agrupan automáticamente en dispositivos:  
  1. Nodo  
  2. Discos físicos  
  3. Máquinas virtuales  
  4. Contenedores  
* **Auto-Naming:** Prefijos automáticos (ej. `pv1-cpu-temp`) para mantener tus dashboards ordenados de forma lógica.

---

## Sensores Destacados

## PVE

### 🖥️ Sensores de Hardware (PVE & PBS)

Temperaturas de CPU • Temperaturas VRM • Temperaturas NVMe/SSD/HDD  
Velocidad de ventiladores (RPM) • Voltajes • Sensores de energía • Entidades `pvesensors`  
• Temperatura del chipset

---

### 🧠 Estado del Nodo

Uso de CPU (%) • Uso de RAM (%) • RAM usada/total  
Tiempo activo (uptime) • Load average • CPU I/O Wait

---

### 💾 Discos

Capacidad total • Espacio usado (GB y %)  
Nivel de desgaste (NVMe) • Estado SMART (si está disponible)

---

### 🖥️ Máquinas Virtuales (QEMU)

Uso de CPU (%) • Uso de RAM (%)  
Estado (encendida/apagada) • Selección automática/manual

---

### 📦 Contenedores (LXC)

Uso de CPU (%) • Uso de RAM (%)  
Estado • Selección automática/manual

---

### 🗄️ Proxmox Backup Server (PBS)

Uso del datastore (GB y %) • Número de backups  
Estado del Garbage Collector • Estado de la última tarea de backup  
• Información completa de tareas y más

---

**Ejemplo de Dashboard**

<p align="center">
  <img src="/img/Dashboard.png" alt="Proxmox Extended Sensors Dashboard" width="1000"/>
</p>
