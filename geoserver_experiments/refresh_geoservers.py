from pgeo.geoserver.geoserver import Geoserver
from settings import settings



def reload_configuration_geoserver_slaves(config):
    geoserver = Geoserver(config)
    print geoserver.reload_configuration_geoserver_slaves(False)


reload_configuration_geoserver_slaves(settings["geoserver"])
