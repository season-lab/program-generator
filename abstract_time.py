import time
import calendar

class AbstractTime(object):

    def __init__(self, string, timestamp):
        self.str = string
        self.timestamp = timestamp

    def __repr__(self):
        return self.str

    def __hash__(self):
        return self.timestamp

    def __cmp__ (self, other):
        assert not isinstance(other, str)
        return self.timestamp.__cmp__(other.timestamp)

    def __sub__(self, other):
        assert not isinstance(other, str)
        return self.timestamp - other.timestamp

    def __eq__(self, other):
        if other is None:
            return False

        assert not isinstance(other, str)
        assert other is not None
        if isinstance(other, int):
            return self.timestamp == other

        return self.timestamp == other.timestamp

    def __neq__(self, other):
        assert not isinstance(other, str)
        assert other is not None
        return self.timestamp != other.timestamp

    def __lt__(self, other):
        assert not isinstance(other, str)
        assert other is not None
        if isinstance(other, int):
            return self.timestamp < other

        return self.timestamp < other.timestamp

    def __le__(self, other):
        assert not isinstance(other, str)
        assert other is not None
        if isinstance(other, int):
            return self.timestamp <= other

        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        assert not isinstance(other, str)
        assert other is not None
        if isinstance(other, int):
            return self.timestamp > other

        return self.timestamp > other.timestamp

    def __ge__(self, other):
        assert not isinstance(other, str)
        assert other is not None
        if isinstance(other, int):
            return self.timestamp >= other

        return self.timestamp >= other.timestamp

    @staticmethod
    def get_timestamp_from_hour(t):
        return calendar.timegm(time.strptime(t, "%H:%M"))

    @staticmethod
    def get_timestamp_from_date_hour(d, t):
        return calendar.timegm(time.strptime(d + " " + t, "%Y/%m/%d %H:%M"))

    @staticmethod
    def get_timestamp_from_date(d):
        return calendar.timegm(time.strptime(d, "%Y/%m/%d"))
