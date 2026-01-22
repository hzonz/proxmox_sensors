#📘 Instalación y configuración de lm‑sensors en Proxmox

(con servicio systemd que no consume recursos)

##🟦 Introducción

**lm-sensors es una herramienta que permite leer temperaturas, voltajes y velocidades de ventiladores directamente desde el hardware del nodo Proxmox.**

**Es imprescindible para exponer métricas fiables al sistema y, por extensión, a integraciones externas como Home Assistant.**

**Esta guía explica cómo:**

* **Instalar lm-sensors**

* **Detectar y activar los sensores del hardware**

* **Crear un servicio systemd moderno**

* **Garantizar que los sensores se inicializan automáticamente en cada arranque**

**Todo ello de forma segura y sin afectar al rendimiento del nodo.**

---

###🟩 ¿Consume recursos lm‑sensors?
**No.**
lm-sensors no es un demonio, no se queda ejecutándose en segundo plano y no usa CPU ni RAM de forma continua.

**El servicio que configuramos:**

* **solo ejecuta un comando de inicialización al arrancar**

* **termina inmediatamente**

* **no deja procesos activos**

* **no abre puertos**

* **no interfiere con Proxmox, QEMU, LXC ni ZFS**

En otras palabras:

**✔ No se queda en memoria**

**✔ No genera carga**

**✔ No afecta al rendimiento del nodo**

**✔ Es completamente seguro instalarlo**

---

##🟧 1. Instalación de paquetes
Ejecuta en el nodo Proxmox:

```bash
apt update
apt install lm-sensors
```

**Esto instala:**

sensors → comando principal

drivers de lectura de hardware

scripts de detección

🟧 2. Detección automática de sensores
Ejecuta:

bash
sensors-detect
Responde YES a todas las preguntas seguras.

Al final verás algo como:

Código
To load everything that is needed, add this to /etc/modules:
coretemp
nct6775
Si te recomienda módulos, añádelos:

bash
echo coretemp >> /etc/modules
echo nct6775 >> /etc/modules
Cárgalos sin reiniciar:

bash
modprobe coretemp
modprobe nct6775
🟧 3. Verificación de sensores
Comprueba que todo funciona:

bash
sensors
Ejemplo de salida:

Código
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  42.0°C
Core 0:        38.0°C
Core 1:        39.0°C
Si ves lecturas, los sensores están funcionando.

🟧 4. Crear un servicio systemd para inicializar los sensores
Aunque lm-sensors no necesita ejecutarse como daemon, Proxmox a veces no ejecuta correctamente el script de inicialización.
Por eso creamos un servicio systemd moderno que:

se ejecuta una sola vez al arrancar

inicializa los sensores

no permanece en memoria

Crear el archivo:
bash
nano /etc/systemd/system/lm-sensors.service
Contenido:

ini
[Unit]
Description=Initialize hardware monitoring sensors
DefaultDependencies=no
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/sensors -s
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
🟧 5. Activar y arrancar el servicio
bash
systemctl daemon-reload
systemctl enable lm-sensors
systemctl start lm-sensors
Comprobar:

bash
systemctl status lm-sensors
Y luego:

bash
sensors
Si ves lecturas → todo correcto.

🟧 6. Notas específicas para Proxmox
✔ Módulos típicos según hardware
Hardware	Módulo
Intel	coretemp
AMD Ryzen	k10temp
Placas base con SuperIO	nct6775 / nct6779
Servidores Dell/HP	ipmi_devintf (requiere ipmitool)
✔ Para IPMI (servidores)
bash
apt install ipmitool
modprobe ipmi_devintf
🟧 7. Problemas comunes y soluciones
❌ sensors no muestra nada
✔ Comprueba módulos:

bash
lsmod | grep coretemp
lsmod | grep k10temp
Si no aparecen:

bash
modprobe coretemp
❌ El servicio no se ejecuta al arrancar
✔ Revisa:

bash
systemctl enable lm-sensors
✔ Mira el log:

bash
journalctl -u lm-sensors
❌ No detecta sensores de la placa base
✔ Instala herramientas I2C:

bash
apt install i2c-tools
✔ Repite:

bash
sensors-detect
