import glob
import sys
import os
from osgeo import gdal
from ftplib import FTP
import subprocess
import datetime



def process_hdfs(obj):
    print obj

    # extract bands
    hdfs = extract_files_and_band_names(obj["source_path"], obj["band"])

    # extract hdf bands
    single_hdfs = create_hdf_files(obj["output_path"], hdfs)

    # merge tiles
    hdf_merged = merge_hdf_files(obj["output_path"], obj["output_path"], obj["gdal_merge"])

    # do stats?

    print hdfs
    print single_hdfs

    # translate
    tiff = warp_hdf_file(hdf_merged, obj["output_path"], obj["output_file_name"], obj["gdalwarp"])

    #add overviews
    if ( obj.has_key("gdaladdo") ):
        tiff = overviews_tif_file(tiff, obj["gdaladdo"]["parameters"], obj["gdaladdo"]["overviews_levels"]  )

    return tiff


def extract_files_and_band_names(path, band):
    bands = []
    hdfs = glob.glob(path + "/*.hdf")
    for f in hdfs:
        gtif = gdal.Open(f)
        sds = gtif.GetSubDatasets()
        bands.append(sds[int(band) - 1][0])
    return bands


def create_hdf_files(output_path, files):
    print "Create HDF Files"
    output_files = []
    i = 0;
    for f in files:
        print f
        cmd = "gdal_translate '" + f + "' " + output_path + "/" + str(i) + ".hdf"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        i += 1;
        #TODO catch the error
        print output
        print error

def merge_hdf_files(source_path, output_path, parameters=None):
    print "Merge HDF Files"
    print parameters
    output_file = output_path + "/output.hdf"

    # creating the cmd
    cmd = "gdal_merge.py "
    for key in parameters.keys():
        cmd += " " + key + " " + str(parameters[key])
    cmd += " " + source_path + "/*.hdf -o " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output
    print error
    return output_file

def warp_hdf_file(source_file, output_path, output_file_name, parameters=None ):
    print "Warp HDF File to Tif"
    output_file = output_path + "/" + output_file_name

    cmd = "gdalwarp "
    print parameters
    print source_file
    for key in parameters.keys():
        cmd += " " + key + " " + str(parameters[key])
    cmd += " " + source_file + " " + output_file

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    # print output
    # print error
    # return output_file


def overviews_tif_file(output_file, parameters=None, overviews_levels=None):
    print "Create Overviews TIFF File "


    cmd = "gdaladdo "
    for key in parameters.keys():
        cmd += " " + key + " " + str(parameters[key])
    cmd += " " + output_file
    cmd += " " + overviews_levels

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    # print output
    # print error
    # return output_file


obj = {
    "output_file_name" : "MODIS_03_2014.tif",
    "source_path" : "modis/",
    "band" : 1,
    "output_path" : "modis/OUTPUT",
    "gdal_merge" : {
        "-n" : -3000,
        "-a_nodata" : -3000
    },
    "gdalwarp" : {
        "-multi" : "",
        "-of" : "GTiff",
        #"-tr" : "0.00833333, -0.00833333",
        # "-s_srs" :"EPSG:4326",
        "-co" : "'TILED=YES'",
        "-t_srs" : "EPSG:3857",
        "-srcnodata" : -3000,
        "-dstnodata" : "nodata"
    },
    "gdaladdo" : {
        "parameters" : {
            "-r" : "average"
        },
        "overviews_levels" : "2 4 8 16"
    }

}


output_file = process_hdfs(obj)
print output_file
