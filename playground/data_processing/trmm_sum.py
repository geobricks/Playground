from pgeo.gis.gdal_calc import calc_layers
import calendar
import datetime
import time
import json
import os
import glob
from pgeo.config.settings import settings, read_template
from pgeo.metadata.metadata import Metadata
from pgeo.manager.manager import Manager
from pgeo.utils.log import logger
from pgeo.metadata.metadata import merge_layer_metadata
from data_processing.processing import process_layers
from pgeo.utils.filesystem import get_filename, remove


# TODO: remove all metadata trmm layers on mongo
# db.layer.remove( { uid: { $regex: 'trmm_*', $options: 'i' } } );


log = logger("playground.data_processing.trmm")

input_folder = "/home/vortex/Desktop/LAYERS/TRMM_alex/Aggregations_16d/*"
output_folder = "/home/vortex/Desktop/LAYERS/TRMM_alex/Aggregations_16d/"

manager = Manager(settings)


# def dt2unix(dt):
#     return int(time.mktime(dt.timetuple()) + (dt.microsecond / 10.0 ** 6))


def calc_trmm():

    # take folders
    folders = glob.glob(input_folder)
    for folder in folders:
        print input_folder
        # create output folder /output
        # covert to geotiff 3857 the file
        if os.path.isdir(folder + "/output"):
            remove(folder + "/output/*.tif")
        else:
            os.mkdir(folder + "/output")


        folder_name = folder[folder.rindex("/")+1:]

        print folder_name

        file_output = folder + "/3b42_" + folder_name + "_4326.tif"

        print file_output
        # sum *.tif to output folder
        input_files = glob.glob(folder +"/*.tif")
        calc_layers(input_files, file_output, "sum")

        file_output_processed = folder + "/output/3b42_" + folder_name + ".tif"
        process_layers(file_output, file_output_processed)


calc_trmm()

