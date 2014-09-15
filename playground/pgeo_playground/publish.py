from pgeo.geoserver.geoserver import Geoserver
import glob
import os

settings = {

    # Folders
    "folders": {
        "config": "config/",
        "tmp": "/home/vortex/Desktop/LAYERS/tmp",
        "data_providers": "data_providers/",
        "metadata": "metadata/",
        "stats": "stats/",
        "geoserver": "geoserver/",

        # used on runtime statistics (for Published layers this is the Geoservers Cluster "datadir")
        "geoserver_datadir": "/home/vortex/Desktop/LAYERS/TRMM",
    },

    # Geoserver
    "geoserver": {
        "geoserver_master": "http://hqlprfenixapp2.hq.un.fao.org:12200/geoserver/rest",
        "geoserver_slaves": [],
        "username": "fenix",
        "password": "Fenix2014",
        "default_workspace": "fenix",
        # this is used as default datasource to this is a reference to the spatial_db
        # da vedere!
        "default_db": "spatial"
    }

}


g = Geoserver(settings["geoserver"])

files = glob.glob("/home/vortex/Desktop/LAYERS/TRMM/OUTPUT/*.tif")
workspace = "fenix"
stylename = "raster_rainfall"

# files = glob.glob("/home/vortex/Desktop/LAYERS/Temperature_WorldClim/OUTPUT/*.tif")
# workspace = "fenix"
# stylename = "raster_temperature_mean"

# files = glob.glob("/home/vortex/Desktop/LAYERS/MODIS_5600/OUTPUT/*.tif")
# workspace = "fenix"
# stylename = "raster_modis_ndvi"

print files

for filepath in files:
    try:
        print filepath

        drive, path = os.path.splitdrive(filepath)
        path, filename = os.path.split(path)
        name = os.path.splitext(filename)[0]
        print name
        layer_to_publish = {
            "name" : name,
            "workspace" : workspace,
            "defaultStyle" : {
                "name": stylename
            },
            "path": filepath
        }
        added = g.publish_coveragestore(layer_to_publish)
        print "Layer %s (%s)" % (name, str(added))
        added = g.set_default_style(name, stylename)
        print "Layer %s styled (%s)" % (name, str(added))
        print "----"
    except:
        pass