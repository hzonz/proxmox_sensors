# ❓ FAQ — Preguntas Frecuentes

A continuación encontrarás las dudas y problemas más comunes al usar la integración **Proxmox Sensors Extended**, junto con sus soluciones rápidas.

---

## 🔐 No puedo iniciar sesión en la integración (PVE o PBS)

### ✔ 1. No debes poner `http://` ni `https://`
Introduce **solo el dominio o IP**, por ejemplo:

`192.168.1.10
pve.mi-dominio.com`

---

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

---

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
Guía completa: [01. Configuración de Sensores de Hardware](01-install-sensors.md)

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

---

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

---

## 🔄 La integración tarda en actualizar los valores
Esto es normal.

La integración usa 'DataUpdateCoordinator` para:

* evitar saturar la API
* reducir carga en el nodo
* mejorar rendimiento

**El intervalo por defecto es 10 segundos, configurable.**

---

## 🧩 ¿Puedo usar varios PVE y PBS a la vez?
### Sí.
La integración permite añadir múltiples instancias, cada una con su propio Token.

---

## 🔒 ¿Es seguro usar Tokens API?
###Sí.

La integración:

* no almacena contraseñas
* usa solo Tokens con permisos mínimos
* no ejecuta comandos en el servidor
* no modifica la configuración de Proxmox
* no abre puertos adicionales

---

## 🧹 ¿Cómo elimino sensores antiguos?
**Home Assistant elimina automáticamente entidades huérfanas.**

**Si quieres forzar la limpieza:**

* Elimina la integración
* Reinicia Home Assistant
* Añádela de nuevo

---

##🛠️ ¿Dónde puedo reportar errores?
**Puedes abrir un issue en GitHub con:**

* versión de HA
* versión de Proxmox
* logs relevantes
* pasos para reproducir
* tipo de servidor (PVE, PBS, Tuxis, etc.)

---

# 🧾 Checklist antes de abrir un Issue

Antes de reportar un problema, revisa esta lista rápida.  
El 90% de los errores se solucionan aquí:

### ✔ 1. ¿Puedes acceder a Proxmox desde el navegador?
Si no puedes entrar en la web de PVE/PBS, la integración tampoco podrá.

### ✔ 2. ¿Estás usando solo el dominio/IP?
No pongas `http://`, `https://` ni puertos.

### ✔ 3. ¿El Token API está activo?
En Proxmox → Datacenter → Permissions → API Tokens  
Debe aparecer **Enabled: Yes**.

### ✔ 4. ¿El usuario tiene permisos en la raíz `/`?
Los permisos deben asignarse en: `/ (root)` No en un nodo concreto.

### ✔ 5. ¿Has instalado y configurado `lm-sensors` en PVE?
Sin esto, no aparecerán sensores de hardware.

### ✔ 6. ¿El PBS es de Tuxis?
Si es así, recuerda que **no expone métricas internas** (espacio, hardware, RRD).

### ✔ 7. ¿Has reiniciado Home Assistant tras cambiar permisos?
HA cachea permisos antiguos.

### ✔ 8. ¿Hay errores en los logs de Home Assistant?
Ve a:  
**Ajustes → Registros → Integraciones**

### ✔ 9. ¿Has probado en modo incógnito?
El frontend de HA cachea recursos durante semanas.

---

# 🚫 Limitaciones Conocidas

Estas limitaciones no son errores de la integración, sino restricciones de Proxmox o del proveedor:

### 🔒 1. PBS de Tuxis
Los servidores PBS gestionados por Tuxis **no permiten acceder a:**

- espacio del datastore  
- uso del disco  
- deduplicación  
- chunks  
- estadísticas RRD  
- hardware del nodo  
- temperatura  
- SMART  
- CPU/RAM  

La integración detecta automáticamente esta limitación y oculta los sensores no disponibles.

---

### 🧊 2. Sensores de hardware en máquinas virtuales
Las VMs **no exponen sensores reales**:

- temperaturas  
- ventiladores  
- voltajes  
- SMART  

Solo funcionan en hardware físico.

---

### 📦 3. Discos NVMe/SSD sin sensores
Algunos modelos OEM o controladoras RAID **no exponen temperatura** ni estado SMART.

---

### 🔐 4. Tokens sin permisos en `/`
Si los permisos se asignan a un nodo en lugar de a la raíz, Proxmox bloquea la API.

---

### 🕒 5. Intervalos de actualización
Para evitar saturar la API, la integración usa un intervalo mínimo de actualización.  
No es un error si los valores tardan unos segundos en actualizarse.

---

### 🧩 6. Clústeres Proxmox
Debes conectarte al **nodo principal** del clúster.  
Los nodos secundarios no exponen toda la API.

---

### 🌐 7. Certificados SSL autofirmados
La integración los acepta automáticamente, pero algunos navegadores pueden mostrar advertencias.

---

