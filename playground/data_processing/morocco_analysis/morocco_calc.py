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
            output_filename = output_folder + "/wheat_" + get_filename(input_file) + ".tif"
            #gdal_calc.py -A wheat_seasonal_act_biomprod_doukkala_mask.tif -B asd --outfile=processed.tif --calc="B*A" --NoDataValue=0
            cmd = 'gdal_calc.py -A ' + input_file + ' -B ' + mask_file + ' --outfile=' + output_filename + ' --calc="B*A" --NoDataValue=0'
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()

    except Exception, e:
        print e
        pass


input_folder = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/original_unsorted/output/Monthly_Results_Doukkala_30m/"
output_folder = input_folder + "masked"
mask_file = "/home/vortex/Desktop/LAYERS/MOROCCO_MICHELA/original_unsorted/wheat_mask.tif"

process(input_folder, output_folder, mask_file)
