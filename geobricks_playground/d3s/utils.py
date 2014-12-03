import calendar
import datetime


def get_range_dates_metadata_yearmonth(date):
    # TODO: check on date
    if date is not None:
        year = int(date[:4])
        month = int(date[4:])
        return get_range_dates_metadata(month, year)
    return None

def get_range_dates_metadata(month, year):
    last_day = calendar.monthrange(int(year), int(month))[1]
    from_date = datetime.datetime(int(year), int(month), 1)
    to_date = datetime.datetime(int(year), int(month), last_day)
    return calendar.timegm(from_date.timetuple() * 1000), calendar.timegm(to_date.timetuple() * 1000)
