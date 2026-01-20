import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup Proxmox buttons with distribution standards."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    
    client = getattr(coordinator, "client", data.get("client"))
    node = data.get("node", "Proxmox_Node")
    features = data.get("features", {})
    
    entities = []
    
    if data.get("server_type") == "PVE":
        # 1. Container (LXC) Buttons
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
                    entities.append(ProxmoxContainerButton(coordinator, client, ct_id, node, label, cmd, icon))

        # 2. Virtual Machine (VM) Buttons
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
                   ("resume", "mdi:play-pause")
                ]
                
                for cmd, icon in vm_commands:
                    entities.append(ProxmoxVMButton(coordinator, client, vm_id, node, label, cmd, icon))
    
    async_add_entities(entities)

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
        # Changed to v4 to match sensor cleaning
        self._attr_unique_id = f"pve_button_ct_{node}_{ct_id}_{command}_v4".lower()

    async def async_press(self) -> None:
        if self._client:
            _LOGGER.info("Sending %s to CT %s", self._command, self._label)
            await self._client.control_container(self.hass, self._node, self._ct_id, self._command)
            await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        return {
            # IDENTIFIER MUST MATCH SENSOR EXACTLY (v4)
            "identifiers": {(DOMAIN, f"proxmox_ct_{self._ct_id}_v4")},
            # NAME MUST MATCH SENSOR EXACTLY (3. CT:)
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
        # Changed to v4
        self._attr_unique_id = f"pve_button_vm_{node}_{vm_id}_{command}_v4".lower()

    async def async_press(self) -> None:
        if self._client:
            _LOGGER.info("Sending %s to VM %s", self._command, self._label)
            await self._client.control_vm(self.hass, self._node, self._vm_id, self._command)
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