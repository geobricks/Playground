import csv
import json


def convert():

    with open('MODIS_GAUL.csv', 'rb') as csvfile:

        spam_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        current = '102'
        out = []

        gaul_buffer = []
        buffers = {}
        for row in spam_reader:
            if row[0] == current:
                gaul_buffer.append(row)
            else:
                current = row[0]
                gaul_buffer = [row]
            buffers[row[1]] = gaul_buffer

        for key in buffers:
            hs = []
            vs = []
            gaul_code = None
            for gaul_buffer in buffers[key]:
                hs.append(int(gaul_buffer[3]))
                vs.append(int(gaul_buffer[4]))
                gaul_code = gaul_buffer[0]
                iso2_code = gaul_buffer[8] if len(gaul_buffer[8]) > 0 else None
                iso3_code = gaul_buffer[9] if len(gaul_buffer[9]) > 0 else None
            tmp = {
                "to_v": max(vs),
                "gaul_label": key,
                "gaul_code": gaul_code,
                "iso2_code": iso2_code,
                "iso3_code": iso3_code,
                "from_v": min(vs),
                "from_h": min(hs),
                "to_h": max(hs)
            }
            out.append(tmp)

    json.dump(out, open('__gaul2modis.json', 'w'))
    print 'Done'

convert()