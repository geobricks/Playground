# coding=utf-8
import os
import glob
from pgeo.utils.filesystem import get_filename
from playground.data_processing.processing import process_layers
import shutil
import calendar
import datetime
from pgeo.manager.manager import Manager
from playground.config.settings import settings

manager = Manager(settings)

def create_metadata(title, product, sldname, date, uid_distribution):

    # TODO: important this is a new workspace
    workspace = "morocco"

    creationDate = calendar.timegm(datetime.datetime.now().timetuple())

    # get metadata
    year = int(date[:4])
    month = int(date[4:])
    from_date, to_date = get_range_dates_metadata(month, year)

    # get title name
    #title = name + " " + sldname + " " + area + " " + str(month) + "-" + str(year)

    #product = "MOROCCO-" + name.upper()

    # Sample of Metadata json
    metadata_def = {}
    metadata_def["meSpatialRepresentation"] = {}
    metadata_def["meSpatialRepresentation"]["workspace"] = workspace

    metadata_def["title"] = {}
    metadata_def["title"]["EN"] = title
    metadata_def["creationDate"] = creationDate

    metadata_def["meContent"] = {}
    metadata_def["meContent"]["seCoverage"] = {}
    metadata_def["meContent"]["seCoverage"]["coverageTime"] = {}
    metadata_def["meContent"]["seCoverage"]["coverageTime"]["from"] = from_date
    metadata_def["meContent"]["seCoverage"]["coverageTime"]["to"] = to_date
    metadata_def["meContent"]["seCoverage"]["coverageSector"] = {}
    metadata_def["meContent"]["seCoverage"]["coverageSector"]["codeList"] = "Products"
    metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code": product}]

    # adding type of layer
    aggregationProcessing = "none"
    metadata_def["meStatisticalProcessing"] = {}
    metadata_def["meStatisticalProcessing"]["seDatasource"] = {}
    metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"] = {}
    metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"]["aggregationProcessing"] = aggregationProcessing

    # default style
    metadata_def["meSpatialRepresentation"] = {}
    metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
    metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = sldname

    # uid used for the distribution
    if uid_distribution is not None:
        metadata_def["distribution"] = {}
        metadata_def["distribution"]["uid"] = uid_distribution
    return metadata_def


def get_range_dates_metadata(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    from_date = datetime.datetime(int(year), int(month), 1)
    to_date = datetime.datetime(int(year), int(month), last_day)
    return calendar.timegm(from_date.timetuple()), calendar.timegm(to_date.timetuple())


# used with: ndvi, precipitation
def publish_data_GriddedLivestock(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")

    product = "Livestock"

    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")

        title = info[0].capitalize()
        product = info[2].capitalize() + " - " + info[0].upper()
        sldname = "none"
        date = info[1]
        metadata_def = create_metadata(title, product, sldname, date, None)
        #manager.publish_coverage(input_file, metadata_def)


publish_data_GriddedLivestock("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/GriddedLivestock/to_publish/")
