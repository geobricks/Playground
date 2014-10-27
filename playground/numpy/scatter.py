import numpy as np
from osgeo import gdal
from pgeo.gis.raster import get_nodata_value
import time
from pylab import hexbin,show
from scipy.ndimage import measurements
from scipy.stats import itemfreq
import rasterio
from pgeo.gis.raster_scatter import  couples_with_freq, get_series, create_scatter
import brewer2mpl
import threading


#old
def scatter_old(raster_path1, raster_path2, band1=1, band2=1, buckets=100):

    ds1 = gdal.Open(raster_path1)
    band1 = ds1.GetRasterBand(band1)
    array1 = np.array(band1.ReadAsArray())

    array1 = np.array(array1).flatten()
    print "DAJE"


    nodata1 = band1.GetNoDataValue()
    print "array1"
    ds2 = gdal.Open(raster_path2)
    band2 = ds2.GetRasterBand(band2)
    array2 = np.array(band2.ReadAsArray())
    array2 = np.array(array2).flatten()

    nodata2 = band2.GetNoDataValue()
    print "array2"

    rows = ds1.RasterYSize
    cols = ds1.RasterXSize
    rows2 = ds2.RasterYSize
    cols2 = ds2.RasterXSize

    # min/max calulation
    (min1, max1) = band1.ComputeRasterMinMax(0)
    step1 = (max1 - min1) / buckets

    (min2, max2) = band2.ComputeRasterMinMax(0)
    step2 = (max2 - min2) / buckets

    # print nodata1, nodata2
    print rows, cols
    # print rows2, cols2
    # print min1, max1
    # print min2, max2
    # print step1, step2


    # frequency_count
    # matrix = frequency_count(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets)
    # print len(array1), len(array1[0]), len(array2),len(array1[0])
    # print rows, cols, min1, min2

    # couples without frequencies
    #matrix = couples_without_frequency(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets)
    matrix = couples_with_freq(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets)
    #matrix = couples_with_freq_multithread(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets)

    print len(matrix), len(array1), len(array2),len(array1)
    print rows, cols, min1, min2

    # data couples data
    #matrix = couple_data(array1, array2,  min1, min2, max1, max2, rows, cols)
    #freq = itemfreq(matrix)
    #print len(freq)
    #for v in freq:
    #    print v

    return matrix, min1, min2, max1, max2, step1, step2


# care about no data
# and buckets
def scatter(raster_path1, raster_path2, band1=1, band2=1, buckets=100):
    print "here2"

    with rasterio.open(raster_path1) as ds1:
        with rasterio.open(raster_path2) as ds2:

            print "here1"
            b = rasterio.band(ds1, band1)
            print b

            array1 = ds1.read(band1)
            band1 = ds1.read_band(band1)

            meta1 = ds1.meta
            rows = meta1['height']
            cols = meta1['width']
            min1 = band1.min()
            max1 = band1.max()

            array2 = ds2.read(band2)
            band2 = ds2.read_band(band2)
            min2 = band2.min()
            max2 = band2.max()

            step1 = (max1 - min1) / buckets
            step2 = (max2 - min2) / buckets

            print len(array1), len(array1[0]), len(array2),len(array1[0])
            print rows, cols, min1, min2


            matrix = couple_data(array1, array2,  min1, min2, max1, max2, rows, cols)

            print "end"

            return matrix, min1, min2, max1, max2, step1, step2


def frequency_count(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets, nodata=None):
    #matrix = np.zeros((buckets+1, buckets+1))
    #dict = {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
    dict = {}
    print "frequency_count"
    for i in range(0, rows):
        for j in range(0, cols):
            if array1[i][j] > min1 and array2[i][j] > min2:
                value1 = int(array1[i][j] / step1)
                value2 = int(array2[i][j] / step2)
                if str(value1 + value2) in dict:
                    dict[str(value1 + value2)] = dict[str(value1 + value2)] + 1
                else:
                    dict[str(value1 + value2)] = 1
    return dict

def couples_without_frequency2(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets, nodata=None):
    dict = {}
    dict2 = {}
    print "couples_without_frequency2"
    for i in range(0, len(array1)):
            if array1[i]> min1 and array2[i]> min2:
                #value1 = str(int(array1[i][j] / step1))
                #value2 = str(int(array2[i][j] / step2))
                #dict[value1 + value2] = [value1, value2]
                value1 = str(round(array1[i], 0))
                value2 = str(round(array2[i], 0))

                val = str(value1 + "_" + value2)
                dict[val] = [value1, value2]
                if val in dict2:
                     dict2[val] = dict2[val] + 1
                else:
                     dict2[val] = 1
    return dict



