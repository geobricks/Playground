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

def create_metadata(title, product, sldname, date, uid_distribution=None, is_raster=True, uid=None):

    # TODO: important this is a new workspace
    #workspace = "morocco"

    creationDate = calendar.timegm(datetime.datetime.now().timetuple())

    # get metadata
    if date is not None:
        year = int(date[:4])
        month = int(date[4:])
        from_date, to_date = get_range_dates_metadata(month, year)

    # get title name
    #title = name + " " + sldname + " " + area + " " + str(month) + "-" + str(year)

    #product = "MOROCCO-" + name.upper()

    # Sample of Metadata json
    metadata_def = {}
    if uid is not None:
        metadata_def["uid"] = uid

    metadata_def["meSpatialRepresentation"] = {}
    #metadata_def["meSpatialRepresentation"]["workspace"] = workspace


    metadata_def["title"] = {}
    metadata_def["title"]["EN"] = title
    metadata_def["creationDate"] = creationDate

    metadata_def["meContent"] = {}
    metadata_def["meContent"]["seCoverage"] = {}
    metadata_def["meContent"]["seCoverage"]["coverageTime"] = {}
    if date is not None:
        metadata_def["meContent"]["seCoverage"]["coverageTime"]["from"] = from_date
    if date is not None:
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

    if is_raster is False:
        metadata_def["meSpatialRepresentation"]["layerType"] = "vector"
        metadata_def["meSpatialRepresentation"]["seVectorSpatialRepresentation"] = {}
        metadata_def["meSpatialRepresentation"]["seVectorSpatialRepresentation"]["geometricObjects"] = "polygon"
    else:
        metadata_def["meSpatialRepresentation"]["layerType"] = "raster"
    return metadata_def


def get_range_dates_metadata(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    from_date = datetime.datetime(int(year), int(month), 1)
    to_date = datetime.datetime(int(year), int(month), last_day)
    return calendar.timegm(from_date.timetuple()), calendar.timegm(to_date.timetuple())


def publish_data_GriddedLivestock(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    product = "Gridded Livestock of the World v. 2.01"
    sldname = "ghg_"
    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        title = info[0].capitalize() + " " + info[1] + " - " + info[2]
        sldname += get_filename(input_file).lower()
        date = info[2] + "01"
        metadata_def = create_metadata(title, product, sldname, date, None)
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def, False, False)


def publish_data_Climate_Zones_processed(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    product = "JRC climate zone"
    sldname = "ghg_jrc_climate_zone_0.25deg"
    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        title = info[0] + " " + info[1].lower() + " - " + info[2].lower()
        if "4326" in info[4]:
            title += " (4326)"
            product += " (4326)"
        date = None
        metadata_def = create_metadata(title, product, sldname, date, None)
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def, False, False)


def publish_data_modis_landcover(input_folder):
    input_files = glob.glob(input_folder +"/*.tif")
    product = "MODIS - Land Cover Type UMD"
    sldname = "modis_land_cover"
    for input_file in input_files:
        info = str.split(get_filename(input_file), "_")
        title = info[0] + " " + info[1] + " " + info[2] + " " + info[3] + " " + info[4] + " " + info[5] + " - " + info[6]
        if "4326" in info[4]:
            title += " (4326)"
            product += " (4326)"
        date = info[6] + info[7]
        metadata_def = create_metadata(title, product, sldname, date, None)
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def, False, False)


def publish_burnerdareas():
    path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/GFED4_BURNEDAREAS_BY_LANDCOVER/"
    input_dir = glob.glob(path + "*")
    for d in input_dir:
        input_files = glob.glob(d + "/*.tiff")

        # sld and workspace
        sldname = "ghg_burnedareas"
        workspace = "fenix:"

        for input_file in input_files:
            #print input_file
            if "3857" in input_file:
                if "humid" in input_file.lower() or "allforests" in input_file.lower():
                    print input_file
                    info = str.split(get_filename(input_file), "_")
                    date = info[3] + '01'
                    filename = get_filename(input_file).rsplit('_', 1)[0]
                    uid = workspace + get_filename(filename).lower()
                    product = burned_areas_switch(filename)
                    title = product + " " + info[3]
                    metadata_def = create_metadata(title, product, sldname, date, None, False, uid)
                    print metadata_def
                    #manager.publish_coverage(input_file, metadata_def, False, False)
                else:
                    info = str.split(get_filename(input_file), "_")
                    date = info[4] + '01'
                    filename = get_filename(input_file).rsplit('_', 1)[0]
                    uid = workspace + get_filename(filename).lower()
                    product = burned_areas_switch(input_file)
                    title = product + " " + info[4]
                    metadata_def = create_metadata(title, product, sldname, date, None, False, uid)
                    print metadata_def
                    #manager.publish_coverage(input_file, metadata_def, False, False)
            else: #4326
                info = str.split(get_filename(input_file), "_")
                if len(info) >= 5:
                    title = info[0] + " " + info[1] + " " + info[2] + " " + info[3] + " " + info[4] + " - 4326"
                    date = info[4] + '01'
                else:
                    title = info[0] + " " + info[1] + " " + info[2] + " " + info[3]
                    date = info[3] + '01'
                product = get_filename(input_file).replace('_', ' ') + " (4326)"
                metadata_def = create_metadata(title, product, sldname, date, None)
                print metadata_def


