# Automatically generate unformatted HTML files for the six conference
# days and add code to load JavaScript source files to them 

SED = gsed # for MacOS X users
DEST = .
SCRIPT_SRC = ..

all: sunday monday tuesday wednesday thursday friday

sunday:
	python $(SCRIPT_SRC)/main.py schedule.xml 0 > $(DEST)/$@.html
	$(SED) -i "5i<script src=\"jquery-3.0.0.min.js\"></script>" $(DEST)/$@.html
	$(SED) -i "6i<script src=\"palette.js\"></script>" $(DEST)/$@.html
	$(SED) -i "7i<script src=\"$@.js\"></script>" $(DEST)/$@.html
	
monday:
	python $(SCRIPT_SRC)/main.py schedule.xml 1 > $(DEST)/$@.html
	$(SED) -i "5i<script src=\"jquery-3.0.0.min.js\"></script>" $(DEST)/$@.html
	$(SED) -i "6i<script src=\"palette.js\"></script>" $(DEST)/$@.html
	$(SED) -i "7i<script src=\"$@.js\"></script>" $(DEST)/$@.html
	
tuesday:
	python $(SCRIPT_SRC)/main.py schedule.xml 2 > $(DEST)/$@.html
	$(SED) -i "5i<script src=\"jquery-3.0.0.min.js\"></script>" $(DEST)/$@.html
	$(SED) -i "6i<script src=\"palette.js\"></script>" $(DEST)/$@.html
	$(SED) -i "7i<script src=\"$@.js\"></script>" $(DEST)/$@.html
	
wednesday:	
	python $(SCRIPT_SRC)/main.py schedule.xml 3 > $(DEST)/$@.html
	$(SED) -i "5i<script src=\"jquery-3.0.0.min.js\"></script>" $(DEST)/$@.html
	$(SED) -i "6i<script src=\"palette.js\"></script>" $(DEST)/$@.html
	$(SED) -i "7i<script src=\"$@.js\"></script>" $(DEST)/$@.html
	
thursday:	
	python $(SCRIPT_SRC)/main.py schedule.xml 4 > $(DEST)/$@.html
	$(SED) -i "5i<script src=\"jquery-3.0.0.min.js\"></script>" $(DEST)/$@.html
	$(SED) -i "6i<script src=\"palette.js\"></script>" $(DEST)/$@.html
	$(SED) -i "7i<script src=\"$@.js\"></script>" $(DEST)/$@.html
	
friday:	
	python $(SCRIPT_SRC)/main.py schedule.xml 5 > $(DEST)/$@.html
	$(SED) -i "5i<script src=\"jquery-3.0.0.min.js\"></script>" $(DEST)/$@.html
	$(SED) -i "6i<script src=\"palette.js\"></script>" $(DEST)/$@.html
	$(SED) -i "7i<script src=\"$@.js\"></script>" $(DEST)/$@.html
