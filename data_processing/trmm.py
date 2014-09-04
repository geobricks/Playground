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


# TODO: remove all metadata trmm layers on mongo
# db.layer.remove( { uid: { $regex: 'trmm_*', $options: 'i' } } );


log = logger("playground.data_processing.trmm")

input_folder = "/home/vortex/Desktop/LAYERS/TRMM/"
output_folder = "/home/vortex/Desktop/LAYERS/TRMM/monthly/"

manager = Manager(settings)


# def dt2unix(dt):
#     return int(time.mktime(dt.timetuple()) + (dt.microsecond / 10.0 ** 6))


def calc_trmm_monthly(year, month, file_prefix="trmm", calc=False):
    try:
        files_path = input_folder  + year+ "/" + month + "/*.tif"
        output_filename = file_prefix+ "_"+ month +"_"+ year +".tif"
        output_file = output_folder + output_filename

        default_workspace = manager.geoserver.get_default_workspace()

        # calculate layers
        if calc:
            calc_layers(files_path, output_file, "sum")


        if os.path.isfile(output_file):

            # covert to geotiff 3857 the file
            if os.path.isdir(output_folder + "/output"):
                pass
            else:
                os.mkdir(output_folder + "/output")
            output_processed_file = output_folder + "/output/" + output_filename
            process_layers(output_file, output_processed_file)
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
    log.info(year)
    log.info(month)
    log.info(from_date)
    log.info(to_date)
    return calendar.timegm(from_date.timetuple()), calendar.timegm(to_date.timetuple())


def calc_trmm_avg_monthly(month, file_prefix="trmm", calc=False):
    try:
        files_path = output_folder + file_prefix + "_" + month +"*"
        file_output = output_folder + "avg/" + file_prefix +  "_" + month + "_avg.tif"
        file_output_processed = output_folder + "output/" + file_prefix +  "_" + month + "_avg.tif"

        log.info(files_path)
        if calc:
            calc_layers(files_path, file_output, "avg")
            process_layers(file_output, file_output_processed)

            # TODO: reproject

    except Exception, e:
        log.error(e)


def calc_trmm_da_monthly(year, month, file_prefix="trmm", calc=False):
    try:
        file_input_month = output_folder + file_prefix + "_" + month +"_" + year + ".tif"
        file_input_avg = output_folder  + "avg/" + file_prefix + "_" +  month +"_avg.tif"

        file_output = output_folder + "da/" + file_prefix + "_" +  month + "_" + year + "_da.tif"

        file_output_processed = output_folder + "output/" + file_prefix + "_" +  month + "_" + year + "_da.tif"

        files = [file_input_month, file_input_avg]

        if calc:
            if os.path.isfile(file_input_month) and os.path.isfile(file_input_avg):
                try:
                    calc_layers(files, file_output, "ratio")
                except Exception, e:
                    log.error(e)
                    pass

                process_layers(file_output, file_output_processed)

            # TODO: reprojection

    except Exception, e:
        log.error(e)


def publish_layers():
    files = glob.glob(output_folder + "output/*.tif")

    for f in files:
        log.info("--------------------------------")

        name = get_filename(f)

        log.info("name %s %s" %(name, f))

        month = int(name[5:7])

        log.info("month %s" % month)
        year = None
        try:
            year = int(name[8:12])
        except Exception, e:
            log.error("year error")

        # TODO: what year for the DA?
        if year is None:
            year = "2014"

        # get title name
        title = name.replace("_", " ").capitalize()

        # get metadata
        from_date, to_date = get_range_dates_metadata(month, year)
        creationDate = calendar.timegm(datetime.datetime.now().timetuple())

        # Sample of Metadata json
        log.info("Creating metadata")
        metadata_def = {}
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
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "TRMM"}]
        metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "TRMM"}]

        # TODO: in theory should be the original file the onlineResource
        metadata_def["meAccessibility"] = {}
        metadata_def["meAccessibility"]["seDistribution"] = {}
        metadata_def["meAccessibility"]["seDistribution"]["onlineResource"] = f

        # TODO: added new field for the original resource (should we have two different metadata?)
        #metadata_def["meAccessibility"]["seDistribution"]["originalResource"] = output_filename

        # adding type of layer
        aggregationProcessing = "none"
        if "_avg" in name:
            aggregationProcessing = "avg"
        elif "_da" in name:
            aggregationProcessing = "da"
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

        # publish layer
        print manager.publish_coverage(f, metadata_def)



# Parameters
years = ['2012', '2013', '2014']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
product = '3B42RT'
file_prefix ="trmm"

# calculating sum
# for year in years:
#     for month in months:
#         calc_trmm_monthly(year, month, file_prefix, True)
#
#
# for month in months:
#     calc_trmm_avg_monthly(month, file_prefix, True)

# for month in months:
#     calc_trmm_avg_monthly(month, file_prefix, True)
#
#
# for year in years:
#     for month in months:
#         calc_trmm_da_monthly(year, month, file_prefix, True)


publish_layers()

