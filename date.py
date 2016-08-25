import time
import calendar
from abstract_time import AbstractTime

class Date(AbstractTime):

    def __init__(self, string_date):
        timestamp = AbstractTime.get_timestamp_from_date_hour(string_date)
        super(Date, self).__init__(string_date, timestamp)