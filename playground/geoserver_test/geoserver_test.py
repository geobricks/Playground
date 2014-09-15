from pgeo.geoserver.geoserver import Geoserver
from pgeo.config.settings import settings
from pgeo.utils import log
from pgeo.error.custom_exceptions import PGeoException
import sys
import random

log = log.logger("pgeo.geoserver.geoserver_test")


g = Geoserver(settings["geoserver"])


try:
    g.reload_configuration_geoserver_slaves()
except PGeoException, e:
    log.error(e)

