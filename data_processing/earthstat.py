from pgeo.gis.gdal_calc import calc_layers
import calendar
import datetime
import time
import json
import os
import glob
from pgeo.utils.filesystem import get_filename
from pgeo.config.settings import settings, read_template
from pgeo.metadata.metadata import Metadata
from pgeo.manager.manager import Manager
from pgeo.utils.log import logger
from pgeo.metadata.metadata import merge_layer_metadata
from data_processing.processing import process_layers


log = logger("playground.data_processing.earthstat")

input_folder = "/home/vortex/Desktop/LAYERS/earthstat/175CropsYieldArea_geotiff/*"
output_folder = "/home/vortex/Desktop/LAYERS/earthstat/output/"


def process_earthstat():
    if os.path.isdir(output_folder):
        log.info("already exists")
    else:
        os.mkdir(output_folder)
    dir = glob.glob(input_folder + "*")
    for d in dir:
        if os.path.isdir(d):
            input_files = glob.glob(d + "/*.tif")
            for input_file in input_files:
                output_file = output_folder + get_filename(input_file) + ".tif"
                process_layers(input_file, output_file)


def publish_layers():
    files = glob.glob(output_folder + "/*.tif")
    for f in files:
        # read filename
        name = get_filename(f)

        # get commodity name

        # get type

        # remove 1 if exists

        # create metadata

        # publish on manager



process_earthstat()