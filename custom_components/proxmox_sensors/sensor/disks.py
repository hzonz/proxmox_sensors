from .base import ProxmoxBaseSensor
from ..const import DOMAIN

def _format_gb(value):
    try:
        if value is None: return 0
        return round(float(value) / (1024 ** 3), 2)
    except (ValueError, TypeError):
        return 0

class ProxmoxDiskSensor(ProxmoxBaseSensor):
    """
    Sensor de capacidad de disco físico.
    Agrupados en un sub-dispositivo vinculado al Nodo.
    """

    def __init__(self, coordinator, disk_id, node, label):
        # Obtenemos la info del disco para el nombre
        disks = coordinator.data.get("disks", {})
        disk_info = disks.get(disk_id, {})
        self._model = disk_info.get("model", label or "Unknown")
        
        # Nombre limpio: "CT1000P3SSD8 Size"
        name = f"{self._model} Size"
        
        # ID Único v3
        unique_id = f"proxmox_disk_{node}_{disk_id}_v3"

        super().__init__(coordinator, disk_id, name, "GB", unique_id, node)

        self._disk_id = disk_id
        self._attr_icon = "mdi:harddisk"
        self._attr_state_class = "measurement"
        self._attr_device_class = "data_size"

    @property
    def device_info(self):
        """Agrupa todos los discos en un dispositivo vinculado al nodo principal."""
        # Forzamos minúsculas en el nodo para que el vínculo 'via_device' no falle
        node_id = self._node.lower()
        
        return {
            "identifiers": {(DOMAIN, f"proxmox_disks_group_{node_id}")},
            "name": f"2. Disks: {self._node.capitalize()}",
            "manufacturer": "Proxmox",
            "model": "Physical Disks Storage",
            # Esto vincula este dispositivo "hijo" al dispositivo "padre" (el Nodo)
            "via_device": (DOMAIN, f"proxmox_node_{node_id}"),
        }

    def _get_value(self):
        """Extrae el tamaño del disco desde el coordinador."""
        disks = self.coordinator.data.get("disks", {})
        disk = disks.get(self._disk_id)
        
        if not disk:
            return None

        size = disk.get("size")
        return _format_gb(size) if size is not None else None

    @property
    def extra_state_attributes(self):
        """Atributos adicionales en inglés."""
        disks = self.coordinator.data.get("disks", {})
        disk = disks.get(self._disk_id)

        if not disk:
            return {}

        return {
            "Model": disk.get("model", "Unknown"),
            "Serial": disk.get("serial", "N/A"),
            "Type": disk.get("type", "N/A"),
            "Raw Capacity (Bytes)": disk.get("size"),
        }