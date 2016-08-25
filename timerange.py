
class TimeRange(object):

    def __init__(self, conference):
        self.conference = conference
        self.sessions = []
        self._start = None
        self._end = None
        self.additional_start_ticks = []

    def add_session(self, session, update_start_end=True):

        if update_start_end:
            if self._start is None or session.start < self.start:
                self._start = session.start
            if self._end is None or session.end > self.end:
                self._end = session.end

        if session.start > self._start and session.start not in self.additional_start_ticks:
            self.additional_start_ticks.append(session.start)

        self.sessions.append(session)

    def conflict(self, session):

        if self._start is None and self._end is None:
            return False

        start_a = self._start
        end_a = self._end
        start_b = session.start
        end_b = session.end
        return (start_a >= start_b and end_a >= end_b) \
               or (start_a >= start_b and end_a < end_b) \
               or (start_b >= start_a and end_b < end_a) \
               or (start_b >= start_a and start_b < start_a) \
               or (start_a <= start_b and end_a > start_b)

    @property
    def start(self):
        assert self._start is not None
        return self._start

    @start.setter
    def start(self, v):
        self._start = v

    @property
    def end(self):
        assert self._end is not None
        return self._end

    @end.setter
    def end(self, v):
        self._end = v

    def get_sessions_track(self, track):
        sessions = []
        for session in self.sessions:

            if track is not None and session.track != track:
                continue

            placed = False

            if len(sessions) == 0:
                sessions.append([session])
            else:
                for subtrack in sessions:
                    for ses in subtrack:
                        if session.conflict(ses):
                            subtrack.append(session)
                            placed = True
                            break

                    if placed:
                        break

                if not placed:
                    sessions.append([session])

        return sessions

    def width_track(self, track):

        tracks = {}
        for session in self.sessions:

            if track is not None and session.track != track:
                continue

            placed = False

            if session.track.name not in tracks:
                tracks[session.track.name] = [[session]]
            else:
                for subtrack in tracks[session.track.name]:
                    for ses in subtrack:
                        if session.conflict(ses):
                            subtrack.append(session)
                            placed = True
                            break

                    if placed:
                        break

                if not placed:
                    tracks[session.track.name].append([session])

        width = 0
        for track in tracks:
            max_width = 0
            for subtrack in tracks[track]:
                max_width = len(subtrack) if len(subtrack) > max_width else max_width
            width += max_width

        return width

    @property
    def width(self):
        return self.width_track(None)

    @property
    def tracks(self):
        tracks = []
        for session in self.sessions:
            if session.track not in tracks:
                tracks.append(session.track)
        return tracks

    def has_track(self, track_name, session_name=None):
        for session in self.sessions:
            if session.track.name == track_name:
                if session_name is None:
                   return True
                elif session.name != session_name:
                    return True
        return False

    def has_track_with_session(self, track_name, session_name=None):
        for session in self.sessions:
            if session.track.name == track_name:
                if session_name is None:
                    return True
                elif session.name == session_name:
                    return True
        return False

    def get_sessions_by_track(self, track_name):
        sessions = []
        for session in self.sessions:
            if session.track.name == track_name:
                sessions.append(session)

        return sessions