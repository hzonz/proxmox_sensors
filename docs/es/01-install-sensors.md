# 🚀 Paso 1: Instalación y configuración de sensores

**Esta guía explica cómo preparar el nodo Proxmox para que exponga los datos de hardware y asegure que las lecturas de temperatura estén disponibles para Home Assistant.**


## 1. Instalación de dependencias

* **Primero, instalamos las herramientas necesarias para leer los sensores integrados en la placa base y la CPU:**


```bash

apt update && apt install lm-sensors -y

```

## 2. Detección de hardware

* **Para que el sistema identifique qué controladores (drivers) necesita, ejecutamos el asistente de detección:**


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
**Dado que la API oficial de Proxmox no expone todos los datos de hardware, es necesario instalar este pequeño script "puente" en el host de Proxmox.**

1. **Descarga e instalación del script**
Ejecuta estos comandos en la terminal de tu servidor Proxmox:
```bash
# Descargar el script desde el repositorio
wget https://raw.githubusercontent.com/Javisen/proxmox_sensors/main/scripts/pve-sensors-api.py -O /usr/local/bin/pve-sensors-api.py

# Dar permisos de ejecución
chmod +x /usr/local/bin/pve-sensors-api.py
```
2. **Configuración como servicio del sistema**
Para que el script se inicie automáticamente con el servidor, crea el archivo de servicio:
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
Activa y arranca el servicio con estos comandos:
```bash
systemctl daemon-reload
systemctl enable --now pve-sensors
````

4. **Verificación final**
Puedes comprobar que el servidor está funcionando abriendo esta dirección en tu navegador (sustituyendo por la IP de tu Proxmox): `http://TU_IP_PROXMOX:9000/sensors`

Si ves un texto en formato JSON con las temperaturas, la integración ya podrá leer los datos correctamente.


**¡Listo! Una vez que el comando `sensors` devuelva datos en la terminal, tu integración de Home Assistant podrá leerlos automáticamente a través de la API de Proxmox.**
