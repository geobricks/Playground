import csv
import json


def convert():
    with open('MODIS_GAUL.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        current = '102'
        hs = []
        vs = []
        out = []
        for row in spamreader:
            h = row[len(row) - 2]
            v = row[len(row) - 1]
            c = row[0]
            l = row[1]
            hs.append(h)
            vs.append(v)
            if c in current:
                pass
            else:
                out.append({
                    'to_v': max(vs),
                    'gaul_label': l,
                    'from_v': min(vs),
                    'from_h': min(hs),
                    'gaul_code': c,
                    'to_h': max(hs)
                })
                hs = []
                vs = []
                current = c
    json.dump(out, open('__gaul2modis.json', 'w'))

convert()