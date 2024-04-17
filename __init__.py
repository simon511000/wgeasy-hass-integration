"""The WireGuard Easy integration."""

from __future__ import annotations

from wg_easy_api_wrapper import Server

from .config_flow import InvalidAuth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_URL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WireGuard Easy from a config entry."""
    data = entry.data

    hass.data.setdefault(DOMAIN, {})
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    server = Server(data[CONF_URL].strip("/"), data[CONF_PASSWORD])

    try:
        await server.login()
        isAuthenticated = await server.is_logged_in()

        if not isAuthenticated:
            raise InvalidAuth

        hass.data[DOMAIN][entry.entry_id] = server
    except Exception as exception:
        await server.__aexit__(None, exception, None)
        raise ConfigEntryNotReady from exception

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        server = hass.data[DOMAIN].pop(entry.entry_id)
        await server.__aexit__(None, None, None)

    return unload_ok
