"""Astisk Component"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import (CONF_HOST, CONF_PASSWORD, CONF_PORT,
                                 CONF_USERNAME)
from homeassistant.helpers.discovery import load_platform

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5038
DEFAULT_USERNAME = "manager"
DEFAULT_PASSWORD = "manager"
CONF_MONITOR = "monitor"
CONF_MAILBOX = "mailboxes"

DOMAIN = "asterisk_ami"
REQUIREMENTS = ['pyst2==0.5.0']
DATA_ASTERISK = 'asterisk'
DATA_MONITOR = 'asterisk-monitor'
DATA_MAILBOX = 'asterisk-mailbox'
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT): cv.port,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_MONITOR): cv.ensure_list,
        vol.Optional(CONF_MAILBOX): cv.ensure_list
    })
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Your controller/hub specific code."""

    import asterisk.manager
    manager = asterisk.manager.Manager()

    host = config[DOMAIN].get(CONF_HOST, DEFAULT_HOST)
    port = config[DOMAIN].get(CONF_PORT, DEFAULT_PORT)
    username = config[DOMAIN].get(CONF_USERNAME, DEFAULT_USERNAME)
    password = config[DOMAIN].get(CONF_PASSWORD, DEFAULT_PASSWORD)

    try:
        manager.connect(host, port)
        login_status = manager.login(username=username, secret=password).get_header("Response")
    except asterisk.manager.ManagerException as exception:
        _LOGGER.error("Error connecting to Asterisk: %s", exception.args[1])
        return False

    if "Success" not in login_status:
        _LOGGER.error("Could not authenticate: %s", login_status)

    hass.data[DATA_ASTERISK] = manager
    hass.data[DATA_MONITOR] = config[DOMAIN].get(CONF_MONITOR, [])
    hass.data[DATA_MAILBOX] = config[DOMAIN].get(CONF_MAILBOX, [])

    load_platform(hass, 'sensor', DOMAIN)

    return True
