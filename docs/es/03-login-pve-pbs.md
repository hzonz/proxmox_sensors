# 🔌 Paso 3: Instalación de la Integración en Home Assistant

Para visualizar los datos (incluyendo temperaturas, sensores de hardware, discos, PBS, VMs y CTs), utilizaremos la integración **Proxmox Extended Sensors**.

---

## 1. Instalación mediante HACS

Al ser una integración personalizada, primero debemos añadirla a HACS:

1. Ve a **HACS → Integraciones**  
2. Haz clic en los **tres puntos** (arriba a la derecha)  
3. Selecciona **Repositorios personalizados**  
4. Añade este repositorio: `https://github.com/Javisen/proxmox_sensors/`
5. En **Categoría**, selecciona `Integración`  
6. Instálala y **reinicia Home Assistant**

---

## 2. Configuración de la Integración

Una vez reiniciado:

1. Ve a **Ajustes → Dispositivos y Servicios**  
2. Haz clic en **Añadir Integración**  
3. Busca **Proxmox Extended Sensors**

---

## 3. Datos de Conexión

El formulario es sencillo, pero hay detalles importantes:

### 🔹 Host
- **En red local:** solo la IP → `192.168.1.50`  
*(No pongas puerto ni http/https)*  
- **Desde el exterior:** tu dominio → `proxmox.midominio.com`  
*(La integración detecta automáticamente http/https)*

### 🔹 Tipo de servidor
- **PVE** → Proxmox Virtual Environment  
- **PBS** → Proxmox Backup Server  

### 🔹 Método de autenticación
- **Login tradicional** (solo PVE)  
- **API Token** (obligatorio en PBS)

---

## 🔐 Opción A: Login con Usuario (sin Token)

Solo válido para **PVE**.

Campos:

- **User:** `usuario@realm`  
Ejemplos:  
- `homeassistant@pve`  
- `root@pam`  
- **Password:** la contraseña del usuario  
- **Node Name:** nombre del nodo (tal como aparece en Proxmox)

---

## 🔐 Opción B: Login con Token (recomendado y obligatorio en PBS)

Campos:

- **User:** `usuario@realm`  
- **token_id:** solo el nombre del token → `ha-token`  
*(No pongas `usuario@pve!token`)*  
- **Token_secret:** el Secret generado por Proxmox  

---

## ✅ Selección de Entidades (solo en PVE)

Tras conectar, la integración escaneará tu servidor y podrás elegir qué monitorizar:

- **VMs**  
- **CTs**  
- **Discos físicos**  
- **Storages**  

> [!TIP]  
> Selecciona solo lo que necesites para mantener Home Assistant limpio y rápido.

---
## 🧭 Guia Visual de Instalación

**A continuación puede encontrar un recorrido visual completo del proceso de configuración, incluidos los métodos de inicio de sesión, la selección de recursos y los pasos de configuración.**

<details>
  <summary>🪪 Captura: Server Connection</summary>
  <p align="center">
    <img src="img/install/setup_pve_1.png" alt="Login Proxmox" width="600">
  </p>
  > No se usa "http://" ni "https://". Ya lo hacemos por tí.
</details>

<details>
  <summary>🪪 Captura: Loguin mediante User y Password (solo PVE)</summary>
  <p align="center">
    <img src="img/install/access_passw.png" alt="Login Proxmox" width="600">
  </p>
  > Asegúrate de usar el reino `pam` o `pve` según tu configuración de usuario.
</details>

<details> 
  <summary>🪪 Captura: Loguin mediante User y Token (PVE y PBS)</summary>
  <p align="center">
    <img src="img/install/access_token.png" alt="Login Proxmox" width="600">
  </p>
  **En el campo Token_id solo se debe poner el nombre del token**
</details>

<details>
  <summary>⚙️ Captura: Resources Selection</summary>
  <p align="center">
    <img src="img/install/resources_select.png" alt="Login Proxmox" width="600">
  </p>
  *Nota: Selecciona los CTs, VMs y Storages que quieres añadir así como las opciones*
</details>

---


## ⚠️ Nota importante para PBS en entornos compartidos (Tuxis, Hetzner, etc.)

Si usas un PBS **gestionado** o **multi‑tenant**, como Tuxis Free PBS:

- No verás sensores de hardware  
- No verás temperaturas  
- No verás discos físicos  
- No verás métricas del nodo  

Esto es normal porque:

- No tienes acceso al hardware real  
- El proveedor oculta la infraestructura  
- No tienes permisos root  
- No puedes acceder al filesystem real  

**Resultado:**  
La integración solo mostrará sensores vacíos o sin datos.  
En futuras versiones intentaremos mostrar métricas del datastore personal.
