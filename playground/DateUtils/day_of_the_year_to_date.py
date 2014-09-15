import datetime


def convert(day, year):
    """
    :param day: day of the year
    :type string i.e. "020" or "20"
    :param year: year of reference
    :type string or int i.e. "2014" or 2014
    :return: date of the day/year
    """
    first_of_year = datetime.datetime(int(year), 1, 1).replace(month=1, day=1)
    ordinal = first_of_year.toordinal() - 1 + int(day)
    return datetime.date.fromordinal(ordinal)


print convert("020", 2012)
print convert("20", 2012)