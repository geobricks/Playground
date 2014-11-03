import os
import glob
from pgeo.utils.filesystem import get_filename
import shutil
import subprocess

def process(input_folder, output_folder, mask_file):

    # create the folder
    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    try:
        input_files = glob.glob(input_folder +"/*.tif")
        for input_file in input_files:
            output_filename = output_folder + "/" + get_filename(input_file) + ".tif"
            #gdal_calc.py -A wheat_seasonal_act_biomprod_doukkala_mask.tif -B asd --outfile=processed.tif --calc="B*A" --NoDataValue=0
            #gdal_calc.py -A ndvi_mask.tif -B  --outfile=result.tif --calc="B*(A>0)" --NoDataValue=-3000
            cmd = 'gdal_calc.py -A ' + input_file + ' -B ' + mask_file + ' --outfile=' + output_filename + ' --calc="B*A" --NoDataValue=-3000'
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            print output
            print error

    except Exception, e:
        print e
        pass


input_folder = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/evapotranspiration/ETRef/clipped/"
output_folder = input_folder + "masked"
mask_file = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/to_publish/3857/meteo/ndvi/ndvi_mask.geotiff"

process(input_folder, output_folder, mask_file)