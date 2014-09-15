import glob
import os
import subprocess

source_folder = "/home/vortex/Desktop/LAYERS/TRMM/*.tif"
output_folder = "/home/vortex/Desktop/LAYERS/TRMM/OUTPUT/"

files = glob.glob(source_folder)

parameters = {
    "gdalwarp" : {
        "-multi" : "",
        "-of" : "GTiff",
        #"-tr" : "0.00833333, -0.00833333",
        #"-s_srs" :"'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
        "-s_srs" :"EPSG:4326",
        "-co": "'TILED=YES'",
        "-t_srs": "EPSG:3857",
        # "-srcnodata" : "nodata",
        # "-dstnodata" : "nodata"
    },
    "gdaladdo" : {
        "parameters" : {
            "-r" : "average"
        },
        "overviews_levels" : "2 4 8 16"
    }
}


for filepath in files:
    drive, path = os.path.splitdrive(filepath)
    path, filename = os.path.split(path)
    name = os.path.splitext(filename)[0]
    output_file = output_folder + filename

    cmd = "gdalwarp "
    for key in parameters["gdalwarp"].keys():
        cmd += " " + key + " " + str(parameters["gdalwarp"][key])
    cmd += " " + filepath + " " + output_file
    print cmd

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()


    cmd = "gdaladdo "
    for key in parameters["gdaladdo"]["parameters"].keys():
        cmd += " " + key + " " + str(parameters["gdaladdo"]["parameters"][key])
    cmd += " " + output_file
    cmd += " " + parameters["gdaladdo"]["overviews_levels"]

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()


print "END"