import csv
import json


def convert():

    with open('MODIS_GAUL.csv', 'rb') as csvfile:

        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        current = '102'
        out = []

        buffer = []
        buffers = {}
        for row in spamreader:
            if row[0] == current:
                buffer.append(row)
            else:
                current = row[0]
                buffer = []
                buffer.append(row)
            buffers[row[1]] = buffer

        for key in buffers:
            hs = []
            vs = []
            gaul_code = None
            for buffer in buffers[key]:
                hs.append(int(buffer[3]))
                vs.append(int(buffer[4]))
                gaul_code = buffer[0]
            tmp = {
                "to_v": max(vs),
                "gaul_label": key,
                "gaul_code": gaul_code,
                "from_v": min(vs),
                "from_h": min(hs),
                "to_h": max(hs)
            }
            out.append(tmp)

    json.dump(out, open('__gaul2modis.json', 'w'))
    print 'Done'

convert()