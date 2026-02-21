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
            for ct_key, ct_data in ct_map.items():
                # Extract real ID from composite key
                parts = str(ct_key).split("_")
                if len(parts) >= 2:
                    actual_node = parts[0]
                    actual_ctid = parts[1]
                else:
                    actual_node = node
                    actual_ctid = ct_key

                if str(actual_ctid) in selected_cts:
                    label = ct_data.get("name", actual_ctid)

                    ct_commands = [
                        ("start", "mdi:play"),
                        ("shutdown", "mdi:power"),
                        ("stop", "mdi:stop"),
                        ("reboot", "mdi:restart"),
                    ]

                    for cmd, icon in ct_commands:
                        entities.append(
                            ProxmoxContainerButton(
                                coordinator,
                                client,
                                actual_ctid,
                                actual_node,
                                label,
                                cmd,
                                icon,
                            )
                        )

        # VM buttons
        if features.get("enable_vms", True):
            vm_map = c_data.get("vms", {})
            for vm_key, vm_data in vm_map.items():
                # Extract real ID from composite key
                parts = str(vm_key).split("_")
                if len(parts) >= 2:
                    actual_node = parts[0]
                    actual_vmid = parts[1]
                else:
                    actual_node = node
                    actual_vmid = vm_key

                if str(actual_vmid) in selected_vms:
                    label = vm_data.get("name", actual_vmid)

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
                                coordinator,
                                client,
                                actual_vmid,
                                actual_node,
                                label,
                                cmd,
                                icon,
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
    """Base class for PBS maintenance buttons."""

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
    """Garbage Collection button for PBS datastore."""

    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "gc", "Garbage Collect")
        self._attr_icon = "mdi:recycle"

    async def async_press(self):
        await run_gc(self._client, self.hass, self._datastore)
        self._update_last_action("GC OK")
        await self.coordinator.async_request_refresh()


class PBSPruneButton(PBSBaseButton):
    """Prune button for PBS datastore."""

    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "prune", "Prune")
        self._attr_icon = "mdi:delete-sweep"

    async def async_press(self):
        await run_prune(self._client, self.hass, self._datastore)
        self._update_last_action("Prune OK")
        await self.coordinator.async_request_refresh()


class PBSVerifyButton(PBSBaseButton):
    """Verify button for PBS datastore."""

    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "verify", "Verify")
        self._attr_icon = "mdi:check-decagram"

    async def async_press(self):
        await run_verify(self._client, self.hass, self._datastore)
        self._update_last_action("Verify OK")
        await self.coordinator.async_request_refresh()


class PBSSyncButton(PBSBaseButton):
    """Sync button for PBS datastore."""

    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore, "sync", "Sync")
        self._attr_icon = "mdi:sync"

    async def async_press(self):
        await run_sync(self._client, self.hass, self._datastore)
        self._update_last_action("Sync OK")
        await self.coordinator.async_request_refresh()


# =======PVE BUTTON CLASSES=========


class ProxmoxBaseButton(CoordinatorEntity, ButtonEntity):
    """Base class for PVE VM/CT buttons."""

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
        """Execute the button command."""
        try:
            data = self.coordinator.data
            # Use composite key for lookup
            vm_key = f"{self._node}_{self._vmid}"
            ct_key = f"{self._node}_{self._vmid}"

            is_vm = vm_key in data.get("vms", {})
            is_ct = ct_key in data.get("cts", {})

            if not is_vm and not is_ct:
                _LOGGER.error("VM/CT %s on node %s not found", self._vmid, self._node)
                _LOGGER.error("Available VMs: %s", list(data.get("vms", {}).keys()))
                _LOGGER.error("Available CTs: %s", list(data.get("cts", {}).keys()))
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
                _LOGGER.info(
                    "Command %s completed for %s on node %s",
                    self._command,
                    self._vmid,
                    self._node,
                )
            else:
                _LOGGER.error(
                    "Command %s failed for %s on node %s",
                    self._command,
                    self._vmid,
                    self._node,
                )

        except Exception as e:
            _LOGGER.error(
                "Error executing command on %s (%s): %s", self._vmid, self._node, e
            )


class ProxmoxVMButton(ProxmoxBaseButton):
    """Button for VM actions."""

    @property
    def device_info(self):
        """Return device info matching VM sensors."""
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._node}_{self._vmid}_v1")},
            "manufacturer": "Proxmox",
            "model": "Virtual Machine",
            "name": f"4. VM: {self._label}-({self._vmid})",
            "via_device": (DOMAIN, f"proxmox_node_{self._node}"),
        }


class ProxmoxContainerButton(ProxmoxBaseButton):
    """Button for LXC container actions."""

    @property
    def device_info(self):
        """Return device info matching CT sensors."""
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._node}_{self._vmid}_v1")},
            "manufacturer": "Proxmox",
            "model": "Container",
            "name": f"3. CT: {self._label}-({self._vmid})",
            "via_device": (DOMAIN, f"proxmox_node_{self._node}"),
        }


class ProxmoxNodeButton(CoordinatorEntity, ButtonEntity):
    """Button for node actions (reboot/shutdown)."""

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
        """Return device info matching node sensors."""
        return {
            "identifiers": {(DOMAIN, f"proxmox_node_{self._node}")},
            "manufacturer": "Proxmox",
            "model": "Proxmox Node",
            "name": f"1. Node: {self._node}",
        }

    async def async_press(self):
        """Execute node command."""
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
                _LOGGER.info("Node command %s executed successfully", self._command)
            else:
                _LOGGER.error("Node command %s failed", self._command)

        except Exception as e:
            _LOGGER.error(
                "Error executing %s on node %s: %s", self._command, self._node, e
            )
