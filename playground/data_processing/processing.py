import subprocess
from  pgeo.utils import filesystem
from pgeo.gis.raster import get_nodata_value

# default options
process_layer_parameters = {
    "gdalwarp" : {
        "-overwrite" : "",
        "-multi" : "",
        "-of" : "GTiff",
        #"-tr" : "0.00833333, -0.00833333",
        #"-s_srs" :"'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
        "-s_srs" :"EPSG:32629",
        # "-co": "'TILED=YES'",
        "-t_srs": "EPSG:3857",
        # "-srcnodata" : "nodata" ,
        # "-dstnodata" : "nodata" ,
    },
    "gdaladdo" : {
        "parameters" : {
            "-r" : "average"
        },
        "overviews_levels" : "2 4 8 16"
    }
}

def process_layers(input_path, output_file, parameters=process_layer_parameters):

    no_data_value = get_nodata_value(input_path)
    print "NO DATA VALUE %s" % no_data_value
    # parameters["gdalwarp"]["-srcnodata"]  = no_data_value
    # parameters["gdalwarp"]["-dstnodata"]  = 0

    gdal_warp_layer = filesystem.create_tmp_filename()
    cmd = "gdalwarp "
    for key in parameters["gdalwarp"].keys():
        cmd += " " + key + " " + str(parameters["gdalwarp"][key])
    cmd += " " + input_path + " " + output_file
    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output


    # gdal_translate_layer = filesystem.create_tmp_filename()
    # cmd = "gdal_translate -a_nodata none " + gdal_warp_layer + " " + gdal_translate_layer
    # print cmd
    # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # output, error = process.communicate()
    # print output


    cmd = "gdaladdo "
    for key in parameters["gdaladdo"]["parameters"].keys():
        cmd += " " + key + " " + str(parameters["gdaladdo"]["parameters"][key])
    # cmd += " " + gdal_translate_layer
    cmd += " " + output_file
    cmd += " " + parameters["gdaladdo"]["overviews_levels"]
    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output


    # cmd = "gdal_translate -a_nodata 9e+20 " + gdal_translate_layer + " " + output_file
    # print cmd
    # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # output, error = process.communicate()
    # print output






