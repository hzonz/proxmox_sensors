# 🔌 Paso 3: Instalación de la Integración en Home Assistant

Para visualizar los datos (incluyendo las temperaturas de hardware), utilizaremos la integración **Proxmox Extended Sensors**.

## 1. Instalación mediante HACS
Al ser una integración personalizada, primero debemos añadirla a nuestra tienda HACS:

1. Ve a **HACS > Integraciones**.
2. Haz clic en los tres puntos de la esquina superior derecha y selecciona **Repositorios personalizados**.
3. Pega la URL de este repositorio: `https://github.com/Javisen/proxmox_sensors/`
4. En **Categoría**, selecciona `Integración` y haz clic en **Añadir**.
5. Busca la integración, instálala y **reinicia Home Assistant**.

## 2. Configuración de la Integración
Una vez reiniciado, sigue estos pasos:

1. Ve a **Ajustes > Dispositivos y Servicios**.
2. Haz clic en **Añadir Integración** y busca `Proxmox Extended Sensors`.

## 3. Datos de Conexión
El formulario de login es muy sencillo, pero presta atención a estos detalles:

* **Host:** * Si es en tu red local: Pon solo la IP (ej. `192.168.1.50`). **No hace falta poner el puerto**.
    * Si accedes desde el exterior: Pon tu dominio. **No escribas `http://` ni `https://`**, la integración lo detecta automáticamente.
* **Tipo de servidor:** Selecciona entre **PVE** (Proxmox Virtual Environment) o **PBS** (Proxmox Backup Server).
* **Usar Token:** Selecciona si vas a usar el API Token creado en el Paso 2 o login tradicional.

### Opción A: Login con Usuario (Sin Token)
Si prefieres no usar token, rellena estos campos:
* **User:** Siempre con el formato `usuario@realm` (ejemplo: `homeassistant@pve` o `root@pam`).
* **Password:** La contraseña del usuario.
* **Node Name:** El nombre de tu nodo Proxmox (el que aparece en el árbol de la izquierda en la web de Proxmox).

### Opción B: Login con Token (Obligatorio en PBS)
Si prefieres usar token, rellena estos campos:
* **User:** Siempre con el formato `usuario@realm` (ejemplo: `homeassistant@pve` o `root@pam`).
* **token_id:** El nombre identificador que le diste al token (ejemplo: `ha-token`). No confundir con el ID completo.
* **Token_secret:** La cadena de caracteres (secreto) que generó Proxmox.

---

## ✅ Selección de Entidades (SOLO EN ENTORNO PVE)
Una vez que hagas clic en enviar, la integración (en modo PVE) escaneará tu servidor y te permitirá elegir qué quieres monitorizar:
* **VMs:** Máquinas virtuales específicas.
* **CTs:** Contenedores LXC.
* **Discos Físicos:** Discos duros y SSDs conectados.
* **Storages:** Particiones de almacenamiento y su espacio libre.

> [!TIP]
> **Solo selecciona lo que realmente necesites.** Esto mantendrá tu Home Assistant limpio y con mejor rendimiento.
