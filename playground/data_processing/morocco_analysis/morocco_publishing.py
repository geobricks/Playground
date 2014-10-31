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

def create_metadata(title, product, sldname, date, measurementunit):

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
    # TODO: remove it from here, ASK FRANCESCA!!
    metadata_def["measurementunit"] = measurementunit

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
    return metadata_def


def get_range_dates_metadata(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    from_date = datetime.datetime(int(year), int(month), 1)
    to_date = datetime.datetime(int(year), int(month), last_day)
    return calendar.timegm(from_date.timetuple()), calendar.timegm(to_date.timetuple())


# used with: ndvi, precipitation
def publish_data_timeseries(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")

    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        if "ndvi" in input_file:
            #print "name %s, sld %s, date %s, area %s" % (info[0], info[1], info[2], info[3])
            title = info[0].upper() + " " + info[1] + " - " + info[2].capitalize()
            product = info[2].capitalize() + " - " + info[0].upper()
        if "precipitation" in input_file:
            title = info[0].capitalize() + " " + info[1] + " - " + info[2].capitalize()
            product = info[2].capitalize() + " - " + info[0].capitalize()

        sldname = "morocco_" + info[0]
        date = info[1]
        metadata_def = create_metadata(title, product, sldname, date,  get_measurement_unit(title))
        print metadata_def
        manager.publish_coverage(input_file, metadata_def)


# used with: temperature
def publish_data_temperature(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        #print "name %s, sld %s, date %s, area %s" % (info[0], info[1], info[2], info[3])
        title = "Temperature " + info[2] + " - " + info[3].capitalize()
        sldname = "morocco_temperature"
        date = info[2]
        product = info[3].capitalize() + " - Temperature"
        metadata_def = create_metadata(title, product, sldname, date, get_measurement_unit(title))
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def)


def publish_data_meteo_evapotranspiration(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    for input_file in input_files:

        info = str.split(get_filename(input_file), "_")
        if "actual" in input_file:
            type = "actual"
        if "potential" in input_file:
            type = "potential"
        if "ETref" in input_file:
            type = "reference"


        #print "name %s, sld %s, date %s, area %s" % (info[0], info[1], info[2], info[3])
        title = type.capitalize() + " evapotransipiration " + " " + info[1] + " - " + info[2].capitalize()
        sldname = "morocco_evapotransipiration"
        date = info[1]
        product = info[2].capitalize() + " - " + type + " evapotransipiration"
        metadata_def = create_metadata(title, product, sldname, date, get_measurement_unit(title))
        #manager.publish_coverage(input_file, metadata_def)


# wheat seasonal data
def publish_data_wheat_seasonal(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    for input_file in input_files:
        if "wheat_productivity" not in input_file and "yieldgap" not in input_file:
            info = str.split(get_filename(input_file), "_")
            #print "name %s, sld %s, date %s, area %s" % (info[0], info[1], info[2], info[3])
            #title = info[4].capitalize() + " - " + info[0] + " " + info[1] + " " + info[2] + " - " + info[3]
            # title = info[4].capitalize() + " - " + info[0] + " " + info[1] + " " + info[2] + " - " + info[3]
            title = info[2] + " - " + info[3]
            sldname = "morocco_" + info[2]
            date = "201401" # FAKE DATE!!!
            product = info[4].capitalize() + " - " + info[0] + " " + info[1]
            metadata_def = create_metadata(title, product, sldname, date, get_measurement_unit(title))
            #print metadata_def
            #manager.publish_coverage(input_file, metadata_def)
        if "water" in input_file:
            info = str.split(get_filename(input_file), "_")
            title =  info[2] + " " + info[3]
            sldname = "morocco_" + info[2] + "_" + info[3]
            date = "201401" # FAKE DATE!!!
            product = info[4].capitalize() + " - " + info[0] + " " + info[1]
            metadata_def = create_metadata(title, product, sldname, date, get_measurement_unit(title))
            #print metadata_def
        if "yieldgap" in input_file:
            info = str.split(get_filename(input_file), "_")
            title = info[2]
            sldname = "morocco_" + info[2]
            date = "201401" # FAKE DATE!!!
            product = info[3].capitalize() + " - " + info[0] + " " + info[1]
            metadata_def = create_metadata(title, product, sldname, date, get_measurement_unit(title))

        # publishing
        #manager.publish_coverage(input_file, metadata_def)


def get_measurement_unit(name):
    if "temperature" in name.lower():
        return "C"
    if "biom" in name.lower():
        return "kg/ha"
    if "yieldgap" in name.lower():
       return ""
    if "yield" in name.lower():
       return "kg/ha"
    if "transpiration" in name.lower():
       return "mm"
    if "precipitation" in name.lower():
        return "mm"
    if "ndvi" in name.lower():
        return ""
    if "water" in name.lower():
       return "kg/m3"
    return ""

#publish_data_timeseries("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/ndvi/")
publish_data_timeseries("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/precipitation/")

# evapotranspiration
#publish_data_meteo_evapotranspiration("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/evapotranspiration/actual/")
#publish_data_meteo_evapotranspiration("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/evapotranspiration/potential/")
#publish_data_meteo_evapotranspiration("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/evapotranspiration/ETRef/")



#publish_data_wheat_seasonal("/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/wheat_seasonal/")
