import urllib2
import json
import csv
import os
group = "T"
domains = json.loads(urllib2.urlopen("http://faostat3.fao.org/wds/rest/domains/faostat2/"+ group +"/E").read())
for domain in domains:
    file_name = "elements_" + domain[1].replace(" ", "_").lower()
    file_path = '/home/vortex/Desktop/codes/' + file_name + '.csv'
    if os.path.isfile(file_path):
        os.remove(file_path)
    with open(file_path, 'wb') as csvfile:
        csv_file = csv.writer(csvfile, delimiter=',', quotechar='"')
        values = json.loads(urllib2.urlopen("http://faostat3.fao.org/wds/rest/procedures/usp_GetListBox/faostat2/"+ domain[0] +"/3/1/E").read())
        for value in values:
            try:
                csv_file.writerow([str(value[0]), str(value[1])])
            except Exception:
                print "Exception", Exception


