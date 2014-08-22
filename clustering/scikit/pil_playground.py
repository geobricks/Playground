import gdalnumeric
from  PIL import Image, ImageEnhance
import gdal
from gdalconst import *

src = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/normal.tif"

dst = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched.tif"


image = Image.open(src)

enhancer = ImageEnhance.Contrast(image)

image.save(dst, "tiff")

# get parameters
src_dataset = gdal.Open(src)
geotransform = src_dataset.GetGeoTransform()
spatialreference = src_dataset.GetProjection()
ncol = src_dataset.RasterXSize
nrow = src_dataset.RasterYSize
nband = 1

# create dataset for output
fmt = 'GTiff'
driver = gdal.GetDriverByName(fmt)
dst_dataset = gdal.Open(dst, GA_Update)
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)





