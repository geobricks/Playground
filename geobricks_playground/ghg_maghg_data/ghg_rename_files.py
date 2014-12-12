import os
import glob
import ntpath
from geobricks_processing.core.processing_core import process_data

files = glob.glob("/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MAGHG-data/OUTPUT/*.tif")

output_path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MAGHG-data/OUTPUT/"

process_obj = [
    {
        # "output_path": output_path + "/gdal_translate",
        # "output_file_name": "MOD13A2_3857.tif",
        "process": [
            {
                "gdal_translate": {
                    "opt": {
                        "-co": "'TILED=YES'",
                        "-co": "'COMPRESS=DEFLATE'",
                        "-a_nodata": 0
                    }
                }
            }
        ]
    },
    {
        "process": [
            {
                "gdaladdo": {
                    "parameters": {},
                    "overviews_levels": "2 4 8 16"
                }
            }
        ]
    }
]

for f in files:
    folder, filename = os.path.split(f)
    print f
    # process_obj[0]["source_path"] = [f]
    # process_obj[0]["output_path"] = output_path
    # process_obj[0]["output_file_name"] = filename
    # process_data(process_obj)

    # print f

    if "_GFED4BA_" in f:
        renamed_file = f.replace("_GFED4BA_", "_")
        os.rename(f, renamed_file)
    if "_GFED4_" in f:
        renamed_file = f.replace("_GFED4_", "_")
        print f, renamed_file
        os.rename(f, renamed_file)


