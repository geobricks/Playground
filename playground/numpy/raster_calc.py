import os, sys, ogr, gdal, utils, numpy
from gdalconst import *
import sys
from pgeo.utils.filesystem import create_tmp_filename



def get_ds(file_path, open_type=GA_ReadOnly):
    # open the image
    return gdal.Open(file_path, open_type)

def get_bands_rows_cols_bands(ds):
    rows = ds.RasterYSize
    cols = ds.RasterXSize
    bands = ds.RasterCount
    return bands, rows, cols

def get_blocksize(band):
    blockSizes = band.GetBlockSize()
    print blockSizes
    xBlockSize = blockSizes[0]
    yBlockSize = blockSizes[1]
    return xBlockSize, yBlockSize

def update_numRowsCols(i, rows_cols_value, blockSize):
    # loop through the rows
    if i + blockSize < rows_cols_value:
        num_rows_cols = blockSize
    else:
        num_rows_cols = rows_cols_value - i
    return num_rows_cols


def get_block_data(band, j, i, numCols, numRows, type=numpy.float16):
    # read the data and do the calculations
    data = band.ReadAsArray(j, i, numCols, numRows).astype(type)
    return data


def apply_formula(band, rows, cols, formula=None):
    #TODO remove count
    count = 0
    xBlockSize, yBlockSize = get_blocksize(band)
    for i in range(0, rows, yBlockSize):
        numRows = update_numRowsCols(i, rows, yBlockSize)
        for j in range(0, cols, xBlockSize):
            numCols = update_numRowsCols(j, cols, xBlockSize)
            data = get_block_data(band, j, i, numCols, numRows)
            mask = numpy.greater(data, 0)
            count = count + numpy.sum(numpy.sum(mask))
    return count


def apply_formula_sum(band1, band2, rows, cols, type=GDT_Float32, formula=None):

    #outDs = driver.Create("/home/vortex/Desktop/LAYERS/MODIS_5600/GHG_INDONESIA/land_cover_maryland.tiff/reclass_40.tif", cols, rows, 1, type)

    tmp_filename = create_tmp_filename('', 'tiff')
    print tmp_filename
    output_raster = gdal.GetDriverByName('GTiff').Create(tmp_filename,cols, rows, 1, type)  # Open the file

    #TODO remove count
    count = 0
    xBlockSize, yBlockSize = get_blocksize(band1)
    for i in range(0, rows, yBlockSize):
        sys.stdout.write(".")
        numRows = update_numRowsCols(i, rows, yBlockSize)
        for j in range(0, cols, xBlockSize):
            numCols = update_numRowsCols(j, cols, xBlockSize)
            data1 = get_block_data(band1, j, i, numCols, numRows)
            data2 = get_block_data(band2, j, i, numCols, numRows)

            data = data1 + data2
            output_raster.GetRasterBand(1).WriteArray(data,j,i)


    return output_raster





