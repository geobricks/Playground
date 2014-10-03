from osgeo import gdal
import pyproj



# Define projection for 2-km and 4-km Texas domains

wsg84 = pyproj.Proj("+init=EPSG:4326")
print wsg84.is_latlong()
print wsg84.srs
print wsg84.proj_version
print wsg84.is_geocent()


