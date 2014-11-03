import os
import glob
from pgeo.utils.filesystem import get_filename
import shutil
import subprocess
from playground.data_processing.processing import process_layers


process_layer_parameters_3857 = {
    "gdalwarp" : {
        "-overwrite": "",
        "-multi": "",
        "-of": "GTiff",
        "-s_srs": "'+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'",
        #"-s_srs": "'+proj=utm +zone=29 +datum=WGS84 +units=m +no_defs'",
        "-t_srs": "EPSG:3857",
        "-tr": "35.6787 -35.6787",
        "-srcnodata": "-3.4028230607370965e+38",
        "-dstnodata": "-3000"
    },
    "gdaladdo": {
        "parameters": {
        },
        "overviews_levels": "2 4 8 16"
    }
}


def process(input_folder, output_folder, process_layer_parameters):
    print "Processing data %s %s %s ", input_folder, output_folder, process_layer_parameters

    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    try:
        input_files = glob.glob(input_folder +"/*.tif")
        for input_file in input_files:
            print input_file

            output_filename = output_folder + "/" + get_filename(input_file) + ".tif"
            print(output_filename)

            # create a geotiff + overviews
            process_layers(input_file, output_filename, process_layer_parameters)

    except Exception, e:
        print e
        pass


def process_file(input_file, output_folder, process_layer_parameters):

    try:
        output_filename = output_folder + "/" + get_filename(input_file) + ".tif"
        print(output_filename)

        # create a geotiff + overviews
        process_layers(input_file, output_filename, process_layer_parameters)

    except Exception, e:
        print e
        pass

input_base_path  = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/irrigated/"
output_base_path = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/irrigated/proj"

path = "/"

input_folder = input_base_path + path
output_folder = output_base_path + path

process(input_folder, output_folder, process_layer_parameters_3857)


#process_file("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/original/wheat_mask.tif", "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/", process_layer_parameters_3857)