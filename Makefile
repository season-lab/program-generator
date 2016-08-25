all:
	python main.py input/schedule.xml 0 > output/first.html
	python main.py input/schedule.xml 1 > output/second.html
	python main.py input/schedule.xml 2 > output/third.html
	python main.py input/schedule.xml 3 > output/fourth.html
	python main.py input/schedule.xml 4 > output/fifth.html
	python main.py input/schedule.xml 5 > output/sixth.html