def couples_without_frequency(array1, array2, step1, step2, min1, min2, max1, max2, rows, cols, buckets, nodata=None):
    dict = {}
    dict2 = {}
    print "couples_without_frequency"
    for i in range(0, rows):
        for j in range(0, cols):
            if array1[i][j] > min1 and array2[i][j] > min2:
                value1 = str(int(array1[i][j] / step1))
                value2 = str(int(array2[i][j] / step2))
                dict[value1 + value2] = [value1, value2]




                # if str(value1 + value2) in dict:
                #     dict2[str(value1 + value2)] = dict2[str(value1 + value2)] + 1
                # else:
                #     dict2[str(value1 + value2)] = 1

                # if str(value1 + value2) in dict:
                #     dict[str(value1 + value2)] = dict[str(value1 + value2)] + 1
                # else:
                #     dict[str(value1 + value2)] = 1
                    #matrix[value1][value2] = matrix[value1][value2] + 1


                    # if array1[i][j] > min1 and array2[i][j] > min2:
                    # value1 = int(array1[i][j] / step1)
                    # value2 = int(array2[i][j] / step2)
                    #dict[str(value1 + value2)] = 1
                    #matrix[value1][value2] = matrix[value1][value2]+1
                    #matrix[value1][value2] = 1
    return dict


def couple_data(array1, array2,  min1, min2, max1, max2, rows, cols, nodata=None):
    matrix = []
    for i in range(0, rows):
        for j in range(0, cols):
            if (array1[i][j] > min1) and (array2[i][j] > min2):
                matrix.append([array1[i][j], array2[i][j]])
    return matrix



#raster1 = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output/actual_biomprod_201010_doukkala_utm29n_30m.tif"
#raster2 = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output/potential_biomprod_201010_doukkala_utm29n_30m.tif"

raster1 = "/home/vortex/Desktop/LAYERS/TRMM/Rainfall_03_2014.tif"
raster2 = "/home/vortex/Desktop/LAYERS/TRMM/Rainfall_04_2014.tif"

np.set_printoptions(suppress=True)
start_time = time.time()
test1 = create_scatter(raster1, raster2, 1, 1, 300)
print("TOTAL --- %s seconds ---" % str(time.time() - start_time))
#start_time = time.time()
#test2 = scatter(raster1, raster2, 1, 1, 50000)
#print("TOTAL--- %s seconds ---" % str(time.time() - start_time))

#print "---"
#print len(test1[0])
#print "---"
#print scatter
#print "////"
# for v in test1:
#     print "---"
#     print v
#     break


#series = get_series(test1[0].values())

# values = test1[0].values()
#
# classification_values = []
# for v in values:
#     classification_values.append(v['freq'])
#
# classes = classification_quantile(classification_values, 7)
# bmap = brewer2mpl.get_map('Set1', 'qualitative', 8)
# colors = bmap.hex_colors
#
# # creating series
# series = []
# for color in colors:
#     print color
#     series.append({
#         "color": color,
#         "data" : []
#     })
#
# print classes
# val = 0;
# for v in values:
#      freq = v['freq']
#      added = False
#      for i in range(len(classes)):
#          if val <= freq <= classes[i]:
#             series[i]['data'].append(v['data'])
#             added = True
#          val = classes[i]
#
#      if added is False:
#         series[len(classes)]['data'].append(v['data'])
#
# print "Series"
# print series
#

# print series
#
# for s in series:
#     print len(s['data']), "+"




# parse heatmap
# step1 = scatter[3]
# step2 = scatter[6]
# m = []
# categoriesx = []
# categoriesy = []
# for i in range(len(scatter[0])):
#     for j in range(len(scatter[0][i])):
#         m.append([i, j, scatter[0][i][j]])
#
# print("--- %s seconds ---" % str(time.time() - start_time))
#
# for i in range(len(scatter[0])):
#     categoriesx.append(str(i*step1))
# print("--- %s seconds ---" % str(time.time() - start_time))
#
# for j in range(len(scatter[0][0])):
#     categoriesy.append(str(j*step2))
# print("--- %s seconds ---" % str(time.time() - start_time))

# parse scatter
# step1 = scatter[3]
# step2 = scatter[6]
# m = []
# categoriesx = []
# categoriesy = []
# for i in range(len(scatter[0])):
#     for j in range(len(scatter[0][i])):
#         m.append([i, j, scatter[0][i][j]])
#
# for i in range(len(scatter[0])):
#     categoriesx.append(str(i*step1))
#
# for j in range(len(scatter[0][0])):
#     categoriesy.append(str(j*step2))



# print("--- %s seconds ---" % str(time.time() - start_time))
# print m
# print categoriesy
# print categoriesx
# print len(categoriesx)
# print len(categoriesy)