import aiohttp


class ProxmoxClient:
    """Async client for Proxmox PVE/PBS using user + password."""

    def __init__(self, host, user, password, server_type="PVE", verify_ssl=False):
        self.host = host
        self.user = user
        self.password = password
        self.server_type = server_type  # "PVE" or "PBS"
        self.verify_ssl = verify_ssl

        port = 8006 if server_type == "PVE" else 8007
        self.base = f"https://{host}:{port}/api2/json"

        self.session = None
        self.ticket = None
        self.csrf = None

    # ---------------------------------------------------------
    # SESSION & AUTH
    # ---------------------------------------------------------
    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def login(self):
        """Authenticate and store ticket + CSRF token."""
        await self._ensure_session()

        url = f"{self.base}/access/ticket"
        payload = {
            "username": self.user,
            "password": self.password,
        }

        async with self.session.post(url, data=payload, ssl=self.verify_ssl) as resp:
            if resp.status == 401:
                raise Exception("auth_failed")
            if resp.status != 200:
                raise Exception(f"login_error_{resp.status}")

            data = await resp.json()
            data = data["data"]

            self.ticket = data["ticket"]
            self.csrf = data.get("CSRFPreventionToken")

    async def _request(self, method, path):
        """Internal helper for authenticated requests."""
        await self._ensure_session()

        if not self.ticket:
            await self.login()

        headers = {
            "Cookie": f"PVEAuthCookie={self.ticket}",
        }

        if self.csrf:
            headers["CSRFPreventionToken"] = self.csrf

        url = f"{self.base}{path}"

        async with self.session.request(
            method, url, headers=headers, ssl=self.verify_ssl
        ) as resp:

            if resp.status == 401:
                # Ticket expired → reauth
                self.ticket = None
                await self.login()
                return await self._request(method, path)

            if resp.status != 200:
                raise Exception(f"api_error_{resp.status}")

            data = await resp.json()
            return data["data"]

    # ---------------------------------------------------------
    # HARDWARE SENSORS (PVE & PBS)
    # ---------------------------------------------------------
    async def get_sensors(self, node):
        """Return hardware sensors from Proxmox."""
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
    # NODE STATUS (CPU, RAM, uptime, load…)
    # ---------------------------------------------------------
    async def get_node_status(self, node):
        """Return normalized node status."""
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
    # DISKS (capacity, usage, wear-level, SMART)
    # ---------------------------------------------------------
    async def get_disks(self, node):
        """Return list of disks with usage and health."""
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
    # VIRTUAL MACHINES (CPU, RAM, status)
    # ---------------------------------------------------------
    async def get_vms(self, node):
        """Return list of VMs with basic info."""
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
    # CONTAINERS (CPU, RAM, status)
    # ---------------------------------------------------------
    async def get_containers(self, node):
        """Return list of LXC containers."""
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
        """Return list of PBS datastores."""
        stores = await self._request("GET", "/admin/datastore")

        return [s["store"] for s in stores]

    async def get_pbs_datastore_status(self, store):
        """Return status of a PBS datastore."""
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
        """Return last PBS tasks."""
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
