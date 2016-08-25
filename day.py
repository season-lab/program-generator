import time
import calendar
from abstract_time import AbstractTime

class Day(AbstractTime):

    def __init__(self, string_day):
        timestamp = AbstractTime.get_timestamp_from_date(string_day)
        super(Day, self).__init__(string_day, timestamp)