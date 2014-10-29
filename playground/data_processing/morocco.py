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

process_layer_parameters_3857 = {
    "gdalwarp" : {
        "-overwrite" : "",
        "-multi" : "",
        "-of" : "GTiff",
        "-s_srs" :"EPSG:32629",
        "-t_srs": "EPSG:3857",
    },
    "gdaladdo" : {
        "parameters" : {

        },
        "overviews_levels" : "2 4 8 16"
    }
}


process_layer_parameters_4326 = {
    "gdalwarp" : {
        "-overwrite" : "",
        "-multi" : "",
        "-of" : "GTiff",
        "-s_srs" :"EPSG:32629",
        "-t_srs": "EPSG:4326",
        }
}


def process(input_folder, output_folder, process_layer_parameters):
    print "Processing data %s %s %s ", input_folder, output_folder, process_layer_parameters

    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

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


def processing_data():
    print "Processing data"

    # processing data
    input_folder = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/"
    output_folder_3857 = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output_3857"
    output_folder_4326 = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output_4326"

    process(input_folder, output_folder_3857, process_layer_parameters_3857)
    process(input_folder, output_folder_4326, process_layer_parameters_4326)

    # processing Wheat data
    input_folder = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/Wheat/"
    output_folder_3857 = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output_3857/wheat"
    output_folder_4326 = "/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output_4326/wheat"


    process(input_folder, output_folder_3857, process_layer_parameters_3857)
    process(input_folder, output_folder_4326, process_layer_parameters_4326)

def create_metadata(name, sldname, date, area):

    # TODO: important this is a new workspace
    workspace = "morocco"

    creationDate = calendar.timegm(datetime.datetime.now().timetuple())

    # get metadata
    year = int(date[:4])
    month = int(date[4:])
    from_date, to_date = get_range_dates_metadata(month, year)

    # get title name
    title = name + " " + sldname + " " + area + " " + str(month) + "-" + str(year)

    product = "MOROCCO-" + name.upper()

    # Sample of Metadata json
    metadata_def = {}
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
    metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"]["aggregationProcessing"] = aggregationProcessing;

    # default style
    metadata_def["meSpatialRepresentation"] = {}
    metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
    metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "morocco_" + sldname
    return metadata_def

def get_range_dates_metadata(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    from_date = datetime.datetime(int(year), int(month), 1)
    to_date = datetime.datetime(int(year), int(month), last_day)
    return calendar.timegm(from_date.timetuple()), calendar.timegm(to_date.timetuple())

def publish_data(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        #print "name %s, sld %s, date %s, area %s" % (info[0], info[1], info[2], info[3])
        if "irrigated" not in info[0]:
            pass
            # metadata_def = create_metadata(info[0], info[1], info[2], info[3])
            # manager.publish_coverage(input_file, metadata_def)
        else:
            name = info[0] + " " + info[1] + " " + info[2]
            sldname = info[0] + "_" + info[1] + "_"  +info[2]
            metadata_def = create_metadata(name, sldname, "201410", info[3])
            manager.publish_coverage(input_file, metadata_def)


def publish_data_wheat(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        #print "name %s, sld %s, date %s, area %s" % (info[0], info[1], info[2], info[3])
        if "water_productivity" in input_file:
            name = info[0] + " " + info[1] + " " + info[2]
            sldname = info[1] + "_" + info[2]
            metadata_def = create_metadata(name, sldname, "201410", info[3])
            manager.publish_coverage(input_file, metadata_def)
        if "yieldgap" in input_file:
            name = info[0] + " " + info[1]
            sldname = info[1]
            metadata_def = create_metadata(name, sldname, "201410", info[3])
            manager.publish_coverage(input_file, metadata_def)
        if "yield" in input_file:
            name = info[0] + " " + info[1] + " " + info[2]
            sldname = info[2]
            metadata_def = create_metadata(name, sldname, "201410", info[3])
            manager.publish_coverage(input_file, metadata_def)
        if "seasonal" in input_file:
            name = info[0] + " " + info[1] + " " + info[2] + " " + info[3]
            sldname = info[3]
            metadata_def = create_metadata(name, sldname, "201410", info[4])
            manager.publish_coverage(input_file, metadata_def)

#processing_data()
publish_data("/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output_3857")

#publish_data_wheat("/home/vortex/Desktop/LAYERS/MOROCCO/Morocco/output_3857/wheat")