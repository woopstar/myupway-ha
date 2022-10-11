"""Sensor platform for MyUpway."""
from homeassistant.components.sensor import SensorEntity

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import IntegrationMyUpwayEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IntegrationMyUpwaySensor(coordinator, entry)])


class IntegrationMyUpwaySensor(IntegrationMyUpwayEntity, SensorEntity):
    """MyUpway Sensor class."""

    def __init__(self):
        """Initialize the sensor."""
        self._hass = hass
        self._hass.custom_attributes = {}

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._hass.custom_attributes

    def update(self):
        attributes = {}
        attributes['mac'] = 'some data'
        attributes['sn'] = 'some other data'
        self._hass.custom_attributes = attributes

    @property
    def unique_id(self):
        """Return the unique id."""
        return f"{DEFAULT_NAME}_{SENSOR}"

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
