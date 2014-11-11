from pgeo.gis import processing
import glob
from pgeo.utils.filesystem import get_filename


objs = [
    {
        "band": 1,
        "output_file_name": "_3857",
        "process": [
            {
                "gdalwarp": {
                    "opt": {
                        "-multi": "",
                        "-overwrite": "",
                        "-of": "GTiff",
                        "-s_srs": "EPSG:4326",
                        "-t_srs": "EPSG:3857",
                        "-co": "'TILED=YES'",
                        # "-tr": "463.3127165, -463.3127165",
                        # "-te": "-20037507.07 -30240971.96 20037507.07 18422214.74",
                        #"-co": "'BIGTIFF=YES'",
                        "-srcnodata": "255",
                        "-dstnodata": "255"
                    },
                    "prefix": "gdalwarp_",
                    "extension": "tif"
                }


            }
        ]
    },
    {
        "band": 1,
        "process": [
            {
                "gdaladdo": {
                    "parameters": {
                        # "--config": "BIGTIFF_OVERVIEW IF_NEEDED"
                    },
                    "overviews_levels": "2 4 8 16"
                }
            }
        ]
    }
]



def process_step(obj):
    output_files = processing.process(obj)
    return output_files

# gdalwarp  -co 'TILED=YES' -s_srs '+proj=sinu +R=6371007.181 +nadgrids=@null +wktext' -srcnodata 255 -overwrite  -t_srs EPSG:3857 -tr '0.004166665 -0.004166665' -multi  -of GTiff -dstnodata -3000 /home/alargos/Desktop/MODIS/MCD12Q1/2001/001/processed/merge.hdf /home/alargos/Desktop/MODIS/MCD12Q1/2001/001/processed/final_pixel.tiff


def process_landcover():
    path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/GFED4_BURNEDAREAS_BY_LANDCOVER/"
    input_dir = glob.glob(path + "*")
    print input_dir
    for d in input_dir:
        input_files = glob.glob(d + "/*.tif")
        for input_file in input_files:
            print d
            print input_file
            filename = get_filename(input_file)
            source_path = [input_file]
            print filename
            output_path = d + "/"
            output_file_name = filename + "_3857"
            print output_path
            for obj in objs:
                obj["source_path"] = source_path
                obj["output_path"] = output_path
                obj["output_file_name"] = output_file_name
                print obj
                source_path = process_step(obj)


def remove_layers():
    path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/GFED4_BURNEDAREAS_BY_LANDCOVER/"
    input_dir = glob.glob(path + "*")
    for d in input_dir:
        input_files = glob.glob(d + "/*.tif")
        for input_file in input_files:
            if "tif.tiff" in input_file:
                print input_file




process_landcover()
#remove_layers()
