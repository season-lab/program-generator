# Automatically generate unformatted HTML files for the six conference
# days and add code to load JavaScript source files to them 

DEST = .
SCRIPT_SRC = ..

INSERTION = 'NR==5{print "<script src=\"jquery-3.0.0.min.js\"></script>\n<script src=\"palette.js\"></script>\n<script src=\"$@.js\"></script>"}1'

all: sunday monday tuesday wednesday thursday friday

sunday:
	python $(SCRIPT_SRC)/main.py schedule.xml 0 | awk $(INSERTION) > $(DEST)/$@.html

monday:
	python $(SCRIPT_SRC)/main.py schedule.xml 1 | awk $(INSERTION) > $(DEST)/$@.html

tuesday:
	python $(SCRIPT_SRC)/main.py schedule.xml 2 | awk $(INSERTION) > $(DEST)/$@.html

wednesday:	
	python $(SCRIPT_SRC)/main.py schedule.xml 3 | awk $(INSERTION) > $(DEST)/$@.html

thursday:	
	python $(SCRIPT_SRC)/main.py schedule.xml 4 | awk $(INSERTION) > $(DEST)/$@.html

friday:	
	python $(SCRIPT_SRC)/main.py schedule.xml 5 | awk $(INSERTION) > $(DEST)/$@.html
