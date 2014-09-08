from pgeo.dataproviders import trmm2 as t
from pgeo.utils import log
from pgeo.thread.bulk_download_threads_manager import BulkDownloadManager

log = log.logger(__name__)

year = '2000'
month = '03'
from_day = 1
to_day   = 31
days = map(lambda x: str(x) if x > 9 else '0'+str(x), range(int(from_day), 1+int(to_day)))
# log.info(days)

# log.info('Get file-names for ' + year + '/' + month)

# for day in days:

file_list = t.list_layers_subset(year, month, from_day, to_day)

filesystem_structure = {
    'product': '3B42',
    'year': year,
    'month': month,
    'day': str(from_day) + '-' + str(to_day)
}

bulk_download_objects = []
for day in days:
    bdo = {
        'ftp_base_url': 'trmmopen.gsfc.nasa.gov',
        'ftp_data_dir': '/trmmdata/GIS/' + year + '/' + month + '/' + day + '/',
        'file_list': file_list,
        'filesystem_structure': {
            'product': '3B42',
            'year': year,
            'month': month,
            'day': day
        }
    }
    bulk_download_objects.append(bdo)

tab_id = 'tab_0'
mgr = BulkDownloadManager('trmm2', None, bulk_download_objects, tab_id)
target_dir = mgr.run()