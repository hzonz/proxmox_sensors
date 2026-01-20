from typing import Any, List, Dict, Optional
import logging
import requests
import asyncio
import urllib3
from proxmoxer import ProxmoxAPI

# Deshabilitar advertencias de SSL si el usuario decide no verificar certificados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = logging.getLogger(__name__)

class ProxmoxClient:
    """API client for Proxmox Virtual Environment and Backup Server."""

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

    def _build_client_sync(self):
        """Build the Proxmoxer client in a synchronous context."""
        if self._server_type == "PBS":
            return
        port = self._port or 8006
        timeout_val = 30
        try:
            if self._token_id and self._token_secret:
                self._proxmox = ProxmoxAPI(
                    self._host, user=self._user, token_name=self._token_id,
                    token_value=self._token_secret, verify_ssl=self._verify_ssl,
                    port=port, timeout=timeout_val,
                )
            else:
                self._proxmox = ProxmoxAPI(
                    self._host, user=self._user, password=self._password,
                    verify_ssl=self._verify_ssl, port=port, timeout=timeout_val,
                )
        except Exception as err:
            LOGGER.error("Failed to initialize Proxmoxer client on %s: %s", self._host, err)
            self._proxmox = None

    async def get_api_client(self, hass):
        """Get or initialize the PVE API client."""
        if self._server_type == "PBS":
            return None
        if self._proxmox is None:
            await hass.async_add_executor_job(self._build_client_sync)
        return self._proxmox

    async def get(self, hass, path: str) -> Any:
        """Generic GET request for both PVE and PBS."""
        if self._server_type == "PBS":
            return await hass.async_add_executor_job(self._pbs_request, "GET", path)
        
        proxmox = await self.get_api_client(hass)
        if proxmox is None: return None
        try:
            return await hass.async_add_executor_job(proxmox.get, path)
        except Exception as err:
            LOGGER.error("PVE GET error on %s: %s", path, err)
            return None

    async def post(self, hass, path: str, data=None) -> Any:
        """Generic POST request for PVE commands."""
        proxmox = await self.get_api_client(hass)
        if proxmox is None: return None
        try:
            return await hass.async_add_executor_job(proxmox.post, path, **(data or {}))
        except Exception as err:
            LOGGER.error("PVE POST error on %s: %s", path, err)
            return None

    # =========================================================
    # PVE METHODS (Virtual Environment)
    # =========================================================
    
    async def get_cluster_tasks(self, hass):
        """Get recent tasks from the entire cluster (useful for backup monitoring)."""
        # Returns the last 50 tasks of the datacenter
        return await self.get(hass, "cluster/tasks") or []

    async def get_node_status(self, hass, node: str):
        """Get general status of a specific node."""
        return await self.get(hass, f"nodes/{node}/status")

    async def get_vms(self, hass, node: str):
        """List all Virtual Machines in a node."""
        return await self.get(hass, f"nodes/{node}/qemu") or []

    async def get_containers(self, hass, node: str):
        """List all LXC Containers in a node."""
        return await self.get(hass, f"nodes/{node}/lxc") or []

    async def get_container_status(self, hass, node: str, vmid: str):
        """Get detailed status of a specific container."""
        return await self.get(hass, f"nodes/{node}/lxc/{vmid}/status/current")

    async def get_storages(self, hass, node: str):
        """List storage resources in a node."""
        return await self.get(hass, f"nodes/{node}/storage") or []

    async def get_disks(self, hass, node: str):
        """List physical disks in a node."""
        return await self.get(hass, f"nodes/{node}/disks/list") or []

    async def control_container(self, hass, node: str, vmid: str, command: str):
        """Send start, stop, shutdown or reboot to a container."""
        path = f"nodes/{node}/lxc/{vmid}/status/{command}"
        return await self.post(hass, path)

    async def get_lm_sensors_http(self, hass, node: str):
        """Fetch temperature and fan data from the external python-sensor script."""
        url = f"http://{self._host}:9000/sensors"
        def _fetch():
            try:
                r = requests.get(url, timeout=5)
                r.raise_for_status()
                return r.json()
            except Exception:
                return {}
        return await hass.async_add_executor_job(_fetch)

    # =========================================================
    # PBS METHODS (Backup Server)
    # =========================================================
    
    def _pbs_request(self, method: str, path: str, data=None):
        """Internal helper for PBS API requests via Requests library."""
        port = self._port or 8007
        url = f"https://{self._host}:{port}/api2/json/{path}"
        
        # Build token-based authentication header
        token_part = f"!{self._token_id}" if self._token_id and "!" not in self._user else ""
        auth_header = f"PBSAPIToken {self._user}{token_part}:{self._token_secret}"
        headers = {"Authorization": auth_header, "Accept": "application/json"}
        
        try:
            if method == "GET":
                r = requests.get(url, headers=headers, verify=self._verify_ssl, timeout=15)
            else:
                r = requests.post(url, headers=headers, json=data or {}, verify=self._verify_ssl, timeout=15)
            r.raise_for_status()
            return r.json().get("data")
        except Exception as err:
            LOGGER.error("PBS communication failure [%s]: %s", path, err)
        return None

    async def get_pbs_datastores(self, hass):
        """List all available PBS datastores."""
        data = await self.get(hass, "admin/datastore")
        return [d["store"] for d in data if isinstance(d, dict) and "store" in d] if data else []

    async def get_pbs_datastore_status(self, hass, store: str):
        """Get status of a specific PBS datastore."""
        return await self.get(hass, f"admin/datastore/{store}/status") or {}

    async def get_pbs_datastore_usage(self, hass, store: str):
        """Get Garbage Collection (usage) info of a PBS datastore."""
        return await self.get(hass, f"admin/datastore/{store}/gc") or {}

    async def get_pbs_tasks(self, hass):
        """Get recent PBS tasks."""
        return await self.get(hass, "nodes/localhost/tasks") or []

    async def get_pbs_version(self, hass):
        """Get PBS version information."""
        return await self.get(hass, "version") or {}
    
    async def get_pbs_backup_list(self, hass, store: str):
        """List all backups (snapshots) inside a PBS datastore."""
        return await self.get(hass, f"admin/datastore/{store}/snapshots") or []