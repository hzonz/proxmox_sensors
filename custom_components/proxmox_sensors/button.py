"""Button entities for Proxmox Virtual Environment (PVE) and Proxmox Backup Server (PBS)."""
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .pbs_actions import run_gc, run_prune, run_verify, run_sync
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    if data.get("server_type") == "PVE":
        client = getattr(coordinator, "client", data.get("client"))
    else:
        client = data.get("client")

    node = data.get("node", "Proxmox_Node")
    features = data.get("features", {})

    entities = []

    # =========PVE BUTTONS===================
    if data.get("server_type") == "PVE":

        # LXC buttons
        if features.get("enable_cts", True):
            for ct_id, ct_data in coordinator.data.get("cts", {}).items():
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
            for vm_id, vm_data in coordinator.data.get("vms", {}).items():
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
    elif data.get("server_type") == "PBS":
        datastores = coordinator.data.get("pbs_datastores", {})

        for datastore_name in datastores.keys():
            entities.append(PBSGCButton(coordinator, client, datastore_name))
            entities.append(PBSPruneButton(coordinator, client, datastore_name))
            entities.append(PBSVerifyButton(coordinator, client, datastore_name))
            entities.append(PBSSyncButton(coordinator, client, datastore_name))

    async_add_entities(entities)


# =========PVE BUTTON CLASSES===================

class ProxmoxContainerButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, client, ct_id, node, label, command, icon):
        super().__init__(coordinator)
        self._client = client
        self._ct_id = ct_id
        self._node = node
        self._label = label
        self._command = command
        self._attr_icon = icon
        self._attr_name = command.capitalize()
        self._attr_unique_id = (
            f"pve_button_ct_{node}_{ct_id}_{command}_v4".lower()
        )

    async def async_press(self):
        if self._client:
            _LOGGER.info(
                "Sending %s command to Container %s", self._command, self._label
            )
            await self._client.control_container(
                self.hass, self._node, self._ct_id, self._command
            )
            await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._ct_id}_v4")},
            "name": f"3. CT: {self._label}",
            "via_device": (DOMAIN, f"proxmox_node_{self._node}"),
            "manufacturer": "Proxmox",
            "model": "LXC Container",
        }


class ProxmoxVMButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, client, vm_id, node, label, command, icon):
        super().__init__(coordinator)
        self._client = client
        self._vm_id = vm_id
        self._node = node
        self._label = label
        self._command = command
        self._attr_icon = icon
        self._attr_name = command.capitalize()
        self._attr_unique_id = (
            f"pve_button_vm_{node}_{vm_id}_{command}_v4".lower()
        )

    async def async_press(self):
        if self._client:
            _LOGGER.info(
                "Sending %s command to VM %s", self._command, self._label
            )
            await self._client.control_vm(
                self.hass, self._node, self._vm_id, self._command
            )
            await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"proxmox_vm_{self._vm_id}")},
            "name": f"4. VM: {self._label}",
            "via_device": (DOMAIN, f"proxmox_node_{self._node}"),
            "manufacturer": "Proxmox",
            "model": "QEMU Virtual Machine",
        }


# ======PBS BUTTON CLASSES===============

class PBSBaseButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator)
        self._client = client
        self._datastore = datastore
        self._sensor_entity_id = f"sensor.{datastore.lower()}_last_action"

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
        """Update the Last Action sensor via Home Assistant."""
        self.hass.states.async_set(self._sensor_entity_id, message)


class PBSGCButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore)
        self._attr_unique_id = f"{datastore.lower()}_gc"

    @property
    def name(self):
        return f"{self._datastore} – Garbage Collect"

    async def async_press(self):
        await run_gc(self._client, self.hass, self._datastore)
        self._update_last_action("GC OK")
        await self.coordinator.async_request_refresh()


class PBSPruneButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore)
        self._attr_unique_id = f"{datastore.lower()}_prune"

    @property
    def name(self):
        return f"{self._datastore} – Prune"

    async def async_press(self):
        await run_prune(self._client, self.hass, self._datastore)
        self._update_last_action("Prune OK")
        await self.coordinator.async_request_refresh()


class PBSVerifyButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore)
        self._attr_unique_id = f"{datastore.lower()}_verify"

    @property
    def name(self):
        return f"{self._datastore} – Verify"

    async def async_press(self):
        await run_verify(self._client, self.hass, self._datastore)
        self._update_last_action("Verify OK")
        await self.coordinator.async_request_refresh()


class PBSSyncButton(PBSBaseButton):
    def __init__(self, coordinator, client, datastore):
        super().__init__(coordinator, client, datastore)
        self._attr_unique_id = f"{datastore.lower()}_sync"

    @property
    def name(self):
        return f"{self._datastore} – Sync"

    async def async_press(self):
        await run_sync(self._client, self.hass, self._datastore)
        self._update_last_action("Sync OK")
        await self.coordinator.async_request_refresh()