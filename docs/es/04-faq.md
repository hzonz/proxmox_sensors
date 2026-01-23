# ❓ FAQ — Preguntas Frecuentes

A continuación encontrarás las dudas y problemas más comunes al usar la integración **Proxmox Sensors Extended**, junto con sus soluciones rápidas.

---

## 🔐 No puedo iniciar sesión en la integración (PVE o PBS)

### ✔ 1. No debes poner `http://` ni `https://`
Introduce **solo el dominio o IP**, por ejemplo:

`192.168.1.10
pve.mi-dominio.com`


### ✔ 2. No debes poner el puerto
La integración detecta automáticamente el puerto correcto.

### ✔ 3. Revisa los permisos del Token API
El usuario debe tener:

- **PVE:**  
  - `Sys.Audit`  
  - `VM.Audit`  
  - `Datastore.Audit`  
  - `Permissions.Modify` (solo si usas selección automática de VMs/LXCs)

- **PBS:**  
  - `Datastore.Audit`  
  - `Datastore.Read`  
  - `Sys.Audit`

### ✔ 4. Asegúrate de que el Token está activo
En Proxmox → Datacenter → Permissions → API Tokens  
Debe aparecer **Enabled: Yes**.

---

## 🔑 Me dice “Permiso denegado” aunque el Token es correcto

Esto suele deberse a:

### ✔ 1. El Token no tiene permisos en la raíz `/`
En Proxmox, los permisos deben asignarse en: `/ (root)` **No en un nodo concreto.**

### ✔ 2. El Token pertenece a un usuario sin permisos
El usuario padre debe tener permisos, no solo el Token.

---

## 🌐 La integración no detecta mi PBS de Tuxis

Esto es normal.

Los PBS gestionados por Tuxis **no permiten acceder a métricas internas** mediante API:

- espacio del datastore  
- uso del disco  
- estadísticas RRD  
- hardware del nodo  
- temperatura  
- SMART  
- CPU/RAM  

Esto no es un error de la integración:  
Tuxis bloquea estos endpoints por diseño.

La integración detecta automáticamente que es un PBS de Tuxis y oculta los sensores no disponibles.

---

## 📦 No veo sensores de espacio del datastore en PBS

### ✔ Si tu PBS es de Tuxis → **no están disponibles**
Por motivos de seguridad, Tuxis bloquea: `/api2/json/admin/datastore/<name>/status`


Sin ese endpoint, no es posible obtener:

- espacio total  
- espacio libre  
- porcentaje de uso  
- deduplicación  
- chunks  
- GC  

---

## 🌡️ No aparecen sensores de temperatura en PVE

### ✔ 1. Debes instalar `lm-sensors` en el nodo
Guía completa: `01-install-sensors.md`

### ✔ 2. Debes ejecutar `sensors-detect`
Y aceptar todas las opciones seguras.

### ✔ 3. Debes cargar los módulos recomendados
Ejemplo:

```bash
modprobe coretemp
modprobe nct6775
```
### ✔ 4. Debes crear el servicio systemd
Para que los sensores funcionen tras reiniciar.

## 🖥️ No aparecen sensores de discos NVMe/SSD/HDD
### ✔ 1. El disco debe soportar lectura de temperatura
Algunos modelos OEM no exponen sensores.

### ✔ 2. En NVMe virtualizados (VMs) no hay sensores
Solo funcionan en hardware real.

### ✔ 3. En PBS de Tuxis no se exponen sensores de disco
Limitación del proveedor.

## 🧠 No aparecen mis VMs o contenedores

### ✔ 1. Revisa permisos del Token
Debe tener: `VM.Audit`

### ✔ 2. Si usas selección automática
La integración necesita: 'Permissions.Modify`

### ✔ 3. Si usas clúster
Debes conectarte al nodo principal, no a un nodo secundario.

## 🔄 La integración tarda en actualizar los valores
Esto es normal.

La integración usa 'DataUpdateCoordinator` para:

* evitar saturar la API
* reducir carga en el nodo
* mejorar rendimiento

**El intervalo por defecto es 10 segundos, configurable.**

## 🧩 ¿Puedo usar varios PVE y PBS a la vez?
### Sí.
La integración permite añadir múltiples instancias, cada una con su propio Token.

## 🔒 ¿Es seguro usar Tokens API?
###Sí.

La integración:

* no almacena contraseñas
* usa solo Tokens con permisos mínimos
* no ejecuta comandos en el servidor
* no modifica la configuración de Proxmox
* no abre puertos adicionales

## 🧹 ¿Cómo elimino sensores antiguos?
**Home Assistant elimina automáticamente entidades huérfanas.**

**Si quieres forzar la limpieza:**

* Elimina la integración
* Reinicia Home Assistant
* Añádela de nuevo

##🛠️ ¿Dónde puedo reportar errores?
**Puedes abrir un issue en GitHub con:**

* versión de HA
* versión de Proxmox
* logs relevantes
* pasos para reproducir
* tipo de servidor (PVE, PBS, Tuxis, etc.)
