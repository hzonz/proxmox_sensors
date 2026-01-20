"""Constantes para la integración Proxmox Custom Sensors."""

DOMAIN = "proxmox_sensors"

# Configuración de conexión
CONF_HOST = "host"
CONF_USER = "user"                # Ej: root@pam o backup@pbs
CONF_PASSWORD = "password"        # Contraseña del usuario
CONF_TOKEN_ID = "token_id"        # Nombre del Token (ej: HA-Token)
CONF_TOKEN_SECRET = "token_secret" # El Secret generado

# Configuración del servidor
CONF_NODE = "node"                # Nombre del nodo (pve, pbs, etc.)
CONF_PLATFORM_TYPE = "platform_type"  # PVE o PBS
CONF_SENSORS = "sensors"

# Tipos de servidor soportados
SERVER_PVE = "PVE"
SERVER_PBS = "PBS"

# Atributos adicionales de configuración (opcional)
CONF_VERIFY_SSL = "verify_ssl"
CONF_PORT = "port"

# Panel Proxmox
PANEL_REPO_VERSION_URL = "https://raw.githubusercontent.com/Javisen/proxmox_panel/main/panel/version.json"
PANEL_REPO_FILES_URL = "https://raw.githubusercontent.com/Javisen/proxmox_panel/main/panel/files.json"
PANEL_REPO_BASE_URL = "https://raw.githubusercontent.com/Javisen/proxmox_panel/main/panel/"

PANEL_LOCAL_PATH = "www/proxmox_panel"
PANEL_STORAGE_FILE = ".storage/proxmox_panel_version.json"

DEFAULT_PANEL_VERSION = "0.0.0"

