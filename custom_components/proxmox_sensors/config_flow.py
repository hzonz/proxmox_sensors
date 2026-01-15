from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_USER,
    CONF_PASSWORD,
    CONF_TOKEN_ID,
    CONF_TOKEN_SECRET,
    CONF_NODE,
    CONF_PLATFORM_TYPE,
)

SERVER_TYPES = {
    "PVE": "Proxmox VE",
    "PBS": "Proxmox Backup Server",
}

# Añadido: definición de sensores de nodo
NODE_SENSOR_DEFINITIONS = {
    "cpu": {"name": "CPU Usage", "unit": "%"},
    "mem": {"name": "Memory Usage", "unit": "%"},
    "uptime": {"name": "Uptime", "unit": "s"},
}


class ProxmoxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Proxmox (VE/PBS)."""

    VERSION = 1

    def __init__(self):
        self._host = None
        self._server_type = None
        self._use_token = False
        self._user = None
        self._password = None
        self._token_id = None
        self._token_secret = None
        self._node = None

        # Añadido: inicialización de todas las listas usadas en el flujo
        self._hardware_sensors = []
        self._selected_hardware = []

        self._node_sensors = {}
        self._selected_node_sensors = []

        self._disks = []
        self._selected_disks = []

        self._vms = []
        self._selected_vms = []

        self._cts = []
        self._selected_cts = []

        self._datastores = []
        self._selected_datastores = []

        self._features = {}
        self._vm_mode = "auto"
        self._ct_mode = "auto"

    # ---------------------------------------------------------
    # STEP 1 — SELECT SERVER TYPE
    # ---------------------------------------------------------
    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            self._host = user_input[CONF_HOST]
            self._server_type = user_input[CONF_PLATFORM_TYPE]
            return await self.async_step_auth_method()

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PLATFORM_TYPE, default="PVE"): vol.In(SERVER_TYPES),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    # ---------------------------------------------------------
    # STEP 2 — SELECT AUTH METHOD
    # ---------------------------------------------------------
    async def async_step_auth_method(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            self._use_token = user_input.get("use_token", False)
            return await self.async_step_credentials()

        schema = vol.Schema(
            {
                vol.Required("use_token", default=False): bool,
            }
        )

        return self.async_show_form(
            step_id="auth_method",
            data_schema=schema,
            errors=errors,
        )

    # ---------------------------------------------------------
    # STEP 3 — CREDENTIALS
    # ---------------------------------------------------------
    async def async_step_credentials(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            self._user = user_input[CONF_USER]

            if self._use_token:
                self._token_id = user_input[CONF_TOKEN_ID]
                self._token_secret = user_input[CONF_TOKEN_SECRET]
                if self._server_type == "PVE":
                    self._node = user_input[CONF_NODE]
            else:
                self._password = user_input[CONF_PASSWORD]
                if self._server_type == "PVE":
                    self._node = user_input[CONF_NODE]

            # No cargamos sensores aquí. Solo guardamos datos.
            return self.async_create_entry(
                title=f"Proxmox {self._host}",
                data={
                    CONF_HOST: self._host,
                    CONF_PLATFORM_TYPE: self._server_type,
                    CONF_USER: self._user,
                    CONF_PASSWORD: self._password,
                    CONF_TOKEN_ID: self._token_id,
                    CONF_TOKEN_SECRET: self._token_secret,
                    CONF_NODE: self._node,
                    "use_token": self._use_token,
                },
            )

        # Crear esquema según si es token o contraseña
        if self._use_token:
            schema_dict = {
                vol.Required(CONF_USER): str,
                vol.Required(CONF_TOKEN_ID): str,
                vol.Required(CONF_TOKEN_SECRET): str,
            }
            if self._server_type == "PVE":
                schema_dict[vol.Required(CONF_NODE)] = str
        else:
            schema_dict = {
                vol.Required(CONF_USER): str,
                vol.Required(CONF_PASSWORD): str,
            }
            if self._server_type == "PVE":
                schema_dict[vol.Required(CONF_NODE)] = str

        schema = vol.Schema(schema_dict)

        return self.async_show_form(
            step_id="credentials",
            data_schema=schema,
            errors=errors,
        )

    # ---------------------------------------------------------
    # STEP 4 — SELECT FEATURES
    # ---------------------------------------------------------
    async def async_step_select_features(self, user_input=None) -> FlowResult:
        if user_input is not None:
            self._features = user_input
            return await self._next_feature_step()

        schema = vol.Schema(
            {
                vol.Optional("enable_hardware", default=True): bool,
                vol.Optional("enable_node", default=True): bool,
                vol.Optional("enable_disks", default=True): bool,
                vol.Optional("enable_vms", default=False): bool,
                vol.Optional("enable_cts", default=False): bool,
                vol.Optional("enable_pbs_datastores", default=True): bool,
                vol.Optional("enable_pbs_tasks", default=True): bool,
            }
        )

        return self.async_show_form(step_id="select_features", data_schema=schema)

    async def _next_feature_step(self):
        if self._features.get("enable_hardware"):
            return await self.async_step_select_hardware_sensors()
        if self._features.get("enable_node"):
            return await self.async_step_select_node_sensors()
        if self._features.get("enable_disks"):
            return await self.async_step_select_disks()
        if self._features.get("enable_vms"):
            return await self.async_step_vm_mode()
        if self._features.get("enable_cts"):
            return await self.async_step_ct_mode()
        if self._features.get("enable_pbs_datastores"):
            return await self.async_step_select_datastores()
        return await self._finish()

    # ---------------------------------------------------------
    # HARDWARE SENSORS
    # ---------------------------------------------------------
    async def async_step_select_hardware_sensors(self, user_input=None):
        if user_input is not None:
            self._selected_hardware = user_input["hardware_sensors"]
            return await self._next_feature_step()

        options = (
            {s["id"]: f"{s['name']} ({s['value']}{s['unit']})" for s in self._hardware_sensors}
            if self._hardware_sensors else {}
        )

        schema = vol.Schema({vol.Required("hardware_sensors"): vol.MultipleChoice(options)})

        return self.async_show_form(step_id="select_hardware_sensors", data_schema=schema)

    # ---------------------------------------------------------
    # NODE SENSORS
    # ---------------------------------------------------------
    async def async_step_select_node_sensors(self, user_input=None):
        if user_input is not None:
            self._selected_node_sensors = user_input["node_sensors"]
            return await self._next_feature_step()

        options = {key: f"{info['name']} ({info['unit']})" for key, info in NODE_SENSOR_DEFINITIONS.items()}

        schema = vol.Schema({vol.Required("node_sensors"): vol.MultipleChoice(options)})

        return self.async_show_form(step_id="select_node_sensors", data_schema=schema)

    # ---------------------------------------------------------
    # DISKS
    # ---------------------------------------------------------
    async def async_step_select_disks(self, user_input=None):
        if user_input is not None:
            self._selected_disks = user_input["disks"]
            return await self._next_feature_step()

        options = (
            {d["id"]: f"{d['name']} ({d['usage_pct']}%)" for d in self._disks}
            if self._disks else {}
        )

        schema = vol.Schema({vol.Required("disks"): vol.MultipleChoice(options)})

        return self.async_show_form(step_id="select_disks", data_schema=schema)

    # ---------------------------------------------------------
    # VMs
    # ---------------------------------------------------------
    async def async_step_vm_mode(self, user_input=None):
        if user_input is not None:
            self._vm_mode = user_input["vm_mode"]
            if self._vm_mode == "manual":
                return await self.async_step_select_vms()
            return await self._next_feature_step()

        schema = vol.Schema({vol.Required("vm_mode", default="auto"): vol.In({"auto": "Automático", "manual": "Manual"})})

        return self.async_show_form(step_id="vm_mode", data_schema=schema)

    async def async_step_select_vms(self, user_input=None):
        if user_input is not None:
            self._selected_vms = user_input["vms"]
            return await self._next_feature_step()

        options = (
            {vm["id"]: f"{vm['name']} ({vm['status']})" for vm in self._vms}
            if self._vms else {}
        )

        schema = vol.Schema({vol.Required("vms"): vol.MultipleChoice(options)})

        return self.async_show_form(step_id="select_vms", data_schema=schema)

    # ---------------------------------------------------------
    # CONTAINERS
    # ---------------------------------------------------------
    async def async_step_ct_mode(self, user_input=None):
        if user_input is not None:
            self._ct_mode = user_input["ct_mode"]
            if self._ct_mode == "manual":
                return await self.async_step_select_containers()
            return await self._next_feature_step()

        schema = vol.Schema({vol.Required("ct_mode", default="auto"): vol.In({"auto": "Automático", "manual": "Manual"})})

        return self.async_show_form(step_id="ct_mode", data_schema=schema)

    async def async_step_select_containers(self, user_input=None):
        if user_input is not None:
            self._selected_cts = user_input["cts"]
            return await self._next_feature_step()

        options = (
            {ct["id"]: f"{ct['name']} ({ct['status']})" for ct in self._cts}
            if self._cts else {}
        )

        schema = vol.Schema({vol.Required("cts"): vol.MultipleChoice(options)})

        return self.async_show_form(step_id="select_containers", data_schema=schema)

    # ---------------------------------------------------------
    # PBS DATASTORES
    # ---------------------------------------------------------
    async def async_step_select_datastores(self, user_input=None):
        if user_input is not None:
            self._selected_datastores = user_input["datastores"]
            return await self._finish()

        options = {store: store for store in self._datastores} if self._datastores else {}

        schema = vol.Schema({vol.Required("datastores"): vol.MultipleChoice(options)})

        return self.async_show_form(step_id="select_datastores", data_schema=schema)

    # ---------------------------------------------------------
    # FINAL STEP
    # ---------------------------------------------------------
    async def _finish(self):
        data = {
            CONF_HOST: self._host,
            CONF_USER: self._user,
            CONF_TOKEN_ID: self._token_id,
            CONF_TOKEN_SECRET: self._token_secret or self._password,
            CONF_NODE: self._node,
            CONF_PLATFORM_TYPE: self._server_type,
            "features": self._features,
            "hardware_sensors": self._selected_hardware,
            "node_sensors": self._selected_node_sensors,
            "disks": self._selected_disks,
            "vm_mode": self._vm_mode,
            "vms": self._selected_vms,
            "ct_mode": self._ct_mode,
            "cts": self._selected_cts,
            "datastores": self._selected_datastores,
        }

        return self.async_create_entry(
            title=f"Proxmox {self._node}",
            data=data,
        )

