# ============================================================
#  CONFIG FLOW — PROXMOX SENSORS EXTENDED
# ============================================================

from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .api import ProxmoxClient
from .const import (
    DOMAIN, CONF_HOST, CONF_USER, CONF_PASSWORD,
    CONF_TOKEN_ID, CONF_TOKEN_SECRET, CONF_NODE, CONF_PLATFORM_TYPE,
)

_LOGGER = logging.getLogger(__name__)

# ------------------------------------------------------------
#  SERVER TYPES AVAILABLE IN THE INTEGRATION
# ------------------------------------------------------------
SERVER_TYPES = {
    "PVE": "Proxmox VE",
    "PBS": "Proxmox Backup Server"
}


# ============================================================
#  MAIN CONFIG FLOW CLASS
# ============================================================
class ProxmoxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the configuration flow for Proxmox Sensors."""

    VERSION = 1

    # --------------------------------------------------------
    #  INITIALIZATION
    # --------------------------------------------------------
    def __init__(self):
        self._config = {}
        self._use_token = False


    # ========================================================
    #  STEP 1 — USER INPUT (HOST + SERVER TYPE)
    # ========================================================
    async def async_step_user(self, user_input=None) -> FlowResult:
        """Step 1: Select host and server type."""

        if user_input is not None:
            self._config.update(user_input)
            return await self.async_step_auth_method()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PLATFORM_TYPE, default="PVE"): vol.In(SERVER_TYPES),
            })
        )


    # ========================================================
    #  STEP 2 — AUTH METHOD (PASSWORD OR TOKEN)
    # ========================================================
    async def async_step_auth_method(self, user_input=None) -> FlowResult:
        """Step 2: Choose between password or token."""

        if user_input is not None:
            self._use_token = user_input.get("use_token", False)
            return await self.async_step_credentials()

        return self.async_show_form(
            step_id="auth_method",
            data_schema=vol.Schema({
                vol.Required("use_token", default=False): bool
            })
        )


    # ========================================================
    #  STEP 3 — CREDENTIALS (USER + TOKEN/PASSWORD)
    #            + NODE SELECTION (ONLY PVE)
    # ========================================================
    async def async_step_credentials(self, user_input=None) -> FlowResult:
        """Step 3: Enter credentials and node (if PVE)."""

        if user_input is not None:
            self._config.update(user_input)

            # Si PVE
            if self._config[CONF_PLATFORM_TYPE] == "PVE":
                return await self.async_step_select_resources()

            # Si PBS
            return await self._finish()

        # ---------- Build dynamic schema ----------
        schema_dict = {vol.Required(CONF_USER): str}

        if self._use_token:
            schema_dict[vol.Required(CONF_TOKEN_ID)] = str
            schema_dict[vol.Required(CONF_TOKEN_SECRET)] = str
        else:
            schema_dict[vol.Required(CONF_PASSWORD)] = str

        # Node PVE
        if self._config[CONF_PLATFORM_TYPE] == "PVE":
            schema_dict[vol.Required(CONF_NODE)] = str

        # Options
        schema_dict[vol.Optional("enable_lm_sensors", default=True)] = bool
        schema_dict[vol.Optional("install_dashboard", default=False)] = bool

        return self.async_show_form(
            step_id="credentials",
            data_schema=vol.Schema(schema_dict)
        )


    # ========================================================
    #  STEP 4 — SELECT RESOURCES (ONLY FOR PVE)
    # ========================================================
    async def async_step_select_resources(self, user_input=None) -> FlowResult:
        """Step 4: Select resources (Only for PVE)."""

        if user_input is not None:
            # Save User Options
            self._config["selected_vms"] = user_input.get("vms", [])
            self._config["selected_cts"] = user_input.get("cts", [])
            self._config["selected_storage"] = user_input.get("storage", [])
            self._config["enable_physical_disks"] = user_input.get("enable_physical_disks", True)
            return await self._finish()

        # ---------- Fetch resources from PVE ----------
        client = ProxmoxClient(
            host=self._config[CONF_HOST],
            user=self._config[CONF_USER],
            password=self._config.get(CONF_PASSWORD),
            token_id=self._config.get(CONF_TOKEN_ID),
            token_secret=self._config.get(CONF_TOKEN_SECRET),
            server_type=self._config[CONF_PLATFORM_TYPE],
            verify_ssl=False
        )

        node = self._config[CONF_NODE]

        try:
            vms_data = await client.get_vms(self.hass, node) or []
            cts_data = await client.get_containers(self.hass, node) or []
            storage_data = await client.get_storages(self.hass, node) or []

            # ---------- Build selection lists ----------
            vm_options = {
                str(v["vmid"]): f"{v['vmid']} ({v.get('name', 'VM')})"
                for v in vms_data if "vmid" in v
            }
            ct_options = {
                str(c["vmid"]): f"{c['vmid']} ({c.get('name', 'CT')})"
                for c in cts_data if "vmid" in c
            }
            st_options = {
                str(s["storage"]): s["storage"]
                for s in storage_data if "storage" in s
            }

            return self.async_show_form(
                step_id="select_resources",
                data_schema=vol.Schema({
                    vol.Optional("vms", default=list(vm_options.keys())): cv.multi_select(vm_options),
                    vol.Optional("cts", default=list(ct_options.keys())): cv.multi_select(ct_options),
                    vol.Optional("storage", default=list(st_options.keys())): cv.multi_select(st_options),
                    vol.Optional("enable_physical_disks", default=True): bool,
                })
            )

        except Exception as e:
            _LOGGER.error("Error fetching resources: %s", e)
            return await self._finish()


    # ========================================================
    #  FINAL STEP — CREATE ENTRY
    # ========================================================
    async def _finish(self):
        """Finalize the configuration entry."""

        # PBS asign node
        if CONF_NODE not in self._config:
            self._config[CONF_NODE] = "Proxmox"

        # ----------------------------------------------------
        # PBS: generate unique server_id (pbs_1, pbs_2, ...)
        # ----------------------------------------------------
        if self._config.get(CONF_PLATFORM_TYPE) == "PBS":
            entries = self.hass.config_entries.async_entries(DOMAIN)
            pbs_entries = [e for e in entries if e.data.get(CONF_PLATFORM_TYPE) == "PBS"]
            self._config["server_id"] = f"pbs_{len(pbs_entries) + 1}"

        # ----------------------------------------------------
        # PVE keeps using the node as server_id
        # ----------------------------------------------------
        else:
            self._config["server_id"] = self._config[CONF_NODE]

        title_name = self._config.get(CONF_NODE)
        server_type = self._config.get(CONF_PLATFORM_TYPE, "Server")

        return self.async_create_entry(
            title=f"{server_type}: {title_name}",
            data=self._config,
        )





    # ========================================================
    #  OPTIONS FLOW HANDLER
    # ========================================================
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        from .options_flow import ProxmoxOptionsFlow
        return ProxmoxOptionsFlow()
