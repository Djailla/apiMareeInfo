"""Sensor for my first"""
import logging

from datetime import timedelta, datetime

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_CODE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from . import apiMareeInfo, sensorApiMaree
from .const import (
    __name__,
)

_LOGGER = logging.getLogger(__name__)
DOMAIN = "saniho"
ICON = "mdi:package-variant-closed"
SCAN_INTERVAL = timedelta(seconds=1800)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CODE): cv.string,
        vol.Required(CONF_LATITUDE): cv.string,
        vol.Required(CONF_LONGITUDE): cv.string,
    }
)


class myMareeInfo:
    def __init__(self, idDuPort, lat, lng, _update_interval):
        self._lastSynchro = None
        self._update_interval = _update_interval
        self._idDuPort = idDuPort
        self._lat = lat
        self._lng = lng
        self._myMaree = apiMareeInfo.ApiMareeInfo()
        pass

    def update(
        self,
    ):
        date_now = datetime.now()
        # _LOGGER.warning("-update possible- ?")
        if (self._lastSynchro is None) or (
            (self._lastSynchro + self._update_interval) < date_now
        ):
            self._myMaree.setport(self._lat, self._lng)
            self._myMaree.getinformationport()
            self._lastSynchro = date_now

    def getIdPort(self):
        return self._idDuPort

    # revoir recupearation valeur
    def getmyMaree(self):
        return self._myMaree

    def getDateCourante(self):
        return self._myMaree.getdatecourante()


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the platform."""
    name = config.get(CONF_NAME)
    update_interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    try:
        idDuPort = config.get(CONF_CODE)
        lat = config.get(CONF_LATITUDE)
        lng = config.get(CONF_LONGITUDE)
        session = []
    except:
        _LOGGER.exception("Could not run my apiMaree Extension miss argument ?")
        return False
    myPort = myMareeInfo(idDuPort, lat, lng, update_interval)
    myPort.update()
    add_entities([infoMareeSensor(session, name, update_interval, myPort)], True)


class infoMareeSensor(Entity):
    """."""

    def __init__(self, session, name, interval, myPort):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myPort = myPort
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)
        self._sAM = sensorApiMaree.manageSensorState()
        self._sAM.init(self._myPort.getmyMaree())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myPort.%s.MareeDuJour" % self._myPort.getIdPort()

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return ""

    def _update(self):
        """Update device state."""
        self._myPort.update()
        self._state, self._attributes = self._sAM.getstatus()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON
