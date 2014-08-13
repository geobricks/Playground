import subprocess

# default options
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

def process_layers(input_path, output_file, parameters=process_layer_parameters):
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