def burned_areas_switch(filename):
    filename = filename.lower()
    if "peatlands" in filename:
        return "GFED4 Burned Areas - Organic soils"
    if "AllForestsMinus".lower() in filename:
        return "GFED4 Burned Areas - Other forest"
    if "humidtropicalforests".lower() in filename:
        return "GFED4 Burned Areas - Humid Tropical Forest"

    burned_areas_lc = "GFED4 Burned Areas - "
    if "lc_1_" in filename:
        return burned_areas_lc + "Evergreen Needleleaf forest"
    if "lc_2_" in filename:
        return burned_areas_lc + "Evergreen Broadleaf forest"
    if "lc_3_" in filename:
        return burned_areas_lc + "Deciduous Needleleaf forest"
    if "lc_4_" in filename:
        return burned_areas_lc + "Deciduous Broadleaf forest"
    if "lc_5_" in filename:
        return burned_areas_lc + "Mixed forest"
    if "lc_6_" in filename:
        return burned_areas_lc + "Closed shrubland"
    if "lc_7_" in filename:
        return burned_areas_lc + "Open shrubland"
    if "lc_8_" in filename:
        return burned_areas_lc + "Woody savanna"
    if "lc_9_" in filename:
        return burned_areas_lc + "Savanna"
    if "lc_10_" in filename:
        return burned_areas_lc + "Grassland"
    if "lc_12_" in filename:
        return burned_areas_lc + "Croplands"
    if "lc_13_" in filename:
        print filename
        return burned_areas_lc + "Urban and built-up"
    if "lc_16_" in filename:
        return burned_areas_lc + "Barren or sparsely vegetated"
    if "lc_17_" in filename:
        return burned_areas_lc + "Unclassified"


def publish_gez_vector():
    uid = "fenix:gez_2010_3857"
    title = "Global Ecological Zones (GEZ) 2010  - Vector"
    product = "Global Ecological Zones (GEZ) 2010"
    sldname = "ghg_gez_2010"
    date = "201001"
    metadata_def = create_metadata(title, product, sldname, date, None, False, uid)
    print metadata_def
    #manager.publish_shapefile(None, metadata_def, False, False)

def publish_area_of_histosols(path):
    input_files = glob.glob(path + "*.tif")
    for input_file in input_files:
        #info = "Organic soil surface area"
        uid = "fenix:area_of_histosols_2008"
        title = "Organic soil surface area"
        product = "Harmonized World Soil Database - Organic soils"
        sldname = "ghg_area_of_histosols"
        date = '200801'
        metadata_def = create_metadata(title, product, sldname, date, None, False, uid)
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def, False, False)


def publish_gez(path):
    input_files = glob.glob(path + "*.tif")
    for input_file in input_files:
        #info = "Organic soil surface area"
        #uid = "fenix:gez_"
        title = "Global Ecological Zones (GEZ) 2010 - Raster"
        product = "Global Ecological Zones (GEZ) 2010"
        sldname = "ghg_gez_2010_raster"
        date = '201001'
        metadata_def = create_metadata(title, product, sldname, date, None, False)
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def, False, False)


def publish_ghg_glc2000_v1_1(path):
    input_files = glob.glob(path + "*.tif")
    for input_file in input_files:
        #info = "Organic soil surface area"
        #uid = "fenix:gez_"
        title = "Global Land Cover 2000 (GLC2000)"
        product = "Global Land Cover 2000 (GLC2000)"
        sldname = "ghg_glc2000_v1_1"
        date = '200001'
        metadata_def = create_metadata(title, product, sldname, date, None, False)
        print metadata_def
        manager.publish_coverage(input_file, metadata_def, False, False)


def publish_cultivation_organic_soils_croplands(path):
    input_files = glob.glob(path + "*.tif")
    for input_file in input_files:
        #info = "Organic soil surface area"
        #uid = "fenix:gez_"
        title = "Cultivation Organic Soils - Croplands"
        product = "Cultivation Organic Soils"
        sldname = "ghg_cultivation_organic_soils_cropland"
        date = '200001'
        metadata_def = create_metadata(title, product, sldname, date, None, False)
        print metadata_def
        #manager.publish_coverage(input_file, metadata_def, False, False)



# publish_data_GriddedLivestock("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/GriddedLivestock/to_publish_3857/")
# publish_data_Climate_Zones_processed("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/Climate_Zones_processed/to_publish/")
# publish_data_modis_landcover("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MCD12Q1/processed_2009/3857/")
# publish_burnerdareas()
# publish_area_of_histosols("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/HWSD/3857/")
# publish_gez("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/gez_raster/3857/")
# publish_gez_vector()
# publish_ghg_glc2000_v1_1("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/glc2000/3857/")
# publish_cultivation_organic_soils_croplands("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/cultivation_organic_soils/3857/")




#db.layer.remove( {"_id": ObjectId("545baf855c19e12f73d17162")});: c.que per info nel link ul: c.que per info nel link ul: c.que per info nel link ul: c.que per info nel link ultimo (168) quelle per i tot e a ag soils non funztimo (168) quelle per i tot e a ag soils non funztimo (168) quelle per i tot e a ag soils non funztimo (168) quelle per i tot e a ag soils non funz