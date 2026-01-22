# 🔐 Paso 2: Configuración de Usuarios y Permisos
**Para que Home Assistant se comunique con Proxmox de forma segura, es recomendable no utilizar el usuario root. En esta guía crearemos un acceso con permisos de "solo lectura".**

## 1. Diferencia entre PVE y PBS
Antes de empezar, debes tener en cuenta:

* **Proxmox VE (PVE): Puedes usar un Usuario/Contraseña convencional o un API Token.**

* **Proxmox Backup Server (PBS): Es imprescindible usar un API Token. Los métodos de login tradicionales a menudo fallan por restricciones de seguridad o permisos en el Datastore.**

---

## 2. Creación del Rol (Permisos)
**Un "Rol" define qué puede hacer la integración.**

1. Ve a Datacenter > Permissions > Roles.

2. Haz clic en Create y ponle de nombre HA-Monitor.

## 3. Creación del Rol (Permisos)
Un "Rol" define qué puede hacer la integración.
1. Ve a **Datacenter > Permissions > Roles**.
2. Haz clic en **Create** y ponle de nombre `HA-Monitor`.
3. Selecciona los siguientes privilegios (**Privileges**):
    * `Sys.Audit`: Permite ver el estado del nodo (CPU, RAM).
    * `VM.Audit`: Permite ver el estado de las VMs y contenedores.
    * `Datastore.Audit`: Permite ver el espacio en disco.

---
  
## 4. Creación del Usuario
1. **Ve a Datacenter > Permissions > Users.**

2. **Haz clic en Add.**

3. **Usuario: homeassistant (puedes dejar el realm como pve).**

4. **Dale una contraseña segura si vas a usar este método para PVE.**

---

## 5. Asignación del Rol
**Debes decirle a Proxmox que ese usuario tiene el rol que creamos:**

1. Ve a **Datacenter > Permissions**.
2. Haz clic en **Add > User Permission**.
3. Configura los siguientes campos:
    * **Path:** `/` (Esto es muy importante para que la integración pueda ver todo el servidor).
    * **User:** `homeassistant@pve` (o el usuario que hayas creado).
    * **Role:** `HA-Monitor`.

---

## 6. Generación del API Token (Obligatorio para PBS)
**Si vas a monitorizar un PBS o prefieres no usar contraseñas en PVE, realiza estos pasos:**

1. Ve a **Datacenter > Permissions > API Tokens**.
2. Haz clic en **Add** y rellena el formulario:
    * **User:** Selecciona el usuario `homeassistant`.
    * **Token ID:** `ha-token` (puedes elegir el nombre que quieras).
    * **Privilege Separation:** ⚠️ **DESMARCA esta casilla**. Si la dejas marcada, el Token no heredará los permisos del usuario y la integración fallará.
3. Al hacer clic en **Add**, se abrirá una ventana con dos datos clave:
    * **Token ID:** (Ejemplo: `homeassistant@pve!ha-token`).
    * **Secret:** (Una cadena larga de letras y números).

> [!WARNING]
> **Copia el "Secret" ahora y guárdalo en un lugar seguro.** Una vez cierres esta ventana, Proxmox no te lo volverá a mostrar nunca más por motivos de seguridad. Si lo pierdes, tendrás que borrar el token y crear uno nuevo.
