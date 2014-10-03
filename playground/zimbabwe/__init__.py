import os


cmd = ''
cmd = 'gdalwarp -cutline '
cmd += '/home/kalimaha/Development/GIS/GAUL_2014/4326/zimbabwe/zimbabwe.shp '
cmd += '/home/kalimaha/Desktop/MODIS/MOD13A2/2013/001/OUTPUT_NDVI/final.tiff '
cmd += '/home/kalimaha/Desktop/MODIS/MOD13A2/2013/001/OUTPUT_NDVI/zimbabwe.tiff '
cmd += '-dstnodata -3000'

# os.system(cmd)

home = '/home/kalimaha/Desktop/MODIS/MOD13A2/'
buffer = []
for year in os.listdir(home):
    year_dir = os.path.join(home, year)
    for day in os.listdir(year_dir):
        day_dir = os.path.join(year_dir, day)
        for hdf in os.listdir(day_dir):
            hdf_dir = os.path.join(day_dir, hdf)
            try:
                for tiff in os.listdir(hdf_dir):
                    tiff_dir = os.path.join(hdf_dir, tiff)
                    if 'final.tiff' in tiff_dir:
                        out_file = '/home/kalimaha/Development/GIS/ZIMBABWE_NDVI/' + year + '_' + day + '.tiff '
                        if out_file not in buffer:
                            buffer.append(out_file)
                            cmd = ''
                            cmd += 'gdalwarp -cutline '
                            cmd += '/home/kalimaha/Development/GIS/GAUL_2014/4326/zimbabwe/zimbabwe.shp '
                            cmd += tiff_dir + ' '
                            cmd += out_file
                            cmd += '-dstnodata -3000'
                            print cmd
                            print
                            print
                            os.system(cmd)
                            # print tiff_dir
                            # print '/home/kalimaha/Development/GIS/ZIMBABWE_NDVI/' + year + '_' + day + '.tiff '
                            # print
            except:
                pass