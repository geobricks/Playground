import subprocess
from pgeo.utils import filesystem
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


    gdal_translate_layer = filesystem.create_tmp_filename()
    cmd = "gdal_translate " + input_path + " " + output_file
    print cmd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print output








