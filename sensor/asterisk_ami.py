from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.entity import Entity

DATA_ASTERISK = 'asterisk'
DATA_MONITOR = 'asterisk-monitor'


def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([AsteriskSensor(hass)])
    for extension in hass.data[DATA_MONITOR]:
        add_devices([AsteriskExtension(hass, extension)])


class AsteriskSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self._hass = hass
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Asterisk Connection'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def should_poll(self):
        return True

    def update(self):
        if self._hass.data[DATA_ASTERISK].connected():
            self._state = 'connected'
        else:
            self._state = 'disconnected'


class AsteriskExtension(Entity):
    def __init__(self, hass, extension):
        self._hass = hass
        self._extension = extension
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        return "Asterisk Extension " + str(self._extension)

    @property
    def state(self):
        return self._state

    @property
    def should_poll(self):
        return True

    def update(self):
        response = self._hass.data[DATA_ASTERISK].sipshowpeer(self._extension)
        if response.get_header("Response", "Error") == "Error":
            self._state = STATE_UNKNOWN
            return
        else:
            status_header = response.get_header("Status", "unknown")
            if "OK" in status_header:
                self._state = "OK"
                return
            else:
                self._state = status_header
