from pgeo.gis.gdal_calc import calc_layers
import calendar
import datetime
import time
import json
import os
from pgeo.config.settings import settings, read_template
from pgeo.metadata.metadata import Metadata
from pgeo.manager.manager import Manager
from pgeo.utils.log import logger
from pgeo.metadata.metadata import merge_layer_metadata
import subprocess


log = logger("playground.trmm.trmm")

input_folder = "/home/vortex/Desktop/LAYERS/TRMM/"
output_folder = "/home/vortex/Desktop/LAYERS/TRMM/monthly/"

manager = Manager(settings)

process_layer_parameters = {
    "gdalwarp" : {
        "-multi" : "",
        "-of" : "GTiff",
        #"-tr" : "0.00833333, -0.00833333",
        #"-s_srs" :"'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
        "-s_srs" :"EPSG:4326",
        "-co": "'TILED=YES'",
        "-t_srs": "EPSG:3857",
        # "-srcnodata" : "nodata",
        # "-dstnodata" : "nodata"
    },
    "gdaladdo" : {
        "parameters" : {
            "-r" : "average"
        },
        "overviews_levels" : "2 4 8 16"
    }
}



def dt2unix(dt):
    return int(time.mktime(dt.timetuple()) + (dt.microsecond / 10.0 ** 6))


def process_trmm(input_path, output_file, parameters):
    cmd = "gdalwarp "
    for key in parameters["gdalwarp"].keys():
        cmd += " " + key + " " + str(parameters["gdalwarp"][key])
    cmd += " " + input_path + " " + output_file

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()


    cmd = "gdaladdo "
    for key in parameters["gdaladdo"]["parameters"].keys():
        cmd += " " + key + " " + str(parameters["gdaladdo"]["parameters"][key])
    cmd += " " + output_file
    cmd += " " + parameters["gdaladdo"]["overviews_levels"]

    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def calc_trmm_monthly(year, month):
    try:
        files_path = input_folder  + year+ "/" + month + "/*.tif"
        output_filename = "trmm_"+ month +"_"+ year +".tif"
        output_file = output_folder + output_filename


        # calculate layers
        #calc_layers(files_path, outputfile, "sum")


        if os.path.isfile(output_file):
            # get metadata
            from_date, to_date = get_range_dates_metadata(month, year)
            creationDate = dt2unix(datetime.datetime.now())


            # Sample of Metadata json
            log.info("Creating metadata")
            metadata_def = {}
            metadata_def["title"] = {}
            metadata_def["title"]["EN"] = "TRMM " + month + "-" + year
            metadata_def["creationDate"] = creationDate
            metadata_def["meContent"] = {}
            metadata_def["meContent"]["seCoverage"] = {}
            metadata_def["meContent"]["seCoverage"]["coverageTime"] = {}
            metadata_def["meContent"]["seCoverage"]["coverageTime"]["from"] = from_date
            metadata_def["meContent"]["seCoverage"]["coverageTime"]["to"] = to_date
            metadata_def["meContent"]["seCoverage"]["coverageSector"] = {}
            metadata_def["meContent"]["seCoverage"]["coverageSector"]["codeList"] = "Products"
            metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "TRMM"}]
            metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "TRMM"}]
            metadata_def["meSpatialRepresentation"] = {}
            metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
            metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "rain"

            # merging metadata to the base raster one
            metadata_def = merge_layer_metadata("raster", metadata_def)

            # "seCoverage" : {
            #     "coverageTime" : {
            #         "from" : 1328405808080,
            #         "to": 1328405808080
            #     },
            #     "coverageGeographic" : {
            #         "codeList" : "...",
            #         "version" : "...",
            #         "codes" : [{"code" : "world"}]
            #     },
            #     "coverageSector" : {
            #         "codeList" : "...",
            #         "version" : "...",
            #         "codes" : [{"code" : "MODISQ1"}]
            #     }
            # }]

            log.info(metadata_def)
            #obj_id = metadata.db_metadata.insert_metadata(metadata_def)


            # covert to geotiff 3857 the file
            if os.path.isdir(output_folder + "/output"):
                pass
            else:
                os.mkdir(output_folder + "/output")
            output_processed_file = output_folder + "/output/" + output_filename
            process_trmm(output_file, output_processed_file, process_layer_parameters)


            print manager.publish_coverage(output_processed_file, metadata_def)
        else:
            log.error("No file named %s " % output_file)

    except Exception, e:
        print e
        pass


def get_range_dates_metadata(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    #from_date = "01-01" + year
    #to_date = "01-" + last_day + "-" + year
    from_date = datetime.datetime(int(year), int(month), 1)
    to_date = datetime.datetime(int(year), int(month), last_day)
    return dt2unix(from_date), dt2unix(to_date)




# def get_metadata():
#     files = glob.glob(output_folder + "*.tif")
#     for file in files:
#         name = get_filename(file)
#         month = name[5:7]
#         print month
#         year  = name[8:]
#         print year



# Parameters
years = ['2012', '2013', '2014']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
product = '3B42RT'

# calculating sum
for year in years:
    for month in months:
        calc_trmm_monthly(year, month)

#get_metadata()

