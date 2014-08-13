from pgeo.gis.gdal_calc import calc_layers


def calc_trmm_monthly(year, month):
    try:
        files_path = "/home/vortex/Desktop/LAYERS/TRMM/" + year+ "/" + month + "/*.tif"
        print files_path
        outputfile = "/home/vortex/Desktop/LAYERS/TRMM/monthly/trmm_"+ month +"_"+ year +".tif"
        print outputfile
        calc_layers(files_path, outputfile, "sum")
    except Exception, e:
        print e
        pass

# Parameters
years = ['2012', '2013', '2014']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
product = '3B42RT'

for year in years:
    for month in months:
        calc_trmm_monthly(year, month)

