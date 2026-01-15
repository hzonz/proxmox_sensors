from typing import Any, List, Dict, Optional
import logging
import subprocess
import re

from proxmoxer import ProxmoxAPI
from requests.exceptions import ConnectTimeout
from proxmoxer.core import ResourceException

LOGGER = logging.getLogger(__name__)


class ProxmoxClient:
    """Async-safe wrapper around proxmoxer ProxmoxAPI for PVE and PBS."""

    def __init__(
        self,
        host: str,
        user: str,
        password: Optional[str] = None,
        token_id: Optional[str] = None,
        token_secret: Optional[str] = None,
        server_type: str = "PVE",
        port: Optional[int] = None,
        verify_ssl: bool = True,
    ):
        self._host = host
        self._user = user
        self._password = password
        self._token_id = token_id
        self._token_secret = token_secret
        self._server_type = server_type
        self._port = port
        self._verify_ssl = verify_ssl

        self._proxmox: Optional[ProxmoxAPI] = None

    # ------------------------------
    # CLIENT INITIALIZATION (SYNC)
    # ------------------------------
    def _build_client_sync(self):
        port = self._port
        if self._server_type == "PVE":
            port = port or 8006
        elif self._server_type == "PBS":
            port = port or 8007
        else:
            raise ValueError(f"Unsupported server type: {self._server_type}")

        if self._token_id and self._token_secret:
            LOGGER.debug("Building ProxmoxAPI client with token for user %s", self._user)
            self._proxmox = ProxmoxAPI(
                self._host,
                user=self._user,
                token_name=self._token_id,
                token_value=self._token_secret,
                verify_ssl=self._verify_ssl,
                port=port,
                timeout=30,
            )
        else:
            LOGGER.debug("Building ProxmoxAPI client with password for user %s", self._user)
            self._proxmox = ProxmoxAPI(
                self._host,
                user=self._user,
                password=self._password,
                verify_ssl=self._verify_ssl,
                port=port,
                timeout=30,
            )

    async def get_api_client(self, hass):
        if self._proxmox is None:
            await hass.async_add_executor_job(self._build_client_sync)
        return self._proxmox

    # ------------------------------
    # GENERIC API HELPERS
    # ------------------------------
    async def get(self, hass, path: str) -> Any:
        proxmox = await self.get_api_client(hass)
        try:
            result = await hass.async_add_executor_job(proxmox.get, path)
            LOGGER.debug("GET %s -> %s", path, result)
            return result
        except (ResourceException, ConnectTimeout) as err:
            LOGGER.error("Proxmox GET error %s: %s", path, err)
            raise

    async def post(self, hass, path: str, data: Optional[dict] = None) -> Any:
        proxmox = await self.get_api_client(hass)
        try:
            result = await hass.async_add_executor_job(proxmox.post, path, data or {})
            LOGGER.debug("POST %s -> %s", path, result)
            return result
        except (ResourceException, ConnectTimeout) as err:
            LOGGER.error("Proxmox POST error %s: %s", path, err)
            raise

    # ------------------------------
    # LOCAL TEMPERATURES (lm-sensors)
    # ------------------------------
    async def get_local_temperatures(self) -> Dict[str, float]:
        """Parse output of `sensors` command."""
        try:
            output = subprocess.check_output(["sensors"], text=True)
        except Exception as err:
            LOGGER.error("Error running sensors: %s", err)
            return {}

        temps = {}
        regex = re.compile(r"(.+?):\s+\+?([0-9]+\.[0-9]+)°C")

        for line in output.splitlines():
            match = regex.search(line)
            if match:
                name = match.group(1).strip().replace(" ", "_").lower()
                value = float(match.group(2))
                temps[name] = value

        LOGGER.debug("Local temperatures parsed: %s", temps)
        return temps

    # ------------------------------
    # PVE METHODS
    # ------------------------------
    async def get_sensors(self, hass, node: str) -> List[Dict[str, Any]]:
        status = await self.get(hass, f"nodes/{node}/status")
        return [
            {"id": "cpu", "name": "CPU Usage", "value": status.get("cpu"), "unit": "%"},
            {"id": "mem", "name": "Memory Usage", "value": status.get("mem"), "unit": "%"},
            {"id": "uptime", "name": "Uptime", "value": status.get("uptime"), "unit": "s"},
        ]

    async def get_node_status(self, hass, node: str) -> Dict[str, Any]:
        return await self.get(hass, f"nodes/{node}/status")

    async def get_disks(self, hass, node: str) -> List[Dict[str, Any]]:
        return await self.get(hass, f"nodes/{node}/disks/list")

    async def get_vms(self, hass, node: str) -> List[Dict[str, Any]]:
        return await self.get(hass, f"nodes/{node}/qemu")

    async def get_containers(self, hass, node: str) -> List[Dict[str, Any]]:
        return await self.get(hass, f"nodes/{node}/lxc")

    # ------------------------------
    # PBS METHODS
    # ------------------------------
    async def get_pbs_datastores(self, hass) -> List[str]:
        if self._server_type != "PBS":
            return []
        storage = await self.get(hass, "storage")
        return [d["store"] for d in storage if "store" in d]

    async def get_pbs_datastore_status(self, hass, store: str) -> Dict[str, Any]:
        if self._server_type != "PBS":
            return {}
        return await self.get(hass, f"storage/{store}/status")

    async def get_pbs_tasks(self, hass) -> Dict[str, Any]:
        if self._server_type != "PBS":
            return {}
        tasks = await self.get(hass, "tasks")
        return tasks[-1] if tasks else {}
