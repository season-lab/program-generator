import sys

from day import Day
from hour import Hour
from timerange import TimeRange


class Conference:

    def __init__(self):
        self.days = {}
        self.tracks = []
        self.conference_days = {}

    def get_day(self, day):
        if isinstance(day, basestring):
            for d in self.days:
                if d.str == day:
                    return d

        if day not in self.days.keys():
            self.days[day] = []

        assert day in self.days.keys()

        return day

    def get_days(self):
        return sorted(self.days.keys())


    def get_track(self, track_name):
        for track in self.tracks:
            if track.name == track_name:
                return track

        track = Track(track_name, self)
        self.tracks.append(track)
        return track

    def add_session(self, session):
        assert session.day is not None
        assert session.day in self.days
        self.days[session.day].append(session)

    def sort_sessions(self):
        for day in self.days:
            sessions = self.days[day]
            for session in sessions:
                session.slots = sorted(session.slots, key=lambda slot: slot.start, reverse=False)

            sessions = sorted(sessions, key=lambda session: (session.start, session.name), reverse=False)
            self.days[day] = sessions

            """
            print "Day: " + str(day)
            for s in self.days[day]:
                print s
            """

    def __repr__(self):
        s = ""
        for track in self.tracks:
            s += "\nTrack: " + track.name + "\n"
            for session in track.sessions:
                s += "\t" + str(session.day) + " " + str(session.start) + " - " + str(session.end) + " : " + session.name + "\n"
                for slot in session.slots:
                    s += '\t\t' + str(slot.start) + " - " + str(slot.end) + ": " + slot.name + "\n"
        return s

    def build_time_ranges(self):

        days = self.get_days()

        verbose = False

        for day in days:

            if verbose:
                print day
            self.conference_days[day] = ConferenceDay(day, self)
            tr = self.conference_days[day].new_time_range()

            for session in self.days[day]:

                #print "processing: " + str(session)

                assert isinstance(session, Session)

                # check if session is in conflict with current time range
                # we assume that sessions are sorted by starting time
                # if yes, include in it
                # if not, start a new time range

                if not tr.conflict(session):

                    if len(tr.sessions) > 0:
                        if verbose:
                            print "\t-- " + str(tr.start) + " => " + str(tr.end)
                        tr = self.conference_days[day].new_time_range()
                    if verbose:
                        print "\t" + str(session)
                    tr.add_session(session)

                else:

                    catering_session = tr.get_sessions_by_track('Catering')
                    assert len(catering_session) == 0 or len(catering_session) == 1
                    if len(catering_session) == 1 and catering_session[0].name == "Poster Session & Workshops Reception":
                        catering_session = []

                    # rule exception
                    # catering is allowed to be in conflict
                    if session.track.name == 'Catering' and session.name != "Poster Session & Workshops Reception":

                        tr.end = session.start
                        if verbose:
                            print "\t-- " + str(tr.start) + " => " + str(tr.end)

                        prev_tr = tr
                        tr = self.conference_days[day].new_time_range()

                        tr.add_session(session)
                        if verbose:
                            print "\t" + str(session)

                        max_end = None
                        for s in prev_tr.sessions:
                            if s.end > session.start:
                                tr.add_session(s)
                                if verbose:
                                    print "\t" + str(s)
                                max_end = s.end if max_end is None or s.end > max_end else max_end

                        tr.start = session.start

                        if max_end < tr.end:
                            tr.end = max_end
                            if verbose:
                                print "\t-- " + str(tr.start) + " => " + str(tr.end)
                            tr = self.conference_days[day].new_time_range()
                            tr.add_session(session)
                            if verbose:
                                print "\t" + str(session)
                            tr.start = max_end

                    # rule exception
                    # a session that is in conflict with catering may span across two time ranges
                    elif tr.has_track('Catering') and len(catering_session) > 0:

                        if session.start >= tr.start and session.start < tr.end:

                            #tr.add_session(session, update_start_end=False)
                            #print "\t" + str(session)
                            tr.end = session.start
                            assert len(catering_session) == 1
                            catering_session = catering_session[0]
                            if verbose:
                                print "\t--" + str(tr.start) + " => " + str(tr.end)
                            tr = self.conference_days[day].new_time_range()
                            tr.add_session(catering_session)
                            tr.add_session(session)
                            if verbose:
                                print "\t" + str(catering_session)
                                print "\t" + str(session)
                            tr.start = session.start

                            if session.end > catering_session.end:
                                tr.end = catering_session.end
                                if verbose:
                                    print "\t--" + str(tr.start) + " => " + str(tr.end)
                                tr = self.conference_days[day].new_time_range()
                                tr.add_session(session)
                                tr.start = catering_session.end
                                if verbose:
                                    print "\t" + str(session)

                        elif session.end > tr.end:

                            tr.add_session(session, update_start_end=False)
                            if verbose:
                                print "\t" + str(session)
                                print "\t--" + str(tr.start) + " => " + str(tr.end)
                            tr = self.conference_days[day].new_time_range()
                            tr.add_session(session)
                            if verbose:
                                print "\t" + str(session)

                        else:

                            tr.add_session(session, update_start_end=False)
                            if verbose:
                                print "\t" +  str(session)

                    else:
                        tr.add_session(session)
                        if verbose:
                            print "\t" + str(session)

            q = 0
            for tr in self.conference_days[day].time_ranges:
                if q < len(self.conference_days[day].time_ranges) - 1:
                    next_tr = self.conference_days[day].time_ranges[q + 1]
                    if tr.end < next_tr.start:
                        t = TimeRange(self)
                        t.start = tr.end
                        t.end = next_tr.start
                        self.conference_days[day].time_ranges.insert(q + 1, t)
                q += 1

            #print self.conference_days[day]


