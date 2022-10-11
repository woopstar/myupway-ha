"""Constants for integration_myupway."""
# Base component constants
NAME = "MyUpway Integration"
DOMAIN = "integration_myupway"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.2"
ATTRIBUTION = "Data provided by https://myupway.com/"
ISSUE_URL = "https://github.com/woopstar/myupway-ha/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration to implement MyUpway!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
