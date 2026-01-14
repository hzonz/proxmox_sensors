from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_USER,
    CONF_TOKEN_ID,
    CONF_TOKEN_SECRET,
    CONF_NODE,
    CONF_PLATFORM_TYPE,
    CONF_SENSORS,
)

from .api import ProxmoxClient


SERVER_TYPES = {
    "PVE": "Proxmox VE",
    "PBS": "Proxmox Backup Server",
}

NODE_SENSOR_DEFINITIONS = {
    "cpu_usage_pct": {"name": "CPU Usage", "unit": "%"},
    "ram_usage_pct": {"name": "RAM Usage", "unit": "%"},
    "ram_used": {"name": "RAM Used", "unit": "bytes"},
    "ram_total": {"name": "RAM Total", "unit": "bytes"},
    "uptime": {"name": "Uptime", "unit": "s"},
    "loadavg": {"name": "Load Average", "unit": ""},
}


class ProxmoxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Proxmox Sensors."""

    VERSION = 3

    def __init__(self):
        self._host = None
        self._user = None
        self._token_id = None
        self._token_secret = None
        self._node = None
        self._server_type = None

        self._client = None

        # Discovered data
        self._hardware_sensors = None
        self._disks = None
        self._vms = None
        self._cts = None
        self._datastores = None

        # User selections
        self._features = {}
        self._selected_hardware = None
        self._selected_node_sensors = None
        self._selected_disks = None
        self._vm_mode = None
        self._selected_vms = None
        self._ct_mode = None
        self._selected_cts = None
        self._selected_datastores = None

    # ---------------------------------------------------------
    # STEP 1 — USER SETUP
    # ---------------------------------------------------------
    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            self._host = user_input[CONF_HOST]
            self._user = user_input[CONF_USER]
            self._token_id = user_input[CONF_TOKEN_ID]
            self._token_secret = user_input[CONF_TOKEN_SECRET]
            self._node = user_input[CONF_NODE]
            self._server_type = user_input[CONF_PLATFORM_TYPE]

            try:
                self._client = ProxmoxClient(
                    host=self._host,
                    user=self._user,
                    token_id=self._token_id,
                    token_secret=self._token_secret,
                    server_type=self._server_type,
                )

                # Discover hardware sensors
                self._hardware_sensors = await self._client.get_sensors(self._node)

                # Discover disks
                self._disks = await self._client.get_disks(self._node)

                # Discover VMs
                self._vms = await self._client.get_vms(self._node)

                # Discover containers
                self._cts = await self._client.get_containers(self._node)

                # Discover PBS datastores
                if self._server_type == "PBS":
                    self._datastores = await self._client.get_pbs_datastores()
                else:
                    self._datastores = []

                return await self.async_step_select_features()

            except Exception as err:
                if "auth_failed" in str(err):
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USER): str,
                vol.Required(CONF_TOKEN_ID): str,
                vol.Required(CONF_TOKEN_SECRET): str,
                vol.Required(CONF_NODE): str,
                vol.Required(CONF_PLATFORM_TYPE, default="PVE"): vol.In(SERVER_TYPES),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    # ---------------------------------------------------------
    # STEP 2 — SELECT FEATURES
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

        return self.async_show_form(
            step_id="select_features",
            data_schema=schema,
        )

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

        options = {
            s["id"]: f"{s['name']} ({s['value']}{s['unit']})"
            for s in self._hardware_sensors
        }

        schema = vol.Schema(
            {vol.Required("hardware_sensors"): vol.MultipleChoice(options)}
        )

        return self.async_show_form(
            step_id="select_hardware_sensors",
            data_schema=schema,
        )

    # ---------------------------------------------------------
    # NODE SENSORS
    # ---------------------------------------------------------
    async def async_step_select_node_sensors(self, user_input=None):
        if user_input is not None:
            self._selected_node_sensors = user_input["node_sensors"]
            return await self._next_feature_step()

        options = {
            key: f"{info['name']} ({info['unit']})"
            for key, info in NODE_SENSOR_DEFINITIONS.items()
        }

        schema = vol.Schema(
            {vol.Required("node_sensors"): vol.MultipleChoice(options)}
        )

        return self.async_show_form(
            step_id="select_node_sensors",
            data_schema=schema,
        )

    # ---------------------------------------------------------
    # DISKS
    # ---------------------------------------------------------
    async def async_step_select_disks(self, user_input=None):
        if user_input is not None:
            self._selected_disks = user_input["disks"]
            return await self._next_feature_step()

        options = {
            d["id"]: f"{d['name']} ({d['usage_pct']}%)"
            for d in self._disks
        }

        schema = vol.Schema(
            {vol.Required("disks"): vol.MultipleChoice(options)}
        )

        return self.async_show_form(
            step_id="select_disks",
            data_schema=schema,
        )

    # ---------------------------------------------------------
    # VMs
    # ---------------------------------------------------------
    async def async_step_vm_mode(self, user_input=None):
        if user_input is not None:
            self._vm_mode = user_input["vm_mode"]
            if self._vm_mode == "manual":
                return await self.async_step_select_vms()
            return await self._next_feature_step()

        schema = vol.Schema(
            {vol.Required("vm_mode", default="auto"): vol.In({"auto": "Automático", "manual": "Manual"})}
        )

        return self.async_show_form(
            step_id="vm_mode",
            data_schema=schema,
        )

    async def async_step_select_vms(self, user_input=None):
        if user_input is not None:
            self._selected_vms = user_input["vms"]
            return await self._next_feature_step()

        options = {
            vm["id"]: f"{vm['name']} ({vm['status']})"
            for vm in self._vms
        }

        schema = vol.Schema(
            {vol.Required("vms"): vol.MultipleChoice(options)}
        )

        return self.async_show_form(
            step_id="select_vms",
            data_schema=schema,
        )

    # ---------------------------------------------------------
    # CONTAINERS
    # ---------------------------------------------------------
    async def async_step_ct_mode(self, user_input=None):
        if user_input is not None:
            self._ct_mode = user_input["ct_mode"]
            if self._ct_mode == "manual":
                return await self.async_step_select_containers()
            return await self._next_feature_step()

        schema = vol.Schema(
            {vol.Required("ct_mode", default="auto"): vol.In({"auto": "Automático", "manual": "Manual"})}
        )

        return self.async_show_form(
            step_id="ct_mode",
            data_schema=schema,
        )

    async def async_step_select_containers(self, user_input=None):
        if user_input is not None:
            self._selected_cts = user_input["cts"]
            return await self._next_feature_step()

        options = {
            ct["id"]: f"{ct['name']} ({ct['status']})"
            for ct in self._cts
        }

        schema = vol.Schema(
            {vol.Required("cts"): vol.MultipleChoice(options)}
        )

        return self.async_show_form(
            step_id="select_containers",
            data_schema=schema,
        )

    # ---------------------------------------------------------
    # PBS DATASTORES
    # ---------------------------------------------------------
    async def async_step_select_datastores(self, user_input=None):
        if user_input is not None:
            self._selected_datastores = user_input["datastores"]
            return await self._finish()

        options = {store: store for store in self._datastores}

        schema = vol.Schema(
            {vol.Required("datastores"): vol.MultipleChoice(options)}
        )

        return self.async_show_form(
            step_id="select_datastores",
            data_schema=schema,
        )

    # ---------------------------------------------------------
    # FINAL STEP
    # ---------------------------------------------------------
    async def _finish(self):
        """Create final config entry."""

        data = {
            CONF_HOST: self._host,
            CONF_USER: self._user,
            CONF_TOKEN_ID: self._token_id,
            CONF_TOKEN_SECRET: self._token_secret,
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
