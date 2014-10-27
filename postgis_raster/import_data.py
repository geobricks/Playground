import subprocess
import glob
import os
from pgeo.utils.filesystem import get_filename
#raster2pgsql -d -I -s EPSG:3857 -M -F -t 500x500 NDVI_2014129_SADC.tif ndvi_tiled_500_500 | psql -U fenix -d pgeo

def import_data_earthstat(input_folder):
    dir = glob.glob(input_folder + "*")
    for d in dir:
        if os.path.isdir(d):
            input_files = glob.glob(d + "/*.tif")
            for input_file in input_files:
                import_data(input_file, "es10_10", get_filename(input_file))




def import_data(filpath, schema, tablename):
    tile_size = "20x20"
    projection = "EPSG:4326"
    #filpath = "/home/vortex/Desktop/LAYERS/earthstat/175CropsYieldArea_geotiff/abaca/abacaarea.tif"
    #tablename = "abacaarea_500_500"
    tablename = schema + "." + tablename


    args_p1 = [
        'raster2pgsql',
        '-d', # drop table
        '-I', # create index on table
        '-M',
        '-F',
        '-t',
        tile_size,
        '-s',
        projection,
        filpath,
        tablename
    ]

    args_p2 = [
        "psql",
        "-U"
        "fenix",
        "pgeo"
    ]

    try:
        print args_p1
        print args_p2

        p1 = subprocess.Popen(args_p1, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(args_p2, stdin=p1.stdout, stdout=subprocess.PIPE)
        stdout_value = p2.communicate()[0]
    except:
        stdout_value = p2.communicate()[0]
        print stdout_value



def clip_one_raster_by_another(request):
    print "map algebra example"
    #
    # # Our raw SQL query, with parameter strings
    # query_string = '''
    # SELECT ST_AsGDALRaster(ST_Clip(landcover.rast,
    #     ST_Buffer(ST_Envelope(burnedarea.rast), %s)), %s) AS rast
    #   FROM landcover, burnedarea
    #  WHERE ST_Intersects(landcover.rast, burnedarea.rast)
    #    AND burnedarea.rid = %s'''
    #
    # # Create a RasterQuery instance; apply the parameters
    # query = RasterQuery(query_string)
    # query.execute([1000, 'GTiff', 2])
    #
    # filename = 'blah.tiff'
    #
    # # Outputs:
    # # [(<read-only buffer for 0x2613470, size 110173, offset 0 at 0x26a05b0>),
    # #  (<read-only buffer for 0x26134b0, size 142794, offset 0 at 0x26a01f0>)]
    #
    # # Return only the first item
    # response = HttpResponse(query.fetch_all()[0], content_type=FORMATS[_format]['mime'])
    # response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    # return response



# input_folder = "/home/vortex/Desktop/LAYERS/earthstat/175CropsYieldArea_geotiff/*"
# import_data_earthstat(input_folder)