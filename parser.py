from conference import Conference
from conference import Session
from conference import Track
from conference import Slot
from conference import Speaker
import xml.etree.ElementTree as ET

class XMLParser:

    def __init__(self, xml_file):
        self.input = xml_file

    def parse(self):

        conference_xml = ET.parse(self.input).getroot()
        conference = Conference()

        for subevent in conference_xml:

            if subevent.tag == 'subevent':

                for child in subevent:

                    if child.tag == 'title':
                        current_session = Session(child.text, conference)

                    elif child.tag == 'date':
                        current_session.day = child.text

                    elif child.tag == 'room':
                        current_session.room = child.text

                    elif child.tag == 'tracks':

                        assert len(child) == 1  # one event in a single track
                        track_tag = child[0]
                        track = conference.get_track(track_tag.text)
                        current_session.track = track
                        track.add_session(current_session)

                    elif child.tag == 'timeslot':
                        for slot_child in child:

                            if slot_child.tag == 'title':
                                current_slot = Slot(slot_child.text if slot_child.text is not None else "Unknown")
                                current_session.add_slot(current_slot)

                            elif slot_child.tag == 'room':
                                current_slot.room = slot_child.text

                            elif slot_child.tag == 'start_time':
                                current_slot.start = slot_child.text

                            elif slot_child.tag == 'end_time':
                                current_slot.end = slot_child.text

                            elif slot_child.tag == 'description':
                                current_slot.description = slot_child.text

                            elif slot_child.tag == 'persons':

                                for person in slot_child:
                                    for person_child in person:

                                        if person_child.tag == 'first_name':
                                            current_speaker = Speaker(person_child.tag, None, None)
                                            current_slot.add_speaker(current_speaker)

                                        elif person_child.tag == 'last_name':
                                            current_speaker.last_name = person_child.text

                                        elif person_child.tag == 'affiliation':
                                            current_speaker.affiliation = person_child.text

            else:
                pass
                # print "Unhandled tag: " + str(subevent)

        # sort sessions by date and name
        conference.sort_sessions()

        # build time ranges
        conference.build_time_ranges()

        return conference