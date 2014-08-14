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
import re


log = logger("playground.data_processing.earthstat")

input_folder = "/home/vortex/Desktop/LAYERS/earthstat/175CropsYieldArea_geotiff/*"
output_folder = "/home/vortex/Desktop/LAYERS/earthstat/output/"

manager = Manager(settings)

def dt2unix(dt):
    return int(time.mktime(dt.timetuple()) + (dt.microsecond / 10.0 ** 6))

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
        title = name.replace("_", " ").replace("1", "").capitalize()



        # create metadata
        creationDate = dt2unix(datetime.datetime.now())
        metadata_def = {}
        metadata_def["title"] = {}
        metadata_def["title"]["EN"] = title
        metadata_def["creationDate"] = creationDate
        metadata_def["meContent"] = {}
        metadata_def["meContent"]["seCoverage"] = {}
        metadata_def["meContent"]["seCoverage"]["coverageTime"] = {}
        # TODO: in theory 1970-2010?
        # metadata_def["meContent"]["seCoverage"]["coverageTime"]["from"] = "1970"
        # metadata_def["meContent"]["seCoverage"]["coverageTime"]["to"] = "2010"
        metadata_def["meContent"]["seCoverage"]["coverageSector"] = {}
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codeList"] = "Products"
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "EARTHSTAT"}]
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "EARTHSTAT"}]
        metadata_def["meSpatialRepresentation"] = {}
        metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
        metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "earthstat_area"

        # merging metata to raster metadata
        metadata_def = merge_layer_metadata("raster", metadata_def)

        # get type
        if "area" in title:
            manager.publish_coverage(f, metadata_def)
            # if "Banana" in title:
            #     # publish on manager
            #     manager.publish_coverage(f, metadata_def)







publish_layers()
#process_earthstat()
