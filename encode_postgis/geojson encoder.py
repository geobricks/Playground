from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
from sys import stdin, stdout
from json import loads, dumps, JSONEncoder
from optparse import OptionParser
from re import compile
import encode_postgis
float_pat = compile(r'^-?\d+\.\d+(e-?\d+)?$')
charfloat_pat = compile(r'^[\[,\,]-?\d+\.\d+(e-?\d+)?$')

#input = { "type": "FeatureCollection","features": [{ "type": "Feature",                  "geometry": {                      "type": "Polygon",                      "coordinates": [                          [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],                            [100.0, 1.0], [100.0, 0.0] ]                      ]                  },                  "properties": {                      "prop0": "value0",                      "prop1": {"this": "that"}                  }                }            ]}
input = { "type": "FeatureCollection",            "features": [                { "type": "Feature",                  "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},                 "properties": {"prop0": "value0"}                },                { "type": "Feature",                  "geometry": {                      "type": "LineString",                      "coordinates": [                          [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]                      ]                  },                  "properties": {                      "prop0": "value0",                      "prop1": 0.0                  }                },                { "type": "Feature",                  "geometry": {                      "type": "Polygon",                      "coordinates": [                          [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],                            [100.0, 1.0], [100.0, 0.0] ]                      ]                  },                  "properties": {                      "prop0": "value0",                      "prop1": {"this": "that"}                  }                }            ]}
data = dumps(input)
print data
#data = loads(data)
#print data
#
# Write!
#
encoder = JSONEncoder(separators=(',', ':'))
encoded = encoder.iterencode(input)

# format = '%.' + str(options.precision) + 'f'
# output = len(args) == 2 and open(args[1], 'w') or stdout
prev_lat = 0
prev_lng = 0
out = ""
char_lat = True

# p = ""
# for feature in input['features']:
#     print feature['geometry']['type']
#     print feature['geometry']['coordinates']
#     print encode_postgis._encode_geometry(feature['geometry'])
#     feature['geometry']['coordinates'] = encode_postgis._encode_geometry(feature['geometry'])


def query_geojson():
    db_settings = {}
    db_settings["dbname"] = "fenix"
    db_settings["password"] = "Qwaszx"
    db_settings["username"] = "fenix"
    db = DBMSPostgreSQL(db_settings)

    #r = db.query("select ST_AsGeoJSON(geom), iso2, faost_n from gaul0_4326 where continent IN ('Asia')")
    #r = db.query("select ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.08)), iso2, faost_n from gaul0_4326 where continent IN ('Asia')")
    #r = db.query("select ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.04)), adm1_code, adm1_name from gaul1_2015_4326 where adm0_name IN ('Russian Federation')")
    r = db.query("select ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.04)), adm0_code, adm0_name from gaul0_2015_4326 where adm0_name IN ('Russian Federation')")
    #r = db.query("select ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.04)), adm0_code, adm0_name from gaul0_2015_4326")


    #r = db.query("select ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.04)), adm1_code, adm1_name, ST_Area(geom) from gaul2_2015_4326 where adm0_name IN ('Malta') and ST_Area(geom) > 0.0009")

    #r = db.query("select ST_AsGeoJSON(geom), iso2, faost_n from gaul0_4326 where continent NOT IN ('Antartica')")
    #r = db.query("select ST_AsGeoJSON(geom), iso2, faost_n from gaul0_4326 where faost_n IN ('Malta','Italy')")
    #geojson = {"type": "FeatureCollection", "features": []}

    print "doing geojson"
    out_file = open("html/data/asia.geojson", "wb")
    out_file.write('{"type":"FeatureCollection","features":[')
    index = 0
    for v in r:

        j = loads(v[0])
        f = {}
        f["type"] = "Feature"
        f["geometry"] = {}
        f["geometry"]["type"] = j["type"]
        f["geometry"]["coordinates"] = encode_postgis._encode_geometry(j)
        f["properties"] = {"iso2": v[1], "name": v[2]}
        out_file.write(dumps(f))
        # properties
        #out_file.write("," + dumps({"properties": {"iso2": v[1], "name": v[2]}}));
        #geojson["features"].append({"geometry": f})
        if index < len(r) -1:
            out_file.write(",")
        index += 1

    out_file.write(']}')
    out_file.close()

# load geojson
query_geojson()

#print input
# for token in encoded:
#     if charfloat_pat.match(token):
#         # in python 2.7, we see a character followed by a float literal
#         # output.write(token[0] + format % float(token[1:]))
#         #print token[0], float(token[1:])
#         # out += str(token[0])
#         # out += str(float(token[1:]))
#         # print token[1:]
#         val = int(float(token[1:]) * 1e5)
#         if char_lat:
#             v = _encode_value(val - prev_lat)
#             prev_lat = val
#             char_lat = False
#         else:
#             v = _encode_value(val - prev_lng)
#             prev_lng = val
#             char_lat = True
#
#         print v
#         out += str(token[0])
#         out += str(v)
#         #lat, lng = int(coord[1] * 1e5), int(coord[0] * 1e5)
#         # lat, lng = int(float(token[1:]) * 1e5), int(float(token[1:]) * 1e5)
#         #
#         # d_lat = _encode_value(lat - prev_lat)
#         # d_lng = _encode_value(lng - prev_lng)
#         #
#         # prev_lat, prev_lng = lat, lng
#         #
#         # out += str(token[0])
#         # out += str(int(float(token[1:]) * 1e5))
#
#     elif float_pat.match(token):
#         print "|", float(token)
#         out += str(float(token))
#         # in python 2.6, we see a simple float literal
#         #output.write(format % float(token))
#
#     else:
#         out += token
#         #print "-->", token
        #output.write(token)




print out