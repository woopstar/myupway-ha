"""Sample API Client."""
import logging
import asyncio
import socket
from typing import Optional
import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}

TYPE_TEMPERATURE = "temperature"
TYPE_CURRENT = "current"
TYPE_DIMENSIONLESS = "dimensionless"
TYPE_BOOLEAN_YES_NO = "boolean_yes_no"
TYPE_BOOLEAN_ON_OFF = "boolean_on_off"
TYPE_TIME = "time_period"
TYPE_POWER = "power"
TYPE_ENERGY = "energy"
TYPE_FLOW = "flow"
TYPE_PERCENTAGE = "percentage"
TYPE_PRESSURE = "pressure"
TYPE_FREQUENCY = "frequency"
UNIT_CELSIUS = "C"
UNIT_AMPERES = "A"
UNIT_DEGREE_MINUTES = "DM"
UNIT_HOURS = "h"
UNIT_KILOWATTS = "kW"
UNIT_KILOWATT_HOURS = "kWh"
UNIT_LITERS_PER_MINUTE = "l/m"
UNIT_PERCENT = "%"
UNIT_BAR = "bar"
UNIT_HERTZ = "Hz"
UNIT_NONE = ""

definition_groups = {
    "tehowatti_status": {
        40067: {"name": "avg. outdoor temp. BT1", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40014: {"name": "hot water charging BT6", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40013: {"name": "hot water top BT7", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40004: {"name": "outdoor temp. BT1", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40083: {"name": "current BE1", "type": TYPE_CURRENT, "unit": UNIT_AMPERES},
        40081: {"name": "current BE2", "type": TYPE_CURRENT, "unit": UNIT_AMPERES},
        40079: {"name": "current BE3", "type": TYPE_CURRENT, "unit": UNIT_AMPERES},
        43005: {"name": "degree minutes", "type": TYPE_DIMENSIONLESS, "unit": UNIT_DEGREE_MINUTES},
    },
    "tehowatti_hot_water": {
        48132: {"name": "temporary lux", "type": TYPE_BOOLEAN_ON_OFF, "unit": UNIT_NONE},
        47041: {"name": "comfort mode", "type": TYPE_DIMENSIONLESS, "unit": UNIT_NONE},
    },
    "tehowatti_climate_system_1": {
        43161: {"name": "external adjustment S1", "type": TYPE_BOOLEAN_YES_NO, "unit": UNIT_NONE},
        47276: {"name": "floor drying function", "type": TYPE_BOOLEAN_ON_OFF, "unit": UNIT_NONE},
        43009: {"name": "calculated flow temp. S1", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40071: {"name": "external flow temp. BT25", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40008: {"name": "heat medium flow BT2", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40012: {"name": "return temp. BT3", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        40033: {"name": "room temperature BT50", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
    },
    "tehowatti_addition": {
        10033: {"name": "blocked", "type": TYPE_BOOLEAN_YES_NO, "unit": UNIT_NONE},
        47214: {"name": "fuse size", "type": TYPE_CURRENT, "unit": UNIT_AMPERES},
        43081: {"name": "time factor", "type": TYPE_TIME, "unit": UNIT_HOURS},
        43084: {"name": "electrical addition power", "type": TYPE_POWER, "unit": UNIT_KILOWATTS},
        47212: {"name": "set max electrical add.", "type": TYPE_POWER, "unit": UNIT_KILOWATTS},
        40121: {"name": "addition temperature BT63", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
    },
    "tehowatti_heat_meter": {
        44302: {"name": "cooling, compr. only.", "type": TYPE_ENERGY, "unit": UNIT_KILOWATT_HOURS},
        44308: {"name": "heating, compr. only.", "type": TYPE_ENERGY, "unit": UNIT_KILOWATT_HOURS},
        44300: {"name": "heating, int. add. incl.", "type": TYPE_ENERGY, "unit": UNIT_KILOWATT_HOURS},
        44306: {"name": "hotwater, compr. only.", "type": TYPE_ENERGY, "unit": UNIT_KILOWATT_HOURS},
        44298: {"name": "hw, incl. int. add", "type": TYPE_ENERGY, "unit": UNIT_KILOWATT_HOURS},
        44304: {"name": "pool, compr. only.", "type": TYPE_ENERGY, "unit": UNIT_KILOWATT_HOURS},
        40072: {"name": "flow BF1", "type": TYPE_FLOW, "unit": UNIT_LITERS_PER_MINUTE},
    },
    # Soft inputs (AUX1-AUX5) not implemented
    "inverter_m8_status": {
        44703: {"name": "defrosting EB101", "type": TYPE_BOOLEAN_YES_NO, "unit": UNIT_NONE},
        44396: {"name": "pump speed heating medium GP1", "type": TYPE_PERCENTAGE, "unit": UNIT_PERCENT},
        44362: {"name": "outdoor temp. EB101-BT28", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
    },
    "inverter_m8_compressor_module": {
        10014: {"name": "blocked", "type": TYPE_BOOLEAN_YES_NO, "unit": UNIT_NONE},
        44069: {"name": "compressor starts EB101", "type": TYPE_DIMENSIONLESS, "unit": UNIT_NONE},
        44702: {"name": "cpr. protection mode EB101", "type": TYPE_BOOLEAN_YES_NO, "unit": UNIT_NONE},
        44058: {"name": "condenser out EB101-BT12", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        44363: {"name": "evaporator EB101-BT16", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        44059: {"name": "hot gas EB101-BT14", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        44060: {"name": "liquid line EB101-BT15", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        44055: {"name": "return temp. EB101-BT3", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        44061: {"name": "suction gas EB101-BT17", "type": TYPE_TEMPERATURE, "unit": UNIT_CELSIUS},
        44699: {"name": "high pressure sensor EB101", "type": TYPE_PRESSURE, "unit": UNIT_BAR},
        44700: {"name": "low pressure sensor EB101", "type": TYPE_PRESSURE, "unit": UNIT_BAR},
        44071: {"name": "compressor operating time EB101", "type": TYPE_TIME, "unit": UNIT_HOURS},
        44073: {"name": "compressor operating time hot water EB101", "type": TYPE_TIME, "unit": UNIT_HOURS},
        40737: {"name": "compressor run time cooling EB101", "type": TYPE_TIME, "unit": UNIT_HOURS},
        44701: {"name": "current compr. frequency EB101", "type": TYPE_FREQUENCY, "unit": UNIT_HERTZ},
        40782: {"name": "requested compressor freq EB101", "type": TYPE_FREQUENCY, "unit": UNIT_HERTZ},
        40001: {"name": "test", "type": TYPE_FREQUENCY, "unit": UNIT_HERTZ},
    }
}

class IntegrationMyUpwayApiClient:
    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        return await self.api_wrapper("get", url)

    async def async_set_title(self, value: str) -> None:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        await self.api_wrapper("patch", url, data={"title": value}, headers=HEADERS)

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    await self._session.post(url, headers=headers, json=data)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
