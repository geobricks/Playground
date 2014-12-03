from geoserver.catalog import Catalog
import geoserver.util


cat = Catalog("http://localhost:9090/geoserver/rest/")
cat.username = "admin"
cat.password = "geoserver"

workspace = cat.get_workspace("fenix")
cat.create_coveragestore("test_gsconfig2", "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/original/wheat_mask.tif", workspace)
layer = cat.get_layer("test_gsconfig2")
layer._set_default_style("mask")
cat.save(layer)
# print cat
# print "here"
# layer = cat.get_style("burg")
