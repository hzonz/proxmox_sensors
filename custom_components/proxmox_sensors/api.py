# ============================================================
#  API — PROXMOX SENSORS EXTENDED
# ============================================================

from typing import Any, Optional
import logging
import requests
import urllib3
from proxmoxer import ProxmoxAPI

# Disable SSL warnings when certificate verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = logging.getLogger(__name__)


class ProxmoxClient:
    """
    Unified API client for both Proxmox VE (PVE) and Proxmox Backup Server (PBS).

    - PVE uses the official proxmoxer library.
    - PBS uses a lightweight HTTP client to support restricted tokens
      on hosted PBS providers (e.g., Tuxis).
    """

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

    # ============================================================
    #  PVE CLIENT INITIALIZATION
    # ============================================================

    def _build_client_sync(self):
        """Initialize the proxmoxer client for PVE."""
        if self._server_type == "PBS":
            return

        port = self._port or 8006
        timeout_val = 30

        try:
            if self._token_id and self._token_secret:
                self._proxmox = ProxmoxAPI(
                    self._host,
                    user=self._user,
                    token_name=self._token_id,
                    token_value=self._token_secret,
                    verify_ssl=self._verify_ssl,
                    port=port,
                    timeout=timeout_val,
                )
            else:
                self._proxmox = ProxmoxAPI(
                    self._host,
                    user=self._user,
                    password=self._password,
                    verify_ssl=self._verify_ssl,
                    port=port,
                    timeout=timeout_val,
                )
        except Exception as err:
            LOGGER.error("Failed to initialize Proxmoxer client on %s: %s", self._host, err)
            self._proxmox = None

    async def get_api_client(self, hass):
        """Return the PVE API client, initializing it if needed."""
        if self._server_type == "PBS":
            return None

        if self._proxmox is None:
            await hass.async_add_executor_job(self._build_client_sync)

        return self._proxmox

    # ============================================================
    #  GENERIC GET/POST WRAPPERS
    # ============================================================

    async def get(self, hass, path: str) -> Any:
        """Unified GET request for both PVE and PBS."""
        if self._server_type == "PBS":
            return await hass.async_add_executor_job(self._pbs_request, "GET", path, None)

        proxmox = await self.get_api_client(hass)
        if proxmox is None:
            return None

        try:
            return await hass.async_add_executor_job(proxmox.get, path)
        except Exception as err:
            LOGGER.error("PVE GET error on %s: %s", path, err)
            return None

    async def post(self, hass, path: str, data=None) -> Any:
        """Unified POST request for PVE."""
        proxmox = await self.get_api_client(hass)
        if proxmox is None:
            return None

        def _do_post():
            return proxmox.post(path, **(data or {}))

        try:
            return await hass.async_add_executor_job(_do_post)
        except Exception as err:
            LOGGER.error("PVE POST error on %s: %s", path, err)
            return None


    # ============================================================
    #  PVE METHODS
    # ============================================================

    async def get_cluster_tasks(self, hass):
        """Return recent cluster tasks."""
        return await self.get(hass, "cluster/tasks") or []

    async def get_node_status(self, hass, node: str):
        """Return general node status."""
        return await self.get(hass, f"nodes/{node}/status")

    async def get_node_network(self, hass, node: str):
        """Return node network interfaces (para TX/RX)."""
        return await self.get(hass, f"nodes/{node}/network") or []

    async def get_vms(self, hass, node: str):
        """Return all VMs in a node."""
        return await self.get(hass, f"nodes/{node}/qemu") or []

    async def get_containers(self, hass, node: str):
        """Return all LXC containers in a node."""
        return await self.get(hass, f"nodes/{node}/lxc") or []

    async def get_container_status(self, hass, node: str, vmid: str):
        """Return detailed container status."""
        return await self.get(hass, f"nodes/{node}/lxc/{vmid}/status/current")

    async def get_qemu_status(self, hass, node: str, vmid: str):
        """Return detailed QEMU VM status."""
        return await self.get(hass, f"nodes/{node}/qemu/{vmid}/status/current")

    async def get_lxc_status(self, hass, node: str, vmid: str):
        """Return detailed LXC container status."""
        return await self.get(hass, f"nodes/{node}/lxc/{vmid}/status/current")

    async def get_vm_type(self, hass, node: str, vmid: str) -> str:
        """Return 'qemu' or 'lxc' depending on VM type."""
        vms = await self.get_vms(hass, node)
        if isinstance(vms, list):
            for vm in vms:
                if str(vm.get("vmid")) == str(vmid):
                    return "qemu"

        containers = await self.get_containers(hass, node)
        if isinstance(containers, list):
            for ct in containers:
                if str(ct.get("vmid")) == str(vmid):
                    return "lxc"

        return "unknown"

    async def get_vm_status(self, hass, node: str, vmid: str):
        """Return VM or CT status, auto-detecting type."""
        vmtype = await self.get_vm_type(hass, node, vmid)
        if vmtype == "qemu":
            return await self.get_qemu_status(hass, node, vmid)
        if vmtype == "lxc":
            return await self.get_lxc_status(hass, node, vmid)
        return None

    async def get_storages(self, hass, node: str):
        """Return storage resources."""
        return await self.get(hass, f"nodes/{node}/storage") or []

    async def get_disks(self, hass, node: str):
        """Return physical disks."""
        return await self.get(hass, f"nodes/{node}/disks/list") or []

    async def control_container(self, hass, node: str, vmid: str, command: str):
        """Send start/stop/reboot/shutdown to a container."""
        return await self.post(hass, f"nodes/{node}/lxc/{vmid}/status/{command}")

    async def control_vm(self, hass, node: str, vmid: str, command: str):
        """Send commands to a QEMU virtual machine.
        
        Supported commands: start, stop, shutdown, reboot, reset, 
                           pause, resume, hibernate
        """
        LOGGER.info(f"Sending {command} command to VM {vmid} on node {node}")
        
        
        if command == 'hibernate':
            path = f"nodes/{node}/qemu/{vmid}/status/suspend"
            data = {'todisk': 1}
        else:
            path = f"nodes/{node}/qemu/{vmid}/status/{command}"
            data = {}
        
        if command in ['shutdown', 'reboot']:
            data['timeout'] = 60
        
        result = await self.post(hass, path, data)
        
        if result:
            LOGGER.info(f"Comando {command} enviado exitosamente a VM {vmid}")
        else:
            LOGGER.error(f"Error al enviar comando {command} a VM {vmid}")
        
        return result

    async def get_lm_sensors_http(self, hass, node: str):
        """Fetch temperature and fan data from an external sensor script."""
        url = f"http://{self._host}:9000/sensors"

        def _fetch():
            try:
                r = requests.get(url, timeout=5)
                r.raise_for_status()
                return r.json()
            except Exception:
                return {}

        return await hass.async_add_executor_job(_fetch)
        
    async def start_vzdump(self, hass, node: str, vmid: str, storage: str, notes: str = None):
        """Send backup from Home Assistant."""
        if not node or not vmid or not storage:
            raise ValueError("node, vmid, and storage are required to start a backup")

        path = f"nodes/{node}/vzdump"
        
        # Optimized parameters for PBS:
        # - snapshot: allows backups without shutting down the VM.
        # - zstd: fast and efficient compression.
        data = {
            "vmid": vmid,
            "storage": storage,
            "mode": "snapshot",
            "compress": "zstd"
        }

        if notes:
            data["notes-template"] = notes
        
        LOGGER.debug("Sending vzdump order to PVE with notes: %s", data)

        result = await self.post(hass, path, data)

        if result:
            LOGGER.info("vzdump successfully launched with notes: %s", result)
        else:
            LOGGER.warning("vzdump did not return a response (possible error or permissions)")

        return result

    # ============================================================
    #  PBS LOW-LEVEL REQUEST + WRAPPERS
    # ============================================================

    def _pbs_request(self, method: str, path: str, data=None):
        """
        Lightweight PBS API request handler.

        Designed to work even with restricted token permissions
        (e.g., hosted PBS providers such as Tuxis).
        """
        port = self._port or 8007

        # Normalize host (remove protocol and any existing port)
        clean_host = (
            self._host.replace("https://", "")
            .replace("http://", "")
            .split("/")[0]
            .split(":")[0]
        )
        url = f"https://{clean_host}:{port}/api2/json/{path}"

        # Build token identifier: user@realm!tokenid
        if not self._user or not self._token_secret:
            LOGGER.error("PBS token authentication requires user and token_secret")
            return None

        if self._token_id:
            if "!" in self._token_id:
                token_full = self._token_id
            else:
                token_full = f"{self._user}!{self._token_id}"
        else:
            LOGGER.error("PBS token_id is missing")
            return None

        auth_header = f"PBSAPIToken {token_full}:{self._token_secret}"
        headers = {"Authorization": auth_header, "Accept": "application/json"}

        try:
            if method == "GET":
                r = requests.get(url, headers=headers, verify=self._verify_ssl, timeout=15)
            else:
                r = requests.post(url, headers=headers, json=(data or {}), verify=self._verify_ssl, timeout=15)

            if r.status_code == 403:
                LOGGER.debug("PBS request forbidden on path %s (403)", path)
                return None

            if r.status_code >= 400:
                LOGGER.error("PBS HTTP %s on %s: %s", r.status_code, path, r.text)
                return None

            return r.json().get("data")

        except Exception as err:
            LOGGER.debug("PBS path %s unreachable: %s", path, err)
            return None

    async def pbs_get(self, hass, path: str) -> Any:
        """Explicit GET wrapper for PBS endpoints."""
        return await hass.async_add_executor_job(self._pbs_request, "GET", path, None)

    async def pbs_post(self, hass, path: str, data=None) -> Any:
        """Explicit POST wrapper for PBS endpoints."""
        return await hass.async_add_executor_job(self._pbs_request, "POST", path, data or {})

    # ============================================================
    #  PBS HIGH-LEVEL METHODS
    # ============================================================

    async def get_pbs_datastores(self, hass):
        """Return all PBS datastores."""
        data = await self.pbs_get(hass, "admin/datastore")
        return [d["store"] for d in data if isinstance(d, dict) and "store" in d] if data else []

    async def get_pbs_datastore_status(self, hass, store: str):
        """Return datastore status."""
        return await self.pbs_get(hass, f"admin/datastore/{store}/status") or {}

    async def get_pbs_datastore_usage(self, hass, store: str):
        """Return GC usage information."""
        return await self.pbs_get(hass, f"admin/datastore/{store}/gc") or {}

    async def get_pbs_tasks(self, hass):
        """Return recent PBS tasks."""
        return await self.pbs_get(hass, "nodes/localhost/tasks") or []

    async def get_pbs_version(self, hass):
        """Return PBS version information."""
        return await self.pbs_get(hass, "version") or {}

    async def get_pbs_backup_list(self, hass, store: str):
        """Return all backups inside a datastore."""
        return await self.pbs_get(hass, f"admin/datastore/{store}/snapshots") or []

    async def get_pbs_node_status(self, hass):
        """Return PBS node hardware status (CPU, RAM, etc.)."""
        return await self.pbs_get(hass, "nodes/localhost/status") or {}

    async def get_pbs_gc(self, hass, store: str):
        """Return GC info for a specific datastore."""
        return await self.pbs_get(hass, f"admin/datastore/{store}/gc") or {}

    async def get_pbs_snapshots(self, hass, store: str):
        """Return snapshots for a specific datastore."""
        return await self.pbs_get(hass, f"admin/datastore/{store}/snapshots") or []