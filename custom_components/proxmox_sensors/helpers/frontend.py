"""Handle Proxmox Frontend panel."""

import os
import json
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel
from homeassistant.components.frontend import DATA_PANELS, Panel

from ..const import (
    PANEL_REPO_VERSION_URL,
    PANEL_REPO_FILES_URL,
    PANEL_REPO_BASE_URL,
    PANEL_LOCAL_PATH,
    PANEL_STORAGE_FILE,
    DEFAULT_PANEL_VERSION,
)

from .logger import _LOGGER


async def async_download_panel_if_needed(hass: HomeAssistant) -> str:
    if hass.data.get("_proxmox_panel_updating"):
        return await read_local_version(hass)

    hass.data["_proxmox_panel_updating"] = True

    async with aiohttp.ClientSession() as session:
        try:
            remote_version = await read_remote_version(session)
            local_version = await read_local_version(hass)

            if remote_version != local_version:
                await download_panel_files(hass, session, remote_version)
                await save_local_version(hass, remote_version)

            return remote_version

        except Exception as e:
            _LOGGER.error(f"[Proxmox Panel] Error updating panel: {e}")
            return "0.0"

        finally:
            hass.data["_proxmox_panel_updating"] = False

