# ============================================================
#  OPTIONS FLOW — PROXMOX SENSORS EXTENDED
# ============================================================

from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN, CONF_HOST, CONF_USER, CONF_PASSWORD,
    CONF_TOKEN_ID, CONF_TOKEN_SECRET, CONF_NODE, CONF_PLATFORM_TYPE
)
from .api import ProxmoxClient


class ProxmoxOptionsFlow(config_entries.OptionsFlow):
    """Handle the options flow for Proxmox Sensors."""

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Main entry point for the options flow."""

        conf = self.config_entry.data
        server_type = conf.get(CONF_PLATFORM_TYPE, "PVE")

        # ============================================================
        #  SAVE OPTIONS
        # ============================================================
        if user_input is not None:

            new_data = dict(self.config_entry.data)

            if server_type == "PVE":
                new_data.update({
                    "enable_lm_sensors": user_input.get("enable_lm_sensors"),
                    "enable_physical_disks": user_input.get("enable_physical_disks"),
                    "selected_vms": user_input.get("vms", []),
                    "selected_cts": user_input.get("cts", []),
                    "selected_storage": user_input.get("storage", []),
                })

            # PBS has no configurable options (kept for future expansion)
            self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        # ============================================================
        #  PBS — NO OPTIONS AVAILABLE
        # ============================================================
        if server_type == "PBS":
            return self.async_abort(reason="pbs_no_options")

        # ============================================================
        #  PVE — LOAD RESOURCES AND SHOW FORM
        # ============================================================
        client = ProxmoxClient(
            host=conf[CONF_HOST],
            user=conf[CONF_USER],
            password=conf.get(CONF_PASSWORD),
            token_id=conf.get(CONF_TOKEN_ID),
            token_secret=conf.get(CONF_TOKEN_SECRET),
            server_type=conf[CONF_PLATFORM_TYPE],
            verify_ssl=False,
        )

        try:
            vms_data = await client.get_vms(self.hass, conf[CONF_NODE]) or []
            cts_data = await client.get_containers(self.hass, conf[CONF_NODE]) or []
            storage_data = await client.get_storages(self.hass, conf[CONF_NODE]) or []

            vm_options = {
                str(v["vmid"]): f"{v['vmid']} ({v.get('name', 'VM')})"
                for v in vms_data
            }
            ct_options = {
                str(c["vmid"]): f"{c['vmid']} ({c.get('name', 'CT')})"
                for c in cts_data
            }
            st_options = {
                str(s["storage"]): s["storage"]
                for s in storage_data
            }

            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Optional(
                        "vms",
                        default=conf.get("selected_vms", list(vm_options.keys()))
                    ): cv.multi_select(vm_options),

                    vol.Optional(
                        "cts",
                        default=conf.get("selected_cts", list(ct_options.keys()))
                    ): cv.multi_select(ct_options),

                    vol.Optional(
                        "storage",
                        default=conf.get("selected_storage", list(st_options.keys()))
                    ): cv.multi_select(st_options),

                    vol.Optional(
                        "enable_lm_sensors",
                        default=conf.get("enable_lm_sensors", True)
                    ): bool,

                    vol.Optional(
                        "enable_physical_disks",
                        default=conf.get("enable_physical_disks", True)
                    ): bool,
                })
            )

        except Exception:
            # If resource loading fails, still allow toggling sensor options
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Optional(
                        "enable_lm_sensors",
                        default=conf.get("enable_lm_sensors", True)
                    ): bool,
                    vol.Optional(
                        "enable_physical_disks",
                        default=conf.get("enable_physical_disks", True)
                    ): bool,
                })
            )
