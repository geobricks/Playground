# script to count the number of non-zero pixels in the first band
import os, sys, ogr, gdal, utils, numpy
from gdalconst import *







#os.chdir(r'Z:\Data\Classes\Python\data')
# register all of the GDAL drivers
print " here"
gdal.AllRegister()
# open the image
ds = gdal.Open('/home/vortex/Desktop/LAYERS/MODIS_5600/single_band', GA_ReadOnly)
if ds is None:
    print 'Could not open aster.img'

# get image size
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount

# get the band and block sizes
band = ds.GetRasterBand(1)
blockSizes = band.GetBlockSize()
print blockSizes
xBlockSize = blockSizes[0]
yBlockSize = blockSizes[1]
# initialize variable
count = 0

# loop through the rows
for i in range(0, rows, yBlockSize):
    if i + yBlockSize < rows:
        numRows = yBlockSize
    else:
        numRows = rows - i
    # loop through the columns
    for j in range(0, cols, xBlockSize):
        if j + xBlockSize < cols:
            numCols = xBlockSize
        else:
            numCols = cols - j

        # read the data and do the calculations
        data = band.ReadAsArray(j, i, numCols, numRows).astype(numpy.float16)
        mask = numpy.greater(data, 0)
        count = count + numpy.sum(numpy.sum(mask))



# print results
print 'Number of non-zero pixels:', count