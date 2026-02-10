# 🔐 Paso 2: Configuración de Usuarios y Permisos

**Para que Home Assistant se comunique con Proxmox de forma segura, es recomendable no utilizar el usuario root. Crearemos un usuario dedicado y le asignaremos los permisos necesarios para que la integración funcione al 100%.**

> ⚠️ **IMPORTANTE:**  
> Debido a las funciones avanzadas de la integración (control de VMs/CTs, backups individuales y masivos, acciones de PBS…), es necesario asignar **permisos de administrador** tanto en PVE como en PBS.

---

## 1. Diferencia entre PVE y PBS

### **Proxmox VE (PVE)**
- Puedes usar **Usuario/Contraseña** o **API Token**.  
- El usuario debe tener el rol **PVEAdmin**.

### **Proxmox Backup Server (PBS)**
- Es **obligatorio** usar **API Token**.  
- El usuario debe tener el rol **Administrator** (PBS no dispone de un rol intermedio válido).

---

## 2. Creación del Usuario

1. Ve a **Datacenter → Permissions → Users**  
2. Haz clic en **Add**  
3. Configura:  
   - **User:** `homeassistant`  
   - **Realm:** `pve`  
   - **Password:** solo si vas a usar login por contraseña en PVE  
4. Guarda los cambios

---

## 3. Asignación del Rol Correcto

1. Ve a **Datacenter → Permissions**  
2. Haz clic en **Add → User Permission**  
3. Configura los siguientes campos:

### ✔ Para PVE:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `PVEAdmin`  

### ✔ Para PBS:
- **Path:** `/`  
- **User:** `homeassistant@pve`  
- **Role:** `Administrator`  

> 💡 **Por qué `/` es necesario:**  
> La integración necesita acceso global para leer nodos, VMs, CTs, discos, datastores y tareas.

---

## 4. Generación del API Token (Obligatorio para PBS)

1. Ve a **Datacenter → Permissions → API Tokens**  
2. Haz clic en **Add**  
3. Configura:  
   - **User:** `homeassistant@pve`  
   - **Token ID:** `ha-token`  
   - **Privilege Separation:** **desmarcado**  
   - **Expire:** **Never**  
4. Al crear el token, Proxmox mostrará:  
   - **Token ID**  
   - **Secret** (solo se muestra una vez)

> [!WARNING]
> **Copia el "Secret" ahora y guárdalo en un lugar seguro.** Una vez cierres esta ventana, Proxmox no te lo volverá a mostrar nunca más por motivos de seguridad.


> [!TIP]
> ### 💡 ¿Has olvidado copiar el Secret?
> No te preocupes. Aunque Proxmox no te lo vuelve a mostrar por seguridad, no es necesario borrar el token y empezar de cero:
> 
> 1. En la lista de **API Tokens**, selecciona el token que ya habías creado.
> 2. Haz clic en el botón **Regenerate**.
> 3. El sistema invalidará la clave vieja inmediatamente y te entregará un **Secret nuevo**.
> 
> *Recuerda que si regeneras el Secret, deberás actualizarlo en la configuración de Home Assistant para que la integración vuelva a conectar.*
