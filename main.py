from parser import XMLParser
from html_generator import HTMLGenerator

import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "python " + __file__ + " <xml_file> <n_day>"
        print "e.g.:"
        print "> python " + __file__ + " input/schedule.xml 0"
        print "for printing the schedule of the first day."
        sys.exit(1)

    parser = XMLParser(sys.argv[1])
    conference = parser.parse()
    dumper = HTMLGenerator(conference)
    dumper.dump(int(sys.argv[2]))