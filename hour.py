from abstract_time import AbstractTime

class Hour(AbstractTime):

    def __init__(self, string_hour):
        timestamp = AbstractTime.get_timestamp_from_date_hour("1970/01/01", string_hour)
        super(Hour, self).__init__(string_hour, timestamp)
        assert self.timestamp is not None

    def __div__(self, other):
        assert not isinstance(other, str)
        if isinstance(other, int):
            return self.timestamp / other

        return self.timestamp / other.timestamp

    def __add__(self, other):
        assert not isinstance(other, str)

        if isinstance(other, int):
            return self.timestamp + other

        return self.timestamp + other.timestamp