class ConferenceDay(object):

    def __init__(self, day, conference):
        self.day = day
        self.conference = conference
        self._start = None
        self._end = None
        self.time_ranges = []
        self.explicit_ticks = []

    def new_time_range(self):
        tr = TimeRange(self.conference)
        self.time_ranges.append(tr)
        return tr

    def get_time_ranges(self):
        self.time_ranges = sorted(self.time_ranges)
        return self.time_ranges

    @property
    def start(self):
        assert len(self.time_ranges) > 0
        time_ranges = sorted(self.time_ranges, key = lambda tr : tr.start)
        return time_ranges[0].start

    @property
    def tracks(self):
        tracks = []
        for tr in self.time_ranges:
            for track in tr.tracks:
                if track not in tracks:

                    # rule exception
                    if track.name == 'Catering':
                        continue

                    tracks.append(track)

        return tracks

    def has_track(self, track_name):
        for tr in self.time_ranges:
            for track in tr.tracks:
                if track.name == track_name:
                    return True
        return False

    def width_track(self, track):
        max_width = -1
        for tr in self.time_ranges:
            width = tr.width_track(track)
            max_width = width if width > max_width else max_width
        return max_width

    @property
    def width(self):
        max_width = -1
        for tr in self.time_ranges:
            width = tr.width

            # rule exception
            width = width - 1 if tr.has_track('Catering') else width

            max_width = width if width > max_width else max_width

        return max_width

    def __repr__(self):
        s = "Day: " + str(self.day) + " width: " + str(self.width) + "\n"
        for tr in self.time_ranges:
            s += "\t" + str(tr.start) + " - " + str(tr.end) \
                + " n_tracks: " + str(len(tr.tracks)) \
                + " width: " + str(tr.width) \
                + " add_ticks: " + str(tr.additional_start_ticks)
            s += "\n"
        return s

class Session(object):
    def __init__(self, name, conference):
        self.name = name
        self.conference = conference
        self.slots = []
        self._track = None
        self._day = None
        self.room = None

    def __repr__(self):
        s = str(self.start) + " - " \
               + str(self.end) + ": " \
               + str(self.track.name) \
               + " - " + self.name \
               + " room: " + self.room

        for slot in self.slots:
            print slot

        return s

    def add_slot(self, slot):
        self.slots.append(slot)

    @staticmethod
    def clean_name(name, track_name):
        return name[name.index(': ') + 2:]

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, d):
        assert isinstance(d, basestring)
        self._day = Day(d)
        self.conference.get_day(self._day)

    @property
    def start(self):
        start = None
        for slot in self.slots:
            if start == None or start > slot.start:
                start = slot.start
        return start

    @property
    def end(self):
        end = None
        for slot in self.slots:
            if end == None or end < slot.end:
                end = slot.end
        return end

    @property
    def track(self):
        return self._track

    @track.setter
    def track(self, track):
        self.name = Session.clean_name(self.name, track.name)
        self._track = track

    def conflict(self, session):

        if self.start is None and self.end is None:
            return False

        start_a = self.start
        end_a = self.end
        start_b = session.start
        end_b = session.end

        # ToDo: fix these...
        return (start_a >= start_b and end_a >= end_b and start_a < end_b) \
               or (start_a >= start_b and end_a < end_b) \
               or (start_b >= start_a and end_b < end_a) \
               or (start_b >= start_a and start_b < start_a) \
               or (start_a <= start_b and end_a > start_b)

class Track:

    def __init__(self, name, conference):
        self.name = name
        self.conference = conference
        self.sessions = []

    def __repr__(self):
        return Track.clean_track_name(self.name)

    def add_session(self, session):
        self.sessions.append(session)
        self.conference.add_session(session)

    @staticmethod
    def clean_track_name(track_name):
        if track_name == 'Research Track':
            return "ECOOP"
        else:
            return track_name

class Slot(object):
    def __init__(self, name):
        self.name = name
        self.room = None
        self._start = None
        self._end = None
        self.description = None
        self.speakers = []

    def add_speaker(self, speaker):
        self.speakers.append(speaker)

    def __repr__(self):
        s = str(self.start) + " - " + str(self.end) \
            + ": " + unicode(self.name).encode('ascii', 'xmlcharrefreplace') + " -"

        for p in self.speakers:
            s += " " + unicode(p.last_name).encode('ascii', 'xmlcharrefreplace')

        return s

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, hour):
        assert isinstance(hour, basestring)
        self._start = Hour(hour)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, hour):
        assert isinstance(hour, basestring)
        self._end = Hour(hour)

class Speaker:
    def __init__(self, first_name, last_name, affiliation):
        self.fist_name = first_name
        self.last_name = last_name
        self.affiliation = affiliation
