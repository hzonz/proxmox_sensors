# 🚀 Paso 1: Instalación y automatización de sensores
**Esta guía explica cómo preparar el nodo Proxmox para que exponga los datos de hardware y asegure que el servicio de telemetría arranque automáticamente con el sistema.**

## 1. Instalación de dependencias
* **Primero, instalamos las herramientas necesarias para leer los sensores integrados en la placa base y la CPU:**

```bash
apt update && apt install lm-sensors -y
```

## 2. Detección de hardware
* **Para que el sistema sepa qué controladores (drivers) necesita, ejecutamos el asistente de detección:**

```Bash
sensors-detect
```
**Responde YES (o pulsa Enter) a todas las preguntas. Al finalizar, el sistema identificará los módulos necesarios (ej. coretemp, nct6775).**

## 3. Persistencia de módulos
**Para que los sensores se activen solos al reiniciar el servidor, el asistente sensors-detect te hará una pregunta clave al final del todo:**
```
Do you want to add these lines automatically to /etc/modules? (yes/NO)
```
[!CAUTION] Debes escribir `yes` manualmente y pulsar Enter. **Si solo pulsas Enter sin escribir nada, el sistema seleccionará NO por defecto y los sensores no cargarán tras un reinicio.**

```Bash
# Sustituye 'modulo_detectado' por los nombres que dio el comando anterior
echo "modulo_detectado" >> /etc/modules
```

## 4. Servicio de Telemetría (Arranque Automático)
**Para que Home Assistant pueda leer estos datos de forma continua, configuraremos el script de la API como un servicio del sistema (systemd). Esto garantiza que, aunque el servidor se reinicie, el servicio arrancará automáticamente.**

### A. Crear el archivo del servicio

```Bash
nano /etc/systemd/system/proxmox-sensors.service
```

### B. Configuración del servicio
**Copia y pega el siguiente bloque. Este diseño asegura que el servicio sea ligero y se reinicie solo si ocurre algún fallo:**

`Ini, TOML`
```
[Unit]
Description=API de Sensores para Home Assistant
After=network.target

[Service]
Type=simple
User=root
# Asegúrate de que la ruta al script sea la correcta
ExecStart=/usr/bin/python3 /ruta/al/archivo/sensor_script.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### C. Activación del servicio
**Ejecuta estos comandos para registrar y activar el arranque automático:**

```Bash
# Recargar la configuración de servicios
systemctl daemon-reload

# Activar el inicio automático con el sistema
systemctl enable proxmox-sensors.service

# Iniciar el servicio inmediatamente
systemctl start proxmox-sensors.service
```

# ✅ Verificación
**Para confirmar que el servicio está funcionando y programado para el próximo reinicio, ejecuta:**

```Bash
systemctl status proxmox-sensors.service
```

**Deberías ver el estado active (running) y la indicación enabled.**

