import time

import sys


class HTMLGenerator(object):

    def __init__(self, conference):
        self.conference = conference

    def get_next_session_start_time(self, subtrack, index, end):

        # ToDo: this is ad-hoc, should be generalized
        if subtrack == None:
            return end
        elif index < len(subtrack):
            return subtrack[index].start
        else:
            return subtrack[0].start

    def get_prev_session_end_time(self, subtrack, index, start):

        # ToDo: this is ad-hoc, should be generalized
        if subtrack == None:
            return start
        elif index < len(subtrack):
            return subtrack[index].end
        else:
            return subtrack[0].end

    def get_session(self, sessions, name):
        for s in sessions:

            if s.name == name:
                return s
        return None

    def get_tick_sessions(self, sessions, now, start, end, width, tick, tr):

        prev = None
        next = None
        current = None

        #print sessions
        #print time.strftime("%H:%M", time.gmtime(now))

        k = 0
        for subtrack in sessions:

            all_bigger = False
            for session in subtrack:

                if session.start >= now and session.end > now:
                    current = subtrack
                    break

            if current != None:
                k += 1
                break

            if all_bigger:
                k += 1
                break

            prev = subtrack
            k += 1

        #print k

        if k < len(sessions):
            next = sessions[k]

        #print "prev: " + str(prev)
        #print "current: " + str(current)
        #print "next: " + str(next)

        if current != None:

            count = len(current)
            span = width / count
            ticks = []

            j = 0
            for session in current:

                if now == session.start:

                    end = session.end

                    n_ticks = (session.end - session.start) / tick
                    ticks.append([session, n_ticks, span, session.start, session.end])

                elif now < session.start:
                    prev_end = self.get_prev_session_end_time(prev, j, start)
                    if now == prev_end:
                        n_ticks = (session.start - prev_end) / tick
                        ticks.append([None, n_ticks, span, prev_end, session.start])
                    else:
                        ticks.append([None, 0, span, None, None])

                elif now == session.end:

                    next_start = self.get_next_session_start_time(next, j, end)
                    n_ticks = (next_start - session.end) / tick
                    ticks.append([None, n_ticks, span, session.end, next_start])

                else:
                    ticks.append([None, 0, span, None, None])

                j += 1

            return ticks

        elif prev == None:

            assert next is not None

            count = len(next)
            span = width / count
            ticks = []

            j = 0
            for session in next:

                if now == start:
                    n_ticks = (session.end - start) / tick
                    ticks.append([None, n_ticks, span, start, session.end])
                else:
                    ticks.append([None, 0, span, None, None])

                j += 1

            return ticks

        elif next == None:

            count = len(prev)
            span = width / count

            ticks = []

            catering_session = self.get_session(tr.sessions, 'Poster Session & Workshops Reception')

            assert prev is not None

            j = 0
            for session in prev:

                # rule exception
                if catering_session is not None and now == catering_session.start:
                    ticks.append([None, 0, span, None, None])
                    j += 1
                    continue

                if now == session.end:
                    n_ticks = (end - session.end) / tick
                    ticks.append([None, n_ticks, span, session.end, end])
                else:
                    ticks.append([None, 0, span, None, None])

                j += 1

            return ticks

        assert False

    def is_catering(self, tr):
        if tr.has_track('Catering') and len(tr.sessions) == 1:
            return True
        else:
            return False

    def get_hour_tick(self, k, timeranges, prev_is_full_catering, next_is_full_catering):

        prev_has_catering = False
        if k > 0:
            prev_has_catering = timeranges[k - 1].has_track('Catering', 'Poster Session & Workshops Reception')

        is_catering = self.is_catering(timeranges[k])
        has_catering = timeranges[k].has_track('Catering', 'Poster Session & Workshops Reception')

        next_has_catering = False
        if k < len(timeranges) - 1:
            next_has_catering = timeranges[k + 1].has_track('Catering', 'Poster Session & Workshops Reception')

        if is_catering:
            if prev_has_catering:
                return [None, None]
            elif next_has_catering and k < len(timeranges) - 1:
                return [timeranges[k].start, timeranges[k + 1].end]
            else:
                return [timeranges[k].start, timeranges[k].end]

        if prev_is_full_catering:
            if has_catering:
                return [None, None]
            else:
                return [timeranges[k].start, timeranges[k].end]

        if next_is_full_catering:
            if has_catering:

                next_next_has_catering = False
                if k + 2 < len(timeranges):
                    next_next_has_catering = timeranges[k + 2].has_track('Catering')

                if next_next_has_catering:
                    return [timeranges[k].start, timeranges[k + 2].end]
                else:
                    return [timeranges[k].start, timeranges[k + 1].end]

            else:
                return [timeranges[k].start, timeranges[k].end]

        return [timeranges[k].start, timeranges[k].end]

    def dump(self, N):

        tick = 60 * 5

        # CSS class used for each track
        css_cl_dict = {'CurryOn': 'td-curryon', 'Research Track': 'td-ecoop', 'IWACO': 'td-iwaco',
                       'GRACE': 'td-grace', 'VORTEX': 'td-vortex', 'ICOOOLPS': 'td-icooolps',
                       'PX': 'td-px', 'COP': 'td-cop', 'JSTools': 'td-jstools', 'FTfJP': 'td-ftfjp',
                       'Summer School': 'td-summer-school', 'STOP': 'td-stop', 'LIVE': 'td-live',
                       'Doctoral Symposium': 'td-doctoral',
                       'Programming Models and Languages for Distributed Computing': 'td-pmldc',
                       'Catering': 'td-catering'}

        session_counter = {}

        days = sorted(self.conference.conference_days.keys())

        q = N
        day = days[q]
        conference_day = self.conference.conference_days[day]

        # tracks are sorted based on these scores
        if day.str != '2016/07/19':
            score = {'COP': 0, 'Research Track': -1, 'CurryOn': -2,
                     'Programming Models and Languages for Distributed Computing': 9, 'STOP': 12, 'PX': 10,
                     'ICOOOLPS': 5, 'VORTEX': 14, 'IWACO': 6, 'LIVE': 8, 'Summer School': 13, 'JSTools': 7,
                     'FTfJP': 3, 'Doctoral Symposium': 2, 'GRACE': 4}
        else:
            score = {'COP': 0, 'Research Track': -2, 'CurryOn': -3,
                     'Programming Models and Languages for Distributed Computing': 9, 'STOP': 12, 'PX': 10,
                     'ICOOOLPS': 5, 'VORTEX': 14, 'IWACO': 6, 'LIVE': 8, 'Summer School': 13, 'JSTools': 7,
                     'FTfJP': -1, 'Doctoral Symposium': 2, 'GRACE': 4}

        tracks = conference_day.tracks
        tracks = sorted(tracks, key=lambda track: score[track.name])

        print """        <html>
          <head>
            <title>""" + str(conference_day.day) + """</title>
            <link rel="stylesheet" type="text/css" href="schedule.css">
          </head>
          <body>
            <table class="table-elem">"""

        print '\t<tr>'
        print '\t\t<th class="td-day" colspan="' + str(conference_day.width + 1) + '">' + str(conference_day.day) + '</th>'
        print '\t</tr>'

        print '\t<tr>'
        print '\t\t<td class="header-track-empty"></td>'

        for track in tracks:

            header_id = ""
            css_cl = ""
            if track.name in css_cl_dict:
                css_cl = css_cl_dict[track.name]
                header_id = 'id="header-' + css_cl[3:] + '" '

            print '\t\t<td ' + header_id + ' class="' + css_cl + ' header-track" colspan="' \
                  + str(conference_day.width_track(track)) + '">' + str(track) + '</td>'

        print '\t</tr>'

        for q in range(len(conference_day.time_ranges)):

            tr = conference_day.time_ranges[q]

            prev_is_full_catering = False
            if q > 0:
                prev_is_full_catering = self.is_catering(conference_day.time_ranges[q - 1])

            next_is_full_catering = False
            next_has_catering = False
            if q < len(conference_day.time_ranges) - 1:
                next_is_full_catering = self.is_catering(conference_day.time_ranges[q + 1])
                next_has_catering = conference_day.time_ranges[q + 1].has_track('Catering')

            n_ticks = (tr.end - tr.start) / tick

            for i in range(n_ticks):

                now = tr.start + (i * tick)

                hour_is_on = False
                print '\t<tr>'

                if i == 0:

                    h_ticks = self.get_hour_tick(q, conference_day.time_ranges, prev_is_full_catering, next_is_full_catering)

                    if h_ticks[0] is not None:

                        hour_is_on = True
                        hn_ticks = (h_ticks[1] - h_ticks[0]) / tick
                        td_tag = '\t\t<td class="td-time" rowspan="' + str(
                          hn_ticks) + '">' + str(h_ticks[0]) + ' ' + str(h_ticks[1]) + '</td>'
                        print td_tag

                if tr.has_track('Catering') and len(tr.sessions) == 1:

                    if now == tr.start:
                        session = tr.sessions[0]
                        s_ticks = (tr.end - tr.start) / tick
                        td_id = self.get_session_id('catering', session_counter, 'td-session-catering', False)
                        print '\t\t<td ' + td_id + ' class="td-catering" rowspan="' + str(s_ticks) \
                              + '" colspan="' + str(conference_day.width) + '">' + session.name \
                              + ' (' + str(session.start) + ' - ' + str(session.end) + '<span class="session-catering-room">, ' + session.room + '</span>)</td>'


                    print '\t</tr>'
                    continue

                catering_session = self.get_session(tr.sessions, 'Poster Session & Workshops Reception')

                for track in tracks:

                    if tr.has_track(track.name):

                        sessions = tr.get_sessions_track(track)
                        width = conference_day.width_track(track)
                        ticks_sessions = self.get_tick_sessions(sessions, now, tr.start, tr.end, width, tick, tr)

                        span = width / len(ticks_sessions)

                        for ses_ticks in ticks_sessions:

                            session = ses_ticks[0]
                            s_ticks = ses_ticks[1]
                            s_span = ses_ticks[2]
                            s_end = ses_ticks[3]

                            if s_ticks == 0:
                                continue

                            if session == None:

                                td_id = self.get_session_id('empty', session_counter, 'td-empty', False)
                                span = 1
                                self.dump_empty_session(s_ticks, track, tr, td_id, hour_is_on,
                                                        catering_session,
                                                        next_is_full_catering, prev_is_full_catering,
                                                        next_has_catering, s_span)

                            else:

                                css_cl = ""
                                session_id = ""
                                if track.name in css_cl_dict:
                                    css_cl = css_cl_dict[track.name]
                                    session_id = self.get_session_id(session.track.name, session_counter, css_cl)

                                self.dump_session(session, s_ticks, s_span, tr, session_id, css_cl)

                    else:

                        if now == tr.start:

                            span = conference_day.width_track(track)

                            for n in range(span): # fix to be consistent with old script

                                if len(tr.sessions) == 0:
                                    fixed_span = span
                                else:
                                    fixed_span = 1

                                # rule exception
                                catering_session_parallel = self.get_session(tr.sessions, 'Poster Session & Workshops Reception')
                                end = tr.end
                                if catering_session_parallel is not None:
                                    end = catering_session.start

                                e_ticks = (end - tr.start) / tick
                                td_id = self.get_session_id('empty', session_counter, 'td-empty', False)

                                self.dump_empty_session(e_ticks, track, tr, td_id, hour_is_on, catering_session,
                                                        next_is_full_catering, prev_is_full_catering,
                                                        next_has_catering, fixed_span)

                                if len(tr.sessions) == 0:
                                    break

                if catering_session is not None and now == catering_session.start:
                    session = catering_session
                    s_ticks = (catering_session.end - catering_session.start) / tick
                    span = conference_day.width
                    for s in tr.sessions:
                        if s is not catering_session and catering_session.conflict(s):
                            span -= 1

                    session_id = self.get_session_id('catering', session_counter, 'td-catering-session', False)

                    self.dump_session(session, s_ticks, span, tr, session_id, "td-catering")

                print '\t</tr>'

        print """            </table>
              </body>
            </html>"""

    def get_session_id(self, track_name, session_counter, css_class, is_session=True):
        count = 1
        if track_name not in session_counter:
            session_counter[track_name] = count + 1
        else:
            count = session_counter[track_name]
            session_counter[track_name] += 1

        return 'id="' + css_class[3:] + '-' \
            + ('session-' if is_session else '') + str(count) + '"'

    def dump_session(self, session, s_ticks, span, tr, session_id, css_class):

        #td_content = session.name + ' (' + str(session.start) + ' - ' + str(session.end) + ')'

        td_content = ""
        td_content += "<table class=\"table-session\">"
        td_content += "<tr><td class=\"session-title\" colspan=\"2\">" + session.name + "</td></tr>"
        td_content += "<tr><td class=\"session-room\" colspan=\"2\">" + (
        session.room if session.room is not None else 'Unknown') + "</td></tr>"
        for slot in session.slots:

            speaker = ""
            for p in slot.speakers:
                speaker += unicode(p.last_name).encode('ascii', 'xmlcharrefreplace') + ", "
            if len(speaker) > 0 and speaker[-1] == " ":
                speaker = speaker[:len(speaker) - 2]

            td_content += "<tr><td class=\"session-slot-time\">" + str(slot.start) + "</td><td class=\"session-slot-author\">" + speaker + "</td></tr>"
            td_content += "<tr><td class=\"session-slot-title\" colspan=\"2\">" + unicode(slot.name).encode('ascii',
                                                                                                                'xmlcharrefreplace') + "</td></tr>"

        if tr.end != session.end:
            td_content += "<tr><td class=\"session-end-time\">" + str(session.end) + "</td><td class=\"session-end-text\">session end</td></tr>"

        td_content += "</table>"

        print '\t\t<td ' + session_id + ' class="' + css_class + ' td-session" rowspan="' + str(
            s_ticks) + '"  colspan="' + str(span) + '">' + td_content + '</td>'

    def dump_empty_session(self, e_ticks, track, tr, td_id, hour_is_on, catering_session, next_is_full_catering, prev_is_full_catering, next_has_catering, span):

        hour_level_td = ""
        if hour_is_on:
            hour_level_td = "td-hour-level"

        catering_top_td = ""
        if next_is_full_catering and tr.has_track('Catering', 'Poster Session & Workshops Reception'):
            catering_top_td = "td-catering-level"
            #hour_level_td = ""

        catering_top_level_td = ""
        if next_is_full_catering and not tr.has_track('Catering', 'Poster Session & Workshops Reception') and catering_top_td == "":  #
            catering_top_level_td = "td-catering-top-level"

        if not next_is_full_catering and next_has_catering and catering_top_td == "":  #
            catering_top_level_td = "td-catering-top-level"

        catering_bottom_td = ""
        if prev_is_full_catering and tr.has_track('Catering', 'Poster Session & Workshops Reception'):
            catering_top_level_td = "td-catering-top-level"
            catering_bottom_td = "td-catering-bottom-level"
            hour_level_td = ""

        print '\t\t<td ' + td_id + ' class="' + catering_top_level_td + ' ' \
              + catering_bottom_td + ' ' + hour_level_td + ' ' + catering_top_td \
              + ' empty-td" rowspan="' + str(e_ticks) + '" colspan="' + str(span) + '"></td>'
