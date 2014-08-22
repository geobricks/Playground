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
from pgeo.utils.filesystem import get_filename


manager = Manager(settings)



def dt2unix(dt):
    return int(time.mktime(dt.timetuple()) + (dt.microsecond / 10.0 ** 6))

creationDate = dt2unix(datetime.datetime.now())



# Sample of Metadata json
metadata_def = {}
metadata_def["title"] = {}
metadata_def["title"]["EN"] = "modis"
metadata_def["creationDate"] = creationDate
metadata_def["meContent"] = {}
metadata_def["meContent"]["seCoverage"] = {}
metadata_def["meContent"]["seCoverage"]["coverageTime"] = {}
metadata_def["meContent"]["seCoverage"]["coverageTime"]["from"] = creationDate
metadata_def["meContent"]["seCoverage"]["coverageTime"]["to"] = creationDate

metadata_def["meContent"]["seCoverage"]["coverageSector"] = {}
metadata_def["meContent"]["seCoverage"]["coverageSector"]["codeList"] = "Products"
metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "MODIS"}]
metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "MODIS"}]


# TODO: in theory should be the original file the onlineResource
metadata_def["meAccessibility"] = {}
metadata_def["meAccessibility"]["seDistribution"] = {}
metadata_def["meAccessibility"]["seDistribution"]["onlineResource"] = "/media/vortex/16DE-3364/MODIS_250m.tif"

# TODO: added new field for the original resource (should we have two different metadata?)
#metadata_def["meAccessibility"]["seDistribution"]["originalResource"] = output_filename

# adding type of layer
aggregationProcessing = "none"
metadata_def["meStatisticalProcessing"] = {}
metadata_def["meStatisticalProcessing"]["seDatasource"] = {}
metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"] = {}
metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"]["aggregationProcessing"] = aggregationProcessing;

# default style
metadata_def["meSpatialRepresentation"] = {}
metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
if aggregationProcessing == "da":
    metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "rainfall_" + aggregationProcessing
else:
    metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "rainfall"


# merging metadata to the base raster one
metadata_def = merge_layer_metadata("raster", metadata_def)

print manager.publish_coverage("/media/vortex/16DE-3364/MODIS_250m.tif", metadata_def)