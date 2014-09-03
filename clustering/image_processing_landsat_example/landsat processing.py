from osgeo import gdal, osr, ogr
import os
import subprocess
import glob
import math
import json
from pgeo.utils import log
from pgeo.utils import filesystem
from pgeo.error.custom_exceptions import PGeoException, errors


print "LANDSAT 7 PROCESSING"

def extract_band(input_file, output_file, band):
    print "todo extranct 4, 3 ,2"
    input_file = input_file + "_B" + band+ ".TIF"
    output_file = output_file + "_" + band + ".tif"
    #gdalwarp -t_srs EPSG:3857 input_file$BAND.TIF $BAND-output_file.tif;
    cmd = "gdalwarp -t_srs EPSG:3857 " + input_file + " " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error

    return output_file


def convert_into_rgb(files, output_file):
    print "combine rgb"
    #convert -combine {4,3,2}-projected.tif RGB.tif
    cmd = "convert -combine "
    for file in files:
        cmd += file + " "

    cmd += output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error



def convert_true_color(input_file, output_file):
    #convert -sigmoidal-contrast 50x16% RGB.tif RGB-corrected.tif
    cmd = "convert -sigmoidal-contrast 50x16% "

    cmd += input_file + " " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error


def correct_image(input_file, output_file):
    print "correct image"
    #convert -channel B -gamma 0.925 -channel R -gamma 1.03 -channel RGB -sigmoidal-contrast 50x16% RGB.tif RGB-corrected.tif

    cmd = "convert -channel B -gamma 0.925 -channel R -gamma 1.03 -channel RGB -sigmoidal-contrast 50x16% "

    cmd += input_file + " " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error


path = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/2003_02/LE71690602003035SGS00/"
path_rgb = path + "rgb/"

input_file = path + "LE71690602003035SGS00"
output_file_band = path_rgb + "projected"

# extracting bands
files = []
# 5,4,3
files.append(extract_band(input_file, output_file_band, "5"))
files.append(extract_band(input_file, output_file_band, "4"))
files.append(extract_band(input_file, output_file_band, "3"))


# merge to rgb
output_file_rgb = path_rgb + "rgb.tif"
convert_into_rgb(files, output_file_rgb)


#true_color
output_file_true_color = path_rgb + "rgb_true_color.tif"
convert_true_color(output_file_rgb, output_file_true_color)


#correct_image
output_file_corrected = path_rgb + "rgb_corrected.tif"
convert_true_color(output_file_rgb, output_file_corrected)




#projected_5.tif threshold




