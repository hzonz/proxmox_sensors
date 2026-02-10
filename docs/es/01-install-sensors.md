# 🚀 Paso 1: Instalación y configuración de sensores

**Esta guía explica cómo preparar el nodo Proxmox para que exponga los datos de hardware y asegure que las lecturas de temperatura y los datos Smart estén disponibles para Home Assistant.**


## 1. Instalación de dependencias

*Para que la integración pueda leer todos los sensores de hardware y los atributos SMART de los discos, es necesario instalar las siguientes herramientas en Proxmox:*

- **lm-sensors** → Sensores de CPU, placa base, chipset, VRM, ventiladores…**
- **smartmontools** → Información SMART de HDD, SSD y NVMe**


```bash

apt update && apt install lm-sensors smartmontools -y

```

## 2. Detección de hardware

* **Ejecuta el asistente de detección para identificar los módulos necesarios:**


```bash

sensors-detect

```

**Responde YES (o pulsa Enter) a todas las preguntas. Al finalizar, el sistema identificará los módulos necesarios (por ejemplo: `coretemp` para CPUs Intel).**


## 3. Persistencia de módulos

**Para que los sensores se activen solos al reiniciar el servidor, el asistente `sensors-detect` te hará una pregunta clave al final del proceso:**


`Do you want to add these lines automatically to /etc/modules? (yes/NO)`



> [!CAUTION]
> **Debes escribir `yes` manualmente y pulsar Enter.** Si solo pulsas Enter sin escribir nada, el sistema seleccionará `NO` por defecto. Si esto ocurre, los sensores no se cargarán tras un reinicio y Home Assistant dejará de recibir datos de temperatura.



## 4. Verificación inmediata

**Para activar los sensores ahora mismo sin tener que reiniciar, ejecuta:**



```bash

# Carga los módulos detectados (ejemplo para Intel)

modprobe coretemp

# Verifica que se muestran las temperaturas

sensors

```

## 🚀 Paso 5: Instalación del Servidor de Sensores (API Bridge)
**La API oficial de Proxmox no expone todos los sensores de hardware, por lo que es necesario instalar un pequeño script que actúa como puente entre Proxmox y Home Assistant.**

1. **Descarga e instalación del script**
Ejecuta estos comandos en la terminal de tu servidor Proxmox:
```bash
# Descargar el script desde el repositorio
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Dar permisos de ejecución
chmod +x /usr/local/bin/pve-sensors-api.py
```
2. **Configuración como servicio del sistema**
Crea el archivo de servicio:
```bash
cat <<EOF > /etc/systemd/system/pve-sensors.service
[Unit]
Description=PVE Sensors API
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/pve-sensors-api.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

3. **Activación inmediata**

```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
````

4. **Verificación final**
Abre en tu navegador:
```
http://TU_IP_PROXMOX:9000/sensors
```

Si aparece un JSON con temperaturas y sensores, el servidor está funcionando correctamente.

## ✔ Conclusión

**Una vez que el comando sensors devuelve lecturas y el servicio pve-sensors está activo, Home Assistant podrá obtener todos los datos de hardware sin necesidad de configuraciones adicionalesx.**
