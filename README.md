This repository provides few scripts/files that can be used for generating a conference program using the data exported from conf.researchr.org. They have been developed for ECOOP 2016.

Some notes:
 * Input file is a ACM DL Mobile app XML containing details about sessions/talks of a conference. It can be exported from the conf.researchr.org using the Dashboard > General Data > Data Export. See input/schedule.xml for an example.
 * These python scripts generate HTML code. CSS and JavaScript are then used to make schedule looks pretty.
 * It is likely that you need to refactor and to improve these scripts if a schedule for another conference has to be generated. They have been developed exploiting some ECOOP-specific features and thus it's unlikely they will work smoothly. Nevertheless, they can be used as a starting point for obtaining a working set of scripts.
 * There is no support for generating the schedule for the whole conference, but only for generating the schedule of each separate day of the conference.

To generate the schedule for the first day of the conference:
`python main.py input/schedule.xml 0 > output/first.html`