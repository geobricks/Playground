from pgeo.gis import processing
import glob

objs = [
    {
        "band": 2,
        "process": [
            {
                "extract_bands": ""
            }
        ]
    },
    {
        "band": 1,
        "output_file_name": "merge",
        "process": [
            {
                "gdal_merge": {
                    "prefix": "gdal_merge_",
                    "extension": "tif",
                    "opt": {
                        "-n": "0"
                    },
                }
            }
        ]
    },
    # {
    #     "band": 1,
    #     "output_file_name": "final_4326",
    #     "process": [
    #         {
    #             "gdalwarp": {
    #                 "opt": {
    #                     "-multi": "",
    #                     "-overwrite": "",
    #                     "-of": "GTiff",
    #                     "-s_srs": "'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
    #                     "-tr": "0.0041666665, -0.0041666665",
    #                     "-co": "'TILED=YES'",
    #                     "-co" : "'BIGTIFF=YES'",
    #                     "-t_srs": "EPSG:4326",
    #                     "-srcnodata": 255,
    #                     "-dstnodata": 255
    #                 },
    #                 "prefix": "gdalwarp_",
    #                 "extension": "tif"
    #             }
    #         }
    #     ]
    # },
    # {
    #     "band": 1,
    #     "output_file_name": "final_pixel4",
    #     "process": [
    #         {
    #             "gdalwarp": {
    #                 "opt": {
    #                     "-multi": "",
    #                     "-overwrite": "",
    #                     "-of": "GTiff",
    #                     "-s_srs": "'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
    #                     "-tr": "5463.3127165, -5463.3127165",
    #                     "-co": "'TILED=YES'",
    #                     # "-co" : "'BIGTIFF=YES'",
    #                     "-t_srs": "EPSG:3857",
    #                     "-srcnodata": "255",
    #                     "-dstnodata": "255"
    #                 },
    #                 "prefix": "gdalwarp_",
    #                 "extension": "tif"
    #             }
    #         }
    #     ]
    # },
    # {
    #     "band": 1,
    #     "output_file_name": "final_3857",
    #     "process": [
    #         {
    #             "gdalwarp": {
    #                 "opt": {
    #                     "-multi": "",
    #                     "-overwrite": "",
    #                     "-of": "GTiff",
    #                     "-s_srs": "EPSG:4326",
    #                     #"-s_srs": "'+proj=sinu +R=6371007.181 +nadgrids=@null +wktext'",
    #                     "-t_srs": "EPSG:3857",
    #                     # "-co": "'TILED=YES'",
    #                     "-tr": "463.3127165, -463.3127165",
    #                     "-te": "-20037507.07 -30240971.96 20037507.07 18422214.74",
    #                     # "-co": "'BIGTIFF=YES'",
    #                     "-srcnodata": "255",
    #                     "-dstnodata": "255"
    #                 },
    #                 "prefix": "gdalwarp_",
    #                 "extension": "tif"
    #             }
    #
    #
    #         }
    #     ]
    # },
    # {
    #     "band": 1,
    #     "output_file_name": "final_3857_deflate",
    #     "process": [
    #         {
    #             "gdal_translate": {
    #                 "opt": {
    #                     "-of": "GTiff",
    #                     "-co": "'TILED=YES'",
    #                     "-co": "'COMPRESS=DEFLATE'"
    #                 },
    #                 "prefix": "gdalwarp_",
    #                 "extension": "tif"
    #             }
    #
    #
    #         }
    #     ]
    # },
    # {
    #     "band": 1,
    #     "process": [
    #         {
    #             "gdaladdo": {
    #                 "parameters": {
    #                     # "--config": "BIGTIFF_OVERVIEW IF_NEEDED"
    #                 },
    #                 "overviews_levels": "2 4 8 16"
    #             }
    #         }
    #     ]
    # }
]



def process_step(obj):
    output_files = processing.process(obj)
    return output_files

# gdalwarp  -co 'TILED=YES' -s_srs '+proj=sinu +R=6371007.181 +nadgrids=@null +wktext' -srcnodata 255 -overwrite  -t_srs EPSG:3857 -tr '0.004166665 -0.004166665' -multi  -of GTiff -dstnodata -3000 /home/alargos/Desktop/MODIS/MCD12Q1/2001/001/processed/merge.hdf /home/alargos/Desktop/MODIS/MCD12Q1/2001/001/processed/final_pixel.tiff


def process_landcover():
    # path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MCD12Q1/*"
    # input_dir = glob.glob(path)
    # for dir in input_dir:
        dir ="/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MCD12Q1/processed_2009/"
        source_path = [dir + "*.hdf"]
        #source_path = [dir + "merge.hdf"]
        #source_path = [dir + "final_3857.tiff"]
        output_path = dir + "test_processing/"
        for obj in objs:
            obj["source_path"] = source_path
            obj["output_path"] = output_path
            source_path = process_step(obj)

    # #source_path = ["/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MOD12Q1/2002/processing/*.hdf"]
    # # source_path = ["/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MOD12Q1/2002/processing/merge.hdf"]
    # source_path = ["/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MOD12Q1/2002/processing/3857/final_pixel4.tiff"]
    # output_path = "/home/vortex/Desktop/LAYERS/GHG_13_NOVEMEBRE/MOD12Q1/2002/processing/3857/"
    # for obj in objs:
    #     obj["source_path"] = source_path
    #     obj["output_path"] = output_path
    #     source_path = process_step(obj)
    #
        print "END!! " + dir



process_landcover()