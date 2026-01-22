# 🔌 Paso 3: Conexión de Proxmox VE con Home Assistant

Una vez configurado el servidor, es hora de añadir la integración en Home Assistant. Sigue estos pasos para asegurar una conexión estable.

## 1. Añadir la integración
1. En Home Assistant, ve a **Ajustes > Dispositivos y Servicios**.
2. Haz clic en el botón **Añadir Integración** y busca **Proxmox VE**.

## 2. Datos de conexión
Verás un formulario. Es vital rellenarlo exactamente así para evitar errores de autenticación:

* **Host:** La dirección IP de tu servidor (ej. `192.168.1.50`).
* **Puerto:** El puerto por defecto es `8006`.
* **Nombre de usuario:** Aquí es donde falla la mayoría. **DEBES usar el formato completo**: `usuario@realm`.
    * *Ejemplo:* `homeassistant@pve`
* **Reino (Realm):** Asegúrate de que coincida con la parte posterior al `@` de tu usuario (normalmente `pve`).
* **Verificación SSL:** Si no has instalado un certificado propio (como Let's Encrypt), **desmarca esta casilla** para evitar errores de conexión por certificado no confiable.

## 3. Método de Autenticación
Tienes dos opciones según lo que configuraste en el **Paso 2**:

### Opción A: Contraseña (Tradicional)
Simplemente introduce la contraseña que le asignaste al usuario `homeassistant` en Proxmox.

### Opción B: API Token (Recomendado)
Si prefieres no usar contraseñas y optaste por un Token:
1. **Token ID:** Introduce el identificador completo (ej. `homeassistant@pve!tu-nombre-de-token`).
2. **Secret:** Pega la clave larga que copiaste (o regeneraste) en el paso anterior.

---

## 💡 ¿Qué verás ahora?
Si la conexión es exitosa, Home Assistant descubrirá automáticamente los recursos de tu nodo y creará las siguientes entidades:

* **Estado del Sistema:** Uso de CPU, RAM y tiempo de encendido (uptime).
* **Máquinas Virtuales y Contenedores:** Sensores individuales para cada VM y LXC.
* **Almacenamiento:** Estado y espacio disponible en tus discos locales.

> [!NOTE]
> **Sensores de Temperatura:**
> Los datos de temperatura obtenidos mediante `lm-sensors` (configurados en el **Paso 1**) aparecerán como entidades independientes siempre y cuando el script de la API y su servicio *systemd* estén en ejecución.
