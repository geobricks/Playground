import gdalnumeric
import gdal
from gdalconst import *

# # Input file name (thermal image)
# src = "/home/vortex/Desktop/LAYERS/MODIS/somalia.tif"
#
# # Output file name
# tgt = "/home/vortex/Desktop/LAYERS/MODIS/classified.jpg"
#
# # Load the image into numpy using gdal
# srcArr = gdalnumeric.LoadFile(src)
#
#
# # Color look-up table (LUT) - must be len(classes)+1.
# # Specified as R,G,B tuples
# lut = [[255,0,0],[191,48,48],[166,0,0],[255,64,64],
#        [255,115,115],[255,116,0],[191,113,48],[57,230,57],[103,230,103],[184,138,0]]
#
# # Split the histogram into 20 bins as our classes
# classes = gdalnumeric.numpy.histogram(srcArr, bins=len(lut)-1)[1]
#
# print len(classes)
# print len(lut)
#
# # Starting value for classification
# start = 1
#
# # Set up the RGB color JPEG output image
# rgb = gdalnumeric.numpy.zeros((3, srcArr.shape[0],
#                                srcArr.shape[1],), gdalnumeric.numpy.float32)
#
# # Process all classes and assign colors
# for i in range(len(classes)):
#     mask = gdalnumeric.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
#     for j in range(len(lut[i])):
#         rgb[j] = gdalnumeric.numpy.choose(mask, (rgb[j], lut[i][j]))
#     start = classes[i]+1
#
# # Save the image
# gdalnumeric.SaveArray(rgb.astype(gdalnumeric.numpy.uint8), tgt, format="JPEG")


#Input file name (thermal image)
#src = "/home/vortex/Desktop/LAYERS/MODIS/somalia.tif"
src = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/rgb.tif"

# Output file name
tgt = "/home/vortex/Desktop/LAYERS/lorenzo/classified2.tif"

# Load the image into numpy using gdal
srcArr = gdalnumeric.LoadFile(src)


# Color look-up table (LUT) - must be len(classes)+1.
# Specified as R,G,B tuples
lut = [[0], [80], [100], [135], [137], [150]]

# Split the histogram into 20 bins as our classes
classes = gdalnumeric.numpy.histogram(srcArr, bins=len(lut)-1)[1]

print len(classes)
print len(lut)

# Starting value for classification
start = 1

# Set up the RGB color JPEG output image
print srcArr.shape[0]
print srcArr.shape[1]
#rgb = gdalnumeric.numpy.zeros((3, srcArr.shape[0], srcArr.shape[1],), gdalnumeric.numpy.float32)
rgb = gdalnumeric.numpy.zeros((3, srcArr.shape[0], srcArr.shape[1],), gdalnumeric.numpy.float32)

# Process all classes and assign colors
for i in range(len(classes)):
    mask = gdalnumeric.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
    for j in range(len(lut[i])):
        print str(lut[i])
        rgb[j] = gdalnumeric.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1

# Save the image

gdalnumeric.SaveArray(rgb.astype(gdalnumeric.numpy.uint8), tgt, format="GTiff")





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
dst_dataset = gdal.Open(tgt, GA_Update)
dst_dataset.SetGeoTransform(geotransform)
dst_dataset.SetProjection(spatialreference)




# img = open_image('/home/vortex/Desktop/LAYERS/MODIS/somalia.lan').load()
#
#
#
# classes = create_training_classes(img, gt, True)
# means = np.zeros((len(classes), img.shape[2]), float)
# for (i, c) in enumerate(classes):
#     means[i] = c.stats.mean

# (m, c) = kmeans(img, 20, 30)
#
# pylab.figure()
#
# pylab.hold(1)
#
# for i in range(c.shape[0]):
#     pylab.plot(c[i])
#
# pylab.show()