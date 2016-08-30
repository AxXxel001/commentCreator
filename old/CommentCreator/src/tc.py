#! /usr/bin/python

import sys
import os


FULL_TEMPLATE = """{
	"persons": [
		{
			"id": "_kundendienst",
			"data": {
				"first_name": "Kundendienst",
				"last_name": "",
				"image": null
			}
		},

		%s,

		%s



	],

	"author": "_kunde",
	"to": "_unternehmen",
	"text": "%s",

	"comments": [
		{
		"author": "_kundendienst",
		"text": "%s",
		"likes": 0,
		"answers": [
			%s
		]
		}
	],

	"likes":0,
	"shares":0,
	"date":""
}"""

UNTERNEHMEN_TEMPLATE = """{
			"id": "_unternehmen",
			"data": {
				"first_name": "%s",
				"last_name": "",
				"image": null
			}
		}"""

KUNDE_TEMPLATE = """{
			"id": "_kunde",
			"data": {
				"first_name": "%s",
				"last_name": "%s",
				"image": null
			}
		}"""

KUNDENDIENST_ANTWORT_TEMPLATE = """{
				"author": "_kundendienst",
				"text": "%s",
				"likes": 0
			}"""

KUNDE_ANTWORT_TEMPLATE = """{
				"author": "_kunde",
				"text": "%s",
				"likes": 0
			}"""

def get_full_file(fname):
	blocks = [s.strip() for s in open(fname, "r").read().replace("\r","").split("\n\n\n")]
	if len(blocks) < 4:
		print blocks
		print (">>: ERROR: zu kurz! Nur %i Blocks" % len(blocks)),fname
	kunde_name = blocks[0].split(" ")
	unternehmen_name = blocks[1]
	kunde_beschwerde = blocks[2]
	kundendienst_comment = blocks[3]
	answers = ""
	kunde_ist_dran = True
	first = True
	if len(blocks) > 4:
		for block in blocks[4:]:
			prefix = ",\n"
			if first:
				prefix = ""
				first = False
			if kunde_ist_dran:
				answers += prefix+("%s" % (KUNDE_ANTWORT_TEMPLATE % block ))
			else:
				answers += prefix+("%s" % (KUNDENDIENST_ANTWORT_TEMPLATE % block ))
			kunde_ist_dran = not kunde_ist_dran
	t1 = UNTERNEHMEN_TEMPLATE % unternehmen_name
	t2 = KUNDE_TEMPLATE % (kunde_name[0], kunde_name[1])
	t3 = FULL_TEMPLATE % (t1, t2, kunde_beschwerde, kundendienst_comment, answers)
	return t3

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "usage: python tc.py -fr source_path"
		sys.exit(1)
	mode = sys.argv[1]
	if mode == "-f":
		print get_full_file(sys.argv[2])
	elif mode == "-r":
		path = sys.argv[2]
		if not os.path.isdir(path):
			print "error: not a directory:",path
			sys.exit(1)
		destination = path+os.sep+"templates"
		try:
			os.mkdir(destination)
		except OSError:
			pass
		fnames = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path,f)) and os.path.splitext(f)[1] in (".txt",) )]
		for name in fnames:
			try:
				result = get_full_file(os.path.join(path,name))
			except BaseException as e:
				print "ERROR:\nfile: %s\nerror: %s\n\n" % (name, str(e))
				sys.exit(1)
			print ">: Datei",os.path.join(destination, os.path.splitext(name)[0]+".json")
			newfile = open(os.path.join(destination, os.path.splitext(name)[0]+".json"), "w")
			newfile.write(result)
			newfile.close()














