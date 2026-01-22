# 🔐 Paso 2: Configuración de Usuarios y Permisos
**Para que Home Assistant se comunique con Proxmox de forma segura, es recomendable no utilizar el usuario root. En esta guía crearemos un acceso con permisos de "solo lectura".**

## 1. Diferencia entre PVE y PBS
Antes de empezar, debes tener en cuenta:

* **Proxmox VE (PVE): Puedes usar un Usuario/Contraseña convencional o un API Token.**

* **Proxmox Backup Server (PBS): Es imprescindible usar un API Token. Los métodos de login tradicionales a menudo fallan por restricciones de seguridad o permisos en el Datastore.**

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
  
  
##3. Creación del Usuario
1. **Ve a Datacenter > Permissions > Users.**

2. **Haz clic en Add.**

3. **Usuario: homeassistant (puedes dejar el realm como pve).**

4. **Dale una contraseña segura si vas a usar este método para PVE.**

##4. Asignación del Rol
**Debes decirle a Proxmox que ese usuario tiene el rol que creamos:**

Ve a Datacenter > Permissions.

Haz clic en Add > User Permission.

Path: / (Esto es muy importante para que vea todo el servidor).

User: homeassistant@pve.

Role: HA-Monitor.

5. Generación del API Token (Obligatorio para PBS)
Si vas a monitorizar un PBS o prefieres no usar contraseñas en PVE, haz lo siguiente:

Ve a Datacenter > Permissions > API Tokens.

Haz clic en Add.

Selecciona el usuario homeassistant.

Token ID: ha-token (por ejemplo).

IMPORTANTE: Desmarca la casilla "Privilege Separation". Si la dejas marcada, tendrías que volver a asignar permisos específicos al Token, lo cual complica el proceso.

Al darle a Add, aparecerán dos códigos:

Token ID: (Algo parecido a homeassistant@pve!ha-token).

Secret: (Una cadena larga de letras y números).

[!WARNING] Copia el "Secret" ahora y guárdalo en un lugar seguro. Una vez cierres la ventana, Proxmox no te lo volverá a mostrar nunca más por seguridad.
