import os
import os, stat, psycopg2
import subprocess
# See: http://www.pygresql.org/install.html
# pip install psycopg2, pygresql

# Designate path to output file
outfile = '/tmp/temp23.tiff'

# Name of PostgreSQL table to export
pg_table = 'es.banana_area1'
#pg_table = 'es.export_test'

# PostgreSQL connection parameters
pg_server = 'localhost'
pg_database = 'pgeo'
pg_user = 'fenix'
pg_password = 'Qwaszx'

# Desginate a file to receive the hex data; make sure it exists with the right permissions
pg_hex = '/tmp/temp23.hex'
#os.chmod(pg_hex, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
subprocess.call(['chmod', '777', pg_hex ])


conn_string = "host='localhost' dbname='pgeo' user='fenix' password='Qwaszx'"

conn = psycopg2.connect(conn_string)
#sql = "COPY (SELECT encode(ST_AsTIFF(ST_Union(" + pg_table + ".rast)), 'hex') FROM " + pg_table + ") TO '" + pg_hex + "'"

query = "SELECT encode(ST_AsTIFF(ST_Union(" + pg_table + ".rast)), 'hex') FROM " + pg_table
#
# query2 = "SELECT encode(ST_AsTIFF(ST_Union(" + pg_table + ".rast)), 'hex') FROM " + pg_table
#
# query2 = "SELECT encode(ST_AsTIFF(ST_MapAlgebraExpr(a.rast, 4, b.rast, 3, '(rast1 - rast2) /(rast1 + rast2)::float')) FROM es.banana_area1 a, es.wheat_area1 b, spatial.gaul0_2013_4326 where adm0_name = 'Nigeria' and st_intersects(a.rast,geom) and st_intersects(b.rast,geom)), 'hex')"

sql = "COPY ("+ query +") TO '" + pg_hex + "'"

print sql



cursor = conn.cursor()
# execute our Query
cursor.execute(sql)

# retrieve the records from the database
#records = cursor.fetchall()

cmd = 'xxd -p -r ' + pg_hex + ' > ' + outfile
os.system(cmd)

#
# class RasterQuery:
#     '''
#     Assumes some global FORMATS dictionary describes the valid file formats, their file extensions and MIME type strings.
#     '''
#     def __init__(self, qs, params=None, file_format='geotiff'):
#         assert file_format in FORMATS.keys(), 'Not a valid file format'
#
#         self.cursor = connection.cursor()
#         self.params = params
#         self.query_string = qs
#         self.file_format = file_format
#         self.file_extension = FORMATS[file_format]['file_extension']
#
#     def execute(self, params=None):
#         '''Execute the stored query string with the given parameters'''
#         self.params = params
#
#         if self.params is not None:
#             self.cursor.execute(self.query_string, params)
#
#         else:
#             self.cursor.execute(self.query_string)
#
#     def fetch_all(self):
#         '''Return all results in a List; a List of buffers is returned'''
#         return [
#             row[0] for row in self.cursor.fetchall()
#         ]
#
#     def write_all(self, path, name=None):
#         '''For each raster in the query, writes it to a file on the given path'''
#         name = name or 'raster_query'
#
#         i = 0
#         results = self.fetch_all()
#         for each in results:
#             name = name + str(i + 1) + self.file_extension
#             with open(os.path.join(path, name), 'wb') as stream:
#                 stream.write(results[i])
#
#             i += 1

def clip_one_raster_by_another(request):

    # Our raw SQL query, with parameter strings
    query_string = '''
    SELECT ST_AsGDALRaster(ST_Clip(landcover.rast,
        ST_Buffer(ST_Envelope(burnedarea.rast), %s)), %s) AS rast
      FROM landcover, burnedarea
     WHERE ST_Intersects(landcover.rast, burnedarea.rast)
       AND burnedarea.rid = %s'''

    # Create a RasterQuery instance; apply the parameters
    query = RasterQuery(query_string)
    query.execute([1000, 'GTiff', 2])

    filename = 'blah.tiff'

    # Outputs:
    # [(<read-only buffer for 0x2613470, size 110173, offset 0 at 0x26a05b0>),
    #  (<read-only buffer for 0x26134b0, size 142794, offset 0 at 0x26a01f0>)]

    # Return only the first item
    response = HttpResponse(query.fetch_all()[0], content_type=FORMATS[_format]['mime'])
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response

# f = open(param_filepath, 'wb')
# chmod_oct = int(chmod,8) # new addition (converts chmod octal code to associated integer value)
# os.chmod(param_filepath,chmod_oct) # new addition (changes read/write permissions)
# f.write(param_bytes)
# f.close()