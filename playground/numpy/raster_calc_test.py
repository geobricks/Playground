# script to count the number of non-zero pixels in the first band
import os, sys, ogr, gdal, utils, numpy
from gdalconst import *
import raster_calc
import time

gdal.AllRegister()


def test(file_path):
    startTime = time.time()
    ds = raster_calc.get_ds(file_path)
    bands, rows, cols = raster_calc.get_bands_rows_cols_bands(ds)
    band = ds.GetRasterBand(1)
    formulaTime = time.time()
    print raster_calc.apply_formula(band, rows, cols)
    endTime = time.time()
    print 'The script took ' + str(formulaTime - startTime) + ' seconds'
    print 'The script took ' + str(endTime - startTime) + ' seconds'


def test_sum(file_path1, file_path2):
    startTime = time.time()

    ds1 = raster_calc.get_ds(file_path1)
    bands1, rows1, cols1 = raster_calc.get_bands_rows_cols_bands(ds1)
    band1 = ds1.GetRasterBand(1)

    ds2 = raster_calc.get_ds(file_path2)
    band2 = ds2.GetRasterBand(1)
    formulaTime = time.time()


    #print raster_calc.apply_formula(band1, rows1, cols1)
    dst_ds = raster_calc.apply_formula_sum(band1, band2, rows1, cols1)
    dst_ds.SetGeoTransform(ds1.GetGeoTransform())
    dst_ds.SetProjection(ds1.GetProjection())
    endTime = time.time()
    print 'The script took ' + str(formulaTime - startTime) + ' seconds'
    print 'The script took ' + str(endTime - startTime) + ' seconds'


# start timing
file_name = '/home/vortex/Desktop/LAYERS/MODIS_5600/GHG_INDONESIA/land_cover_maryland.tiff'

#test(file_name)
test_sum(file_name, file_name)

