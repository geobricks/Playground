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
import sys


log = logger("playground.data_processing.earthstat")

input_file = "/home/vortex/Desktop/LAYERS/AFRIPOP/to_publish/ap10v4_TOTAL.tif"
output_folder = "/home/vortex/Desktop/LAYERS/AFRIPOP/to_publish/output/"

manager = Manager(settings)


def process():
    if os.path.isdir(output_folder):
        log.info("already exists")
    else:
        os.mkdir(output_folder)
    output_file = output_folder + get_filename(input_file) + ".tif"
    process_layers(input_file, output_file)
    print output_file

def publish_layers():
    print "Publish Layers"
    files = glob.glob(output_folder + "/*.tif")
    print files
    for f in files:
        print f
        # read filename
        name = get_filename(f)

        # get commodity name
        title = name.replace("_", " ").capitalize()

        print title

        # create metadata
        creationDate =  calendar.timegm(datetime.datetime.now().timetuple())
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
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "AFRIPOP"}]
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "AFRIPOP"}]
        metadata_def["meSpatialRepresentation"] = {}
        metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
        metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "africa_population"

        # merging metata to raster metadata
        metadata_def = merge_layer_metadata("raster", metadata_def)

        manager.publish_coverage(f, metadata_def)

        print metadata_def







# process()
publish_layers()
