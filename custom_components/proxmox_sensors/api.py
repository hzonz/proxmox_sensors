import aiohttp


class ProxmoxClient:
    """Async client for Proxmox PVE/PBS using API Token authentication."""

    def __init__(
        self,
        host,
        user,
        token_id,
        token_secret,
        server_type="PVE",
        verify_ssl=False,
    ):
        self.host = host
        self.user = user
        self.token_id = token_id
        self.token_secret = token_secret
        self.server_type = server_type
        self.verify_ssl = verify_ssl

        port = 8006 if server_type == "PVE" else 8007
        self.base = f"https://{host}:{port}/api2/json"

        self.session = None

    # ---------------------------------------------------------
    # SESSION
    # ---------------------------------------------------------
    async def _ensure_session(self):
        if self.session is None:
            # SSL desactivado (certificados autofirmados)
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
            )

    # ---------------------------------------------------------
    # REQUEST (TOKEN AUTH)
    # ---------------------------------------------------------
    async def _request(self, method, path):
        """Internal helper for authenticated requests using API Token."""
        await self._ensure_session()

        # Selección automática del tipo de token
        if self.server_type == "PBS":
            auth_type = "PBSAPIToken"
        else:
            auth_type = "PVEAPIToken"

        headers = {
            "Authorization": f"{auth_type}={self.user}!{self.token_id}={self.token_secret}"
        }

        url = f"{self.base}{path}"

        async with self.session.request(method, url, headers=headers) as resp:

            if resp.status == 401:
                raise Exception("auth_failed")

            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"api_error_{resp.status}: {text}")

            data = await resp.json()
            return data.get("data")

    # ---------------------------------------------------------
    # CONNECTION TEST
    # ---------------------------------------------------------
    async def test_connection(self):
        """Simple connectivity test valid for both PVE and PBS."""
        await self._request("GET", "/version")
        return True

    # ---------------------------------------------------------
    # HARDWARE SENSORS (PVE)
    # ---------------------------------------------------------
    async def get_sensors(self, node):
        sensors = await self._request("GET", f"/nodes/{node}/hardware/sensors")

        normalized = []
        for s in sensors or []:
            normalized.append({
                "id": s.get("id"),
                "name": s.get("name", s.get("id")),
                "value": s.get("value"),
                "unit": s.get("unit", ""),
            })

        return normalized

    # ---------------------------------------------------------
    # NODE STATUS (PVE)
    # ---------------------------------------------------------
    async def get_node_status(self, node):
        data = await self._request("GET", f"/nodes/{node}/status")

        cpu_pct = round(data["cpu"] * 100, 2) if data and "cpu" in data else None
        ram_used = data.get("mem") if data else None
        ram_total = data.get("maxmem") if data else None
        ram_pct = round((ram_used / ram_total) * 100, 2) if ram_total else None

        return {
            "cpu_usage_pct": cpu_pct,
            "ram_usage_pct": ram_pct,
            "ram_used": ram_used,
            "ram_total": ram_total,
            "uptime": data.get("uptime") if data else None,
            "loadavg": data.get("loadavg") if data else None,
        }

    # ---------------------------------------------------------
    # DISKS (PVE)
    # ---------------------------------------------------------
    async def get_disks(self, node):
        disks = await self._request("GET", f"/nodes/{node}/disks/list")

        normalized = []
        for d in disks or []:
            size = d.get("size")
            used = d.get("used")
            pct = round((used / size) * 100, 2) if size else None

            normalized.append({
                "id": d.get("devpath"),
                "name": d.get("devpath"),
                "size": size,
                "used": used,
                "usage_pct": pct,
                "health": d.get("health"),
                "wearout": d.get("wearout"),
            })

        return normalized

    # ---------------------------------------------------------
    # VIRTUAL MACHINES (PVE)
    # ---------------------------------------------------------
    async def get_vms(self, node):
        vms = await self._request("GET", f"/nodes/{node}/qemu")

        normalized = []
        for vm in vms or []:
            vmid = vm["vmid"]
            status = await self._request(
                "GET",
                f"/nodes/{node}/qemu/{vmid}/status/current"
            )

            cpu_pct = round(status["cpu"] * 100, 2) if status and "cpu" in status else None
            mem_used = status.get("mem") if status else None
            mem_total = status.get("maxmem") if status else None
            mem_pct = round((mem_used / mem_total) * 100, 2) if mem_total else None

            normalized.append({
                "id": f"vm_{vmid}",
                "vmid": vmid,
                "name": vm.get("name", f"VM {vmid}"),
                "status": status.get("status") if status else None,
                "cpu_pct": cpu_pct,
                "mem_pct": mem_pct,
            })

        return normalized

    # ---------------------------------------------------------
    # CONTAINERS (PVE)
    # ---------------------------------------------------------
    async def get_containers(self, node):
        cts = await self._request("GET", f"/nodes/{node}/lxc")

        normalized = []
        for ct in cts or []:
            vmid = ct["vmid"]
            status = await self._request(
                "GET",
                f"/nodes/{node}/lxc/{vmid}/status/current"
            )

            cpu_pct = round(status["cpu"] * 100, 2) if status and "cpu" in status else None
            mem_used = status.get("mem") if status else None
            mem_total = status.get("maxmem") if status else None
            mem_pct = round((mem_used / mem_total) * 100, 2) if mem_total else None

            normalized.append({
                "id": f"ct_{vmid}",
                "vmid": vmid,
                "name": ct.get("name", f"CT {vmid}"),
                "status": status.get("status") if status else None,
                "cpu_pct": cpu_pct,
                "mem_pct": mem_pct,
            })

        return normalized

    # ---------------------------------------------------------
    # PBS DATASTORES
    # ---------------------------------------------------------
    async def get_pbs_datastores(self):
        stores = await self._request("GET", "/admin/datastore")
        return [s.get("store") for s in stores or []]

    async def get_pbs_datastore_status(self, store):
        data = await self._request("GET", f"/admin/datastore/{store}/status")

        size = data.get("total") if data else None
        used = data.get("used") if data else None
        pct = round((used / size) * 100, 2) if size else None

        return {
            "id": f"pbs_store_{store}",
            "store": store,
            "total": size,
            "used": used,
            "free": data.get("avail") if data else None,
            "usage_pct": pct,
            "backup_count": data.get("backup-count") if data else None,
            "gc_status": data.get("gc-status") if data else None,
        }

    # ---------------------------------------------------------
    # PBS TASKS
    # ---------------------------------------------------------
    async def get_pbs_tasks(self):
        tasks = await self._request("GET", "/admin/tasks")

        if not tasks:
            return None

        last = tasks[0]

        return {
            "id": "pbs_last_task",
            "upid": last.get("upid"),
            "status": last.get("status"),
            "type": last.get("type"),
            "starttime": last.get("starttime"),
            "endtime": last.get("endtime"),
        }

    # ---------------------------------------------------------
    # CLOSE SESSION
    # ---------------------------------------------------------
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
