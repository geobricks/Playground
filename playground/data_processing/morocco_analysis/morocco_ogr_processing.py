import os
import glob
from pgeo.utils.filesystem import get_filename
import shutil
import subprocess
from osgeo import ogr



def process(input_folder, output_folder, srcproj, dstproj):
    print "Processing data %s %s %s ", input_folder, output_folder

    ext = "shp"

    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    try:
        input_files = glob.glob(input_folder + "/*." + ext)
        for input_file in input_files:
            output_filename = output_folder + "/" + get_filename(input_file) + "." + ext
            cmd = "ogr2ogr -f 'ESRI Shapefile' -s_srs " + srcproj + " -t_srs " + dstproj + " " + output_filename + " " + input_file
            print cmd
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            print output
            print error

    except Exception, e:
        print e
        pass



input_folder = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/SHAPEFILE"
output_folder = input_folder + "/3857"

process(input_folder, output_folder, '"+proj=utm +zone=29 +datum=WGS84 +units=m +no_defs"', '"EPSG:3857"')


#process_file("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/original/wheat_mask.tif", "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/", process_layer_parameters_3857)