"""Sensor platform for MyUpway."""
from homeassistant.components.sensor import SensorEntity

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import IntegrationMyUpwayEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    sensors.append(IntegrationMyUpwaySensor(coordinator, entry))
    sensors.append(IntegrationMyUpwaySensor(coordinator, entry))

    async_add_devices(sensors)

class IntegrationMyUpwaySensor(IntegrationMyUpwayEntity, SensorEntity):
    """MyUpway Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON
