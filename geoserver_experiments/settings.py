import logging
import json
import os


settings = {

    # To be used by Flask: DEVELOPMENT ONLY
    "debug": True,

    "geoserver": {
        "geoserver_master": "http://hqlprfenixapp2.hq.un.fao.org:12200/geoserver/rest",
        "geoserver_slaves": [
            "http://hqlprfenixapp2.hq.un.fao.org:12300/geoserver/rest",
            "http://hqlprfenixapp2.hq.un.fao.org:12400/geoserver/rest",
            "http://hqlprfenixapp2.hq.un.fao.org:12500/geoserver/rest",
        ],
        "username": "fenix",
        "password": "Fenix2014",
        "default_workspace": "fenix",
        # this is used as default datasource to this is a reference to the spatial_db
        # da vedere!
        # this should be connected with the current spatial db
        "default_datastore": "pgeo"
    },

}
