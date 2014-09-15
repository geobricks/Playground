import glob
import string
import random


cmd = 'scripts/gdal_calculations.py '


files = glob.glob("/home/vortex/Desktop/LAYERS/TRMM/03/*.tif")
outputfile = "/home/vortex/Desktop/result_last_new.tif"


print files
def random_char(y):

    return ''.join(random.choice(string.ascii_letters) for x in range(y)).upper()

cmd = "gdal_calc.py "
file_variables=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V"]
files_numeber=0
for filepath in files:
    print filepath
    try:
        cmd += " -" + file_variables[files_numeber] + " " + filepath + " "
        files_numeber = files_numeber+1
    except:
        pass

cmd += " --outfile=/home/vortex/Desktop/LAYERS/TRMM/03/result_last.tif"
print str(len(file_variables))

cmd += ' --calc="('
for file_variable in file_variables:
    cmd += file_variable
    cmd += "+"
cmd += ')"'
       # '/' + str(len(file_variables)) + '"'



print cmd






