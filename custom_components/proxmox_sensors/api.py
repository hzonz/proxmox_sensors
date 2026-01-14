import aiohttp


class ProxmoxClient:
    """Async client for Proxmox PVE/PBS using API Token authentication."""

    def __init__(self, host, user, token_id, token_secret, server_type="PVE", verify_ssl=False):
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
            # SSL DESACTIVADO CORRECTAMENTE
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
            )

    # ---------------------------------------------------------
    # REQUEST (TOKEN AUTH)
    # ---------------------------------------------------------
    async def _request(self, method, path):
        """Internal helper for authenticated requests using API Token."""
        await self._ensure_session()

        headers = {
            "Authorization": f"PVEAPIToken={self.user}!{self.token_id}={self.token_secret}"
        }

        url = f"{self.base}{path}"

        async with self.session.request(
            method, url, headers=headers
        ) as resp:

            if resp.status == 401:
                raise Exception("auth_failed")

            if resp.status != 200:
                raise Exception(f"api_error_{resp.status}")

            data = await resp.json()
            return data["data"]

    # ---------------------------------------------------------
    # HARDWARE SENSORS
    # ---------------------------------------------------------
    async def get_sensors(self, node):
        sensors = await self._request("GET", f"/nodes/{node}/hardware/sensors")

        normalized = []
        for s in sensors:
            normalized.append({
                "id": s.get("id"),
                "name": s.get("name", s.get("id")),
                "value": s.get("value"),
                "unit": s.get("unit", ""),
            })

        return normalized

    # ---------------------------------------------------------
    # NODE STATUS
    # ---------------------------------------------------------
    async def get_node_status(self, node):
        data = await self._request("GET", f"/nodes/{node}/status")

        cpu_pct = round(data["cpu"] * 100, 2) if "cpu" in data else None
        ram_used = data.get("mem")
        ram_total = data.get("maxmem")
        ram_pct = round((ram_used / ram_total) * 100, 2) if ram_total else None

        return {
            "cpu_usage_pct": cpu_pct,
            "ram_usage_pct": ram_pct,
            "ram_used": ram_used,
            "ram_total": ram_total,
            "uptime": data.get("uptime"),
            "loadavg": data.get("loadavg"),
        }

    # ---------------------------------------------------------
    # DISKS
    # ---------------------------------------------------------
    async def get_disks(self, node):
        disks = await self._request("GET", f"/nodes/{node}/disks/list")

        normalized = []
        for d in disks:
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
    # VIRTUAL MACHINES
    # ---------------------------------------------------------
    async def get_vms(self, node):
        vms = await self._request("GET", f"/nodes/{node}/qemu")

        normalized = []
        for vm in vms:
            vmid = vm["vmid"]
            status = await self._request("GET", f"/nodes/{node}/qemu/{vmid}/status/current")

            cpu_pct = round(status["cpu"] * 100, 2) if "cpu" in status else None
            mem_used = status.get("mem")
            mem_total = status.get("maxmem")
            mem_pct = round((mem_used / mem_total) * 100, 2) if mem_total else None

            normalized.append({
                "id": f"vm_{vmid}",
                "vmid": vmid,
                "name": vm.get("name", f"VM {vmid}"),
                "status": status.get("status"),
                "cpu_pct": cpu_pct,
                "mem_pct": mem_pct,
            })

        return normalized

    # ---------------------------------------------------------
    # CONTAINERS
    # ---------------------------------------------------------
    async def get_containers(self, node):
        cts = await self._request("GET", f"/nodes/{node}/lxc")

        normalized = []
        for ct in cts:
            vmid = ct["vmid"]
            status = await self._request("GET", f"/nodes/{node}/lxc/{vmid}/status/current")

            cpu_pct = round(status["cpu"] * 100, 2) if "cpu" in status else None
            mem_used = status.get("mem")
            mem_total = status.get("maxmem")
            mem_pct = round((mem_used / mem_total) * 100, 2) if mem_total else None

            normalized.append({
                "id": f"ct_{vmid}",
                "vmid": vmid,
                "name": ct.get("name", f"CT {vmid}"),
                "status": status.get("status"),
                "cpu_pct": cpu_pct,
                "mem_pct": mem_pct,
            })

        return normalized

    # ---------------------------------------------------------
    # PBS DATASTORES
    # ---------------------------------------------------------
    async def get_pbs_datastores(self):
        stores = await self._request("GET", "/admin/datastore")
        return [s["store"] for s in stores]

    async def get_pbs_datastore_status(self, store):
        data = await self._request("GET", f"/admin/datastore/{store}/status")

        size = data.get("total")
        used = data.get("used")
        pct = round((used / size) * 100, 2) if size else None

        return {
            "id": f"pbs_store_{store}",
            "store": store,
            "total": size,
            "used": used,
            "free": data.get("avail"),
            "usage_pct": pct,
            "backup_count": data.get("backup-count"),
            "gc_status": data.get("gc-status"),
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


