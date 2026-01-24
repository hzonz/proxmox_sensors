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

>  **Debes escribir `yes` manualmente y pulsar Enter.** Si solo pulsas Enter sin escribir nada, el sistema seleccionará `NO` por defecto. Si esto ocurre, los sensores no se cargarán tras un reinicio y Home Assistant dejará de recibir datos de temperatura.



## 4. Verificación inmediata

**Para activar los sensores ahora mismo sin tener que reiniciar, ejecuta:**



```bash

# Carga los módulos detectados (ejemplo para Intel)

modprobe coretemp

# Verifica que se muestran las temperaturas

sensors

```



**¡Listo! Una vez que el comando `sensors` devuelva datos en la terminal, tu integración de Home Assistant podrá leerlos automáticamente a través de la API de Proxmox.**
