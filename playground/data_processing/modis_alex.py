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
from pgeo.utils.filesystem import get_filename, remove
from pgeo.utils.date import day_of_the_year_to_date


# TODO: remove all metadata trmm layers on mongo
# db.layer.remove( { uid: { $regex: 'trmm_*', $options: 'i' } } );


log = logger("playground.data_processing.trmm")

input_folder = "/home/vortex/Desktop/LAYERS/MODIS_NDVI_SADC/*"
output_folder = ""

manager = Manager(settings)


# def dt2unix(dt):
#     return int(time.mktime(dt.timetuple()) + (dt.microsecond / 10.0 ** 6))


def calc_trmm():

    # take folders
    folders = glob.glob(input_folder)
    for folder in folders:
        print input_folder
        # create output folder /output
        # covert to geotiff 3857 the file
        output_folder = folder + "/output"
        if os.path.isdir(output_folder):
            remove(output_folder + "/*.tif")
        else:
            os.mkdir(output_folder)


        input_files = glob.glob(folder +"/*.tif")
        for input_file in input_files:

            output_filename = output_folder + "/" + get_filename(input_file) + ".tif"
            print(output_filename)
            # create a geotiff + overviews
            process_layers(input_file, output_filename)


def publish():
    folders = glob.glob(input_folder)

    for folder in folders:
        files = glob.glob(folder +"/output/*.tif")

        for f in files:
            if "Average" in f:
                print "Average"
                log.info("--------------------------------")
                log.info(f)

                name = get_filename(f)
                to_day = name[name.index("_")+1:name.rindex("_")]
                year = 1990
                print d
                print year
                from_day = int(to_day) - 15
                print from_day

                from_date = calendar.timegm(day_of_the_year_to_date(to_day, year).timetuple())
                to_date = calendar.timegm(day_of_the_year_to_date(from_day, year).timetuple())

                #title = name.replace("", " ").upper()

                title = "NDVI SADC Avg - " + to_day

            else:
                log.info("--------------------------------")
                log.info(f)

                name = get_filename(f)

                d = name[name.index("_")+1:name.rindex("_")]
                year = d[0:4]
                to_day = d[4:]
                print d
                print year
                print to_day
                from_day = int(to_day) - 15
                print from_day

                fromdate = day_of_the_year_to_date(to_day, year)
                todate = day_of_the_year_to_date(from_day, year)

                from_date = calendar.timegm(fromdate.timetuple())
                to_date = calendar.timegm(todate.timetuple())

                print from_date
                print to_date

                # get title name
                #title = name.replace("_", " ").capitalize()
                if "Anomaly" in f:
                    title = "NDVI SADC Anomaly - " + str(fromdate)
                else:
                    title = "NDVI SADC - " + str(fromdate)



            # get metadata
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
            metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "MODIS-NDVI-SADC"}]
            metadata_def["meContent"]["seCoverage"]["coverageSector"]["codes"] = [{"code" : "MODIS-NDVI-SADC"}]

            # TODO: in theory should be the original file the onlineResource
            metadata_def["meAccessibility"] = {}
            metadata_def["meAccessibility"]["seDistribution"] = {}
            metadata_def["meAccessibility"]["seDistribution"]["onlineResource"] = f

            # TODO: added new field for the original resource (should we have two different metadata?)
            #metadata_def["meAccessibility"]["seDistribution"]["originalResource"] = output_filename

            # adding type of layer
            aggregationProcessing = "none"
            if "Anomaly" in f:
                aggregationProcessing = "anomaly"
            elif "Average" in f:
                aggregationProcessing = "avg"
            metadata_def["meStatisticalProcessing"] = {}
            metadata_def["meStatisticalProcessing"]["seDatasource"] = {}
            metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"] = {}
            metadata_def["meStatisticalProcessing"]["seDatasource"]["seDataCompilation"]["aggregationProcessing"] = aggregationProcessing;

            # default style
            metadata_def["meSpatialRepresentation"] = {}
            metadata_def["meSpatialRepresentation"]["seDefaultStyle"] = {}
            if aggregationProcessing == "anomaly":
                metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "ndvi_" + aggregationProcessing
            else:
                metadata_def["meSpatialRepresentation"]["seDefaultStyle"]["name"] = "ndvi"


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


#calc_trmm()

publish()
