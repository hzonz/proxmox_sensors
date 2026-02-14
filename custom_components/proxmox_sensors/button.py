"""Button entities for Proxmox Virtual Environment (PVE) and Proxmox Backup Server (PBS)."""

import asyncio
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import device_registry as dr

from .pbs_actions import run_gc, run_prune, run_verify, run_sync
from .const import DOMAIN, CONF_NODE, CONF_PLATFORM_TYPE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up button entities."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    if data.get("server_type") == "PVE":
        client = getattr(coordinator, "client", data.get("client"))
    else:
        client = data.get("client")

    selected_vms = entry.options.get("selected_vms", entry.data.get("selected_vms", []))
    selected_cts = entry.options.get("selected_cts", entry.data.get("selected_cts", []))
    enable_node_controls = entry.options.get(
        "enable_node_controls", entry.data.get("enable_node_controls", False)
    )

    node = entry.data.get(CONF_NODE, "Proxmox")
    server_type = entry.data.get(CONF_PLATFORM_TYPE, "PVE")
    features = data.get("features", {})

    entities = []
    c_data = coordinator.data

    if not c_data:
        _LOGGER.warning("No data found in coordinator for %s", node)
        return

    # =========PVE BUTTONS===================
    if server_type == "PVE":

        device_registry = dr.async_get(hass)
        device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, f"proxmox_node_{node}")},
            manufacturer="Proxmox",
            model="Proxmox Node",
            name=f"1. Node: {node}",
        )

        # NODE BUTTONS
        if enable_node_controls:
            entities.append(
                ProxmoxNodeButton(
                    coordinator, client, node, "Node", "reboot", "mdi:restart"
                )
            )
            entities.append(
                ProxmoxNodeButton(
                    coordinator, client, node, "Node", "shutdown", "mdi:power"
                )
            )

        # LXC buttons
        if features.get("enable_cts", True):
            ct_map = c_data.get("cts", {})
            for ct_id, ct_data in ct_map.items():
                if str(ct_id) in selected_cts:
                    label = ct_data.get("name", ct_id)

                    ct_commands = [
                        ("start", "mdi:play"),
                        ("shutdown", "mdi:power"),
                        ("stop", "mdi:stop"),
                        ("reboot", "mdi:restart"),
                    ]

                    for cmd, icon in ct_commands:
                        entities.append(
                            ProxmoxContainerButton(
                                coordinator, client, ct_id, node, label, cmd, icon
                            )
                        )

        # VM buttons
        if features.get("enable_vms", True):
            vm_map = c_data.get("vms", {})
            for vm_id, vm_data in vm_map.items():
                if str(vm_id) in selected_vms:
                    label = vm_data.get("name", vm_id)

                    vm_commands = [
                        ("start", "mdi:play"),
                        ("shutdown", "mdi:power"),
                        ("stop", "mdi:stop"),
                        ("reboot", "mdi:restart"),
                        ("reset", "mdi:restart-alert"),
                        ("pause", "mdi:pause"),
                        ("hibernate", "mdi:download"),
                        ("resume", "mdi:play-pause"),
                    ]

                    for cmd, icon in vm_commands:
                        entities.append(
                            ProxmoxVMButton(
                                coordinator, client, vm_id, node, label, cmd, icon
                            )
                        )

    # ========PBS BUTTONS====================
    elif server_type == "PBS":
        server_id = entry.data.get("server_id", "pbs_main")
        datastores = c_data.get("pbs_datastores", {})

        for datastore_name in datastores.keys():
            entities.append(PBSGCButton(coordinator, client, datastore_name))
            entities.append(PBSPruneButton(coordinator, client, datastore_name))
            entities.append(PBSVerifyButton(coordinator, client, datastore_name))
            entities.append(PBSSyncButton(coordinator, client, datastore_name))

    _LOGGER.info(f"Total button entities created: {len(entities)}")
    async_add_entities(entities)


# =======PBS BUTTON CLASSES=============


class PBSBaseButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, client, datastore, command_name, command_display):
        super().__init__(coordinator)
        self._client = client
        self._datastore = datastore
        self._sensor_entity_id = f"sensor.{datastore.lower()}_last_action"
        self._command_name = command_name
        self._command_display = command_display

        self._attr_unique_id = f"{datastore.lower()}_{command_name}"
        self._attr_name = command_display

        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"maintenance_{datastore}")},
            "name": f"Maintenance: {datastore}",
            "manufacturer": "Proxmox",
            "model": "Proxmox Backup Server",
        }

    @property
    def available(self):
        return self.coordinator.last_update_success

    def _update_last_action(self, message: str):
        self.hass.states.async_set(self._sensor_entity_id, message)


class PBSGCButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "gc", "Garbage Collect")
        self._attr_icon = "mdi:recycle"

    async def async_press(self):
        await run_gc(self._client, self.hass, self._datastore)
        self._update_last_action("GC OK")
        await self.coordinator.async_request_refresh()


class PBSPruneButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "prune", "Prune")
        self._attr_icon = "mdi:delete-sweep"

    async def async_press(self):
        await run_prune(self._client, self.hass, self._datastore)
        self._update_last_action("Prune OK")
        await self.coordinator.async_request_refresh()


class PBSVerifyButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "verify", "Verify")
        self._attr_icon = "mdi:check-decagram"

    async def async_press(self):
        await run_verify(self._client, self.hass, self._datastore)
        self._update_last_action("Verify OK")
        await self.coordinator.async_request_refresh()


class PBSSyncButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "sync", "Sync")
        self._attr_icon = "mdi:sync"

    async def async_press(self):
        await run_sync(self._client, self.hass, self._datastore)
        self._update_last_action("Sync OK")
        await self.coordinator.async_request_refresh()


# =======PVE BUTTON CLASSES=========


class ProxmoxBaseButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, client, vmid, node, label, command, icon):
        super().__init__(coordinator)
        self._client = client
        self._vmid = vmid
        self._node = node
        self._label = label
        self._command = command

        self._attr_unique_id = f"proxmox_{node}_{vmid}_{command}"
        self._attr_name = f"{command.capitalize()} {label}"
        self._attr_icon = icon

    async def async_press(self):
        try:
            data = self.coordinator.data
            is_vm = False
            is_ct = False

            if "vms" in data:
                vms_keys = [str(k) for k in data["vms"].keys()]
                if str(self._vmid) in vms_keys:
                    is_vm = True

            if "cts" in data and not is_vm:
                cts_keys = [str(k) for k in data["cts"].keys()]
                if str(self._vmid) in cts_keys:
                    is_ct = True

            if not is_vm and not is_ct:
                _LOGGER.error(
                    f"VM/CT {self._vmid} no encontrado en datos del coordinador"
                )
                _LOGGER.error(
                    f"VMs disponibles: {[str(k) for k in data.get('vms', {}).keys()]}"
                )
                _LOGGER.error(
                    f"CTs disponibles: {[str(k) for k in data.get('cts', {}).keys()]}"
                )
                return

            result = False
            if is_vm:
                result = await self._client.execute_vm_command(
                    self.hass, self._node, self._vmid, self._command
                )
            else:
                result = await self._client.execute_ct_command(
                    self.hass, self._node, self._vmid, self._command
                )

            if result:
                await asyncio.sleep(2)
                await self.coordinator.async_request_refresh()
                self.async_write_ha_state()
                _LOGGER.info(f"Comando {self._command} completado para {self._vmid}")
            else:
                _LOGGER.error(f"Comando {self._command} falló para {self._vmid}")

        except Exception as e:
            _LOGGER.error(f"Error ejecutando comando en {self._vmid}: {e}")


class ProxmoxVMButton(ProxmoxBaseButton):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._vmid}_v1")},
            "manufacturer": "Proxmox",
            "model": "Virtual Machine",
            "name": f"4. VM: {self._label}-({self._vmid})",
            "via_device": (DOMAIN, f"proxmox_node_{self._node}"),
        }


class ProxmoxContainerButton(ProxmoxBaseButton):
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._vmid}_v1")},
            "manufacturer": "Proxmox",
            "model": "Container",
            "name": f"3. CT: {self._label}-({self._vmid})",
            "via_device": (DOMAIN, f"proxmox_node_{self._node}"),
        }


class ProxmoxNodeButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, client, node, label, command, icon):
        super().__init__(coordinator)
        self._client = client
        self._node = node
        self._command = command
        self._attr_icon = icon

        self._attr_unique_id = f"{node}_node_{command}"
        self._attr_name = f"{label} – {command.capitalize()}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
            "name": f"1. Node: {self._node}",
        }

    async def async_press(self):
        try:
            if hasattr(self._client, "execute_node_command"):
                result = await self._client.execute_node_command(
                    self.hass, self._node, self._command
                )
            else:
                path = f"nodes/{self._node}/status"
                data = {"command": self._command}
                result = await self._client.post(self.hass, path, data)

            if result:
                await asyncio.sleep(3)
                await self.coordinator.async_request_refresh()
                self.async_write_ha_state()
                _LOGGER.info(f"Node command {self._command} executed successfully")
            else:
                _LOGGER.error(f"Node command {self._command} failed")

        except Exception as e:
            _LOGGER.error(f"Error executing {self._command} on node {self._node}: {e}")
