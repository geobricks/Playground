import calendar
import glob
import os
import datetime
# from pgeo.config.settings import settings, read_template
from pgeo.metadata.metadata import Metadata
from pgeo.manager.manager import Manager
from pgeo.utils.log import logger
# from pgeo.metadata.metadata import merge_layer_metadata
# from data_processing.processing import process_layers
from pgeo.utils.filesystem import get_filename


manager = Manager(settings)

default_style = "ghg_burnedareas"


def publish():
    path = "/home/vortex/Desktop/LAYERS/GHG/"
    for dir in os.listdir(path):
        filepath = os.path.join(path, dir, dir + ".geotiff")
        p, fp, name = get_filename(filepath, True)
        print p
        print fp
        print name
        date = name[len(name)-4:]
        product_code = name[:len(name)-5]
        print date
        print product_code

        creationDate = calendar.timegm(datetime.datetime.now().timetuple())


        from_date = datetime.datetime(int(date), int(1), 1)
        to_date = datetime.datetime(int(date), int(12), 31)


        # Sample of Metadata json
        metadata_def = {}
        metadata_def["title"] = {}
        metadata_def["title"]["EN"] = name
        metadata_def["creationDate"] = creationDate
        metadata_def["meContent"] = {}
        metadata_def["meContent"]["seCoverage"] = {}
        metadata_def["meContent"]["seCoverage"]["coverageTime"] = {}
        metadata_def["meContent"]["seCoverage"]["coverageTime"]["from"] = from_date
        metadata_def["meContent"]["seCoverage"]["coverageTime"]["to"] = to_date

        metadata_def["meContent"]["seCoverage"]["coverageSector"] = {}
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codeList"] = "Products"
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : product_code}]
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : product_code}]


        # TODO: in theory should be the original file the onlineResource
        metadata_def["meAccessibility"] = {}
        metadata_def["meAccessibility"]["seDistribution"] = {}
        # metadata_def["meAccessibility"]["seDistribution"]["onlineResource"] = "/media/vortex/16DE-3364/MODIS_250m.tif"

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
        metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = default_style


        # merging metadata to the base raster one
        metadata_def = merge_layer_metadata("raster", metadata_def)

        #print manager.publish_coverage(filepath, metadata_def)
        print manager.geoserver.set_default_style(name, default_style)



publish()

