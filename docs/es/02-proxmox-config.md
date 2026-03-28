# 🔐 Paso 2: Configuración de Usuarios y Permisos

Para que Home Assistant se comunique con Proxmox de forma segura, se recomienda **no utilizar el usuario root**.

En su lugar, crearemos un usuario dedicado con los permisos necesarios para que la integración funcione correctamente.

---

> ⚠️ **IMPORTANTE**  
> Debido a las funcionalidades avanzadas de la integración (control de VMs/CTs, backups, acciones sobre PBS, etc.), es necesario asignar permisos elevados en Proxmox.
>
> Estos permisos permiten:
> - Controlar máquinas virtuales y contenedores  
> - Ejecutar backups (individuales y masivos)  
> - Acceder a información de nodos, discos y tareas  
> - Interactuar con Proxmox Backup Server (PBS)  
>
> Aunque se trata de permisos amplios, el uso de un **usuario dedicado + API Token** mantiene el acceso aislado y controlado.

---

## 1. Diferencia entre PVE y PBS

### 🖥️ Proxmox VE (PVE)
- Permite autenticación mediante:
  - Usuario/Contraseña  
  - API Token  
- El usuario debe tener el rol **PVEAdmin**  

---

### 🗄️ Proxmox Backup Server (PBS)
- Requiere **API Token** obligatoriamente  
- El usuario debe tener el rol **Administrator**  
- No existe un rol intermedio compatible con todas las funciones  

---

## 2. Creación del usuario

1. Ve a **Datacenter → Permissions → Users**  
2. Haz clic en **Add**  
3. Configura:

- **User:** `homeassistant`  
- **Realm:** `pve`  
- **Password:** (solo si usarás login por contraseña en PVE)

4. Guarda los cambios  

---

## 3. Asignación de permisos

1. Ve a **Datacenter → Permissions**  
2. Haz clic en **Add → User Permission**  

---

### ✔ Para Proxmox VE (PVE)

- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

---

### ✔ Para Proxmox Backup Server (PBS)

- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

---

> 💡 **Por qué usar `/` (acceso global)**  
> La integración necesita acceso a toda la infraestructura:
> nodos, VMs, contenedores, discos, storages y tareas.

---

## 4. Creación del API Token

1. Ve a **Datacenter → Permissions → API Tokens**  
2. Haz clic en **Add**  
3. Configura:

- **User:** `homeassistant@pve`  
- **Token ID:** `ha-token`  
- **Privilege Separation:** ❌ Desmarcado  
- **Expire:** Never  

---

### 🔍 ¿Por qué desactivar "Privilege Separation"?

Porque el token necesita heredar los permisos completos del usuario.

Si se activa esta opción:
- el token tendrá permisos limitados  
- algunas funciones (backups, control, PBS) no funcionarán correctamente  

---

4. Al crear el token, Proxmox mostrará:

- **Token ID**  
- **Secret** (solo visible una vez)

---

> [!WARNING]
> Guarda el **Secret** en un lugar seguro.  
> No podrá volver a visualizarse una vez cierres esta ventana.

---

> [!TIP]
> ### 💡 ¿Has olvidado copiar el Secret?
> No es necesario eliminar el token:
>
> 1. Selecciona el token en la lista  
> 2. Haz clic en **Regenerate**  
> 3. Se generará un nuevo Secret inmediatamente  
>
> ⚠️ Recuerda actualizarlo en Home Assistant.

---

## ✔ Conclusión

Una vez configurado:

- Usuario dedicado  
- Permisos correctamente asignados  
- API Token creado  

La integración podrá conectarse a Proxmox de forma segura y con acceso completo a todas sus funcionalidades.