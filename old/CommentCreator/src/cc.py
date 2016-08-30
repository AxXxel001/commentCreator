# -*- coding: utf-8 -*-

# Imports
import sys
import json
import traceback
import re
import string
import codecs
from os.path import exists as path_exists, isfile, splitext, join
from os.path import abspath, dirname
from os import makedirs
from os import sep
from os import getcwd
from os import listdir
from shutil import copy as copy_file
from shutil import copytree as copy_dir
from random import shuffle

def assemble_path(*args):
	return sep.join(args)

RESPATH = "./base"#assemble_path(getcwd(), "base")
IMAGE_EXT = ".png"
DEBUG = False

def debug(msg):
	if DEBUG:
		print msg

class Profile(object):

	def __init__(self, json):
		self.first_name = json["first_name"]
		self.last_name = json["last_name"]
		self.image = json["image"]

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Post(object):

	def __init__(self, json):
		self.persons = {}
		for person_dict in json["persons"]:
			self.persons[person_dict["id"]] = Profile(person_dict["data"])
		self.author = json["author"]
		self.to = json["to"]
		self.likes = json["likes"]
		self.text = json["text"]
		self.date = json["date"]
		self.comments = []
		for c in json["comments"]:
			self.comments.append(Comment(c, self))
		self.shares = json["shares"]

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Comment(object):

	def __init__(self, json, post):
		self.author = json["author"]
		self.text = json["text"]
		self.likes = json["likes"]
		self.answers = []
		for a in json["answers"]:
			self.answers.append(Answer(a, post))

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Answer(object):

	def __init__(self, json, post):
		self.author = json["author"]
		self.text = json["text"]
		self.likes = json["likes"]

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)









def create_html_post(post):
	numberofpersons = len(post.persons)
	assert numberofpersons <= 20
	numbers = range(1,21)
	shuffle(numbers)
	imagerelation = {}
	for person_id in post.persons.iterkeys():
		if person_id == "_kundendienst":
			imagerelation[person_id] = 0
			continue
		imagerelation[person_id] = numbers.pop(len(numbers)-1)
	html = """<html>
	<head>
		<link rel="stylesheet" type="text/css" href="%s">
	</head>
	<body>
		<div class="post">""" % assemble_path(RESPATH, "commentcreator.css")
	html += create_html_header(post, imagerelation)
	html += """
		<div class="commentsection">"""
	for comment in post.comments:
		html += create_html_comment(post, comment, imagerelation)
	html += """
		</div>
		</div>
	</body>
</html>"""
	return html

def create_html_header(post, imagerelation):
	author = post.persons[post.author]
	to = post.persons[post.to]
	html_header = """
			<div class="header">
				<span class="imagecontainer_head"><img class="header_image_%s" src="%s"/></span>
				<div class="header_from">
					%s
				</div>
				<img class="header_from_to_image" src="%s">
				<div class="header_to">
					%s
				</div>
				<div class="header_text">
					%s
				</div>
				<div class="header_likes">
					
				</div>
			</div>
			%s
""" % (
		"visible" if post.author == "_kundendienst" else "hidden",
		assemble_path(
			RESPATH,
			"people",
			("person_"+str(imagerelation[post.author])+IMAGE_EXT)
		),
		author.first_name+" <span class=\"blurnamecontainer\"><span class=\"blurname\">"+author.last_name+"</span></span>",
		assemble_path(RESPATH, "arrow"+IMAGE_EXT),
		to.first_name+" "+to.last_name,
		post.text,
		BIG_LIKE_BOX#"<!--<span class='l'>%d</span><span class='c'>%d</span><span class='s'>%d</span>-->" % (post.likes, len(post.comments), post.shares)
	)
	return html_header


def create_html_comment(post, comment, imagerelation):
	author = post.persons[comment.author]
	html_comment = """
			<div class="comment">
				<span class="imagecontainer_comment">
					<img class="comment_image_%s" src="%s">
				</span>
				<div class="comment_text">
					<span class="comment_from">
						%s
					</span>
					%s
				</div>
				%s
				<!--<div class="comment_likes">
					%s
				</div>-->
			</div>
""" % (
		"visible" if comment.author == "_kundendienst" else "hidden",
		assemble_path(
			RESPATH,
			"people",
			(author.image if author.image!=None else "person_"+str(imagerelation[comment.author])+IMAGE_EXT)
		),
		author.first_name+" "+" <span class=\"blurnamecontainer\"><span class=\"blurname\">"+author.last_name+"</span></span>",
		comment.text,
		LIKE_BOX,
		"%d-%d" % (comment.likes, len(comment.answers))
	)
	for answer in comment.answers:
		html_comment += create_html_answer(post, answer, imagerelation)
	#html_comment += """
	#		</div>"""
	return html_comment

def create_html_answer(post, answer, imagerelation):
	author = post.persons[answer.author]
	imgpath = ""
	if author.image != None:
		imgpath = author.image
	else:
		imgpath = assemble_path(
			RESPATH,
			"people",
			(author.image if author.image!=None else "person_"+str(imagerelation[answer.author])+IMAGE_EXT)
		)
	html_answer = """
				<div class="answer">
					<span class="imagecontainer_answer">
						<img class="answer_image_%s" src="%s">
					</span>
					<div class="answer_text">
						<span class="answer_from">
							%s
						</span>
						%s
					</div>
					%s
					<!--<div class="likes">
						%d
					</div>-->
				</div>
""" % (
		"visible" if (answer.author == "_kundendienst" or author.image != None) else "hidden",
		imgpath,
		author.first_name+" "+" <span class=\"blurnamecontainer\"><span class=\"blurname\">"+author.last_name+"</span></span>",
		answer.text,
		LIKE_BOX,
		answer.likes
	)
	return html_answer






def findall(sub, string):
    """
    >>> text = "Allowed Hello Hollow"
    >>> tuple(findall('ll', text))
    (1, 10, 16)
    """
    index = 0 - len(sub)
    try:
        while True:
            index = string.index(sub, index + len(sub))
            yield index
    except ValueError:
        pass

def jsonfile_to_post(jsonfile):
	# Get json data
	#raw_input("davor")
	jsontext = jsonfile.read()
	#print jsontext
	#print "#"*100
	jsontext = jsontext.replace("ä","&auml;")
	#print 1
	jsontext = jsontext.replace("ö","&ouml;")
	#print 2
	jsontext = jsontext.replace("ü","&uuml;")
	#print 3
	jsontext = jsontext.replace("Ä","&Auml;")
	#print 4
	jsontext = jsontext.replace("Ö","&Ouml;")
	jsontext = jsontext.replace("Ü","&Uuml;")
	jsontext = jsontext.replace("ß","&szlig;")
	jsontext = jsontext.replace("€", "&euro;")
	#print jsontext
	#raw_input("------------------")
	#print "."*100
	i = 0
	for c in jsontext:
		if c not in string.ascii_letters+string.digits+string.whitespace+"#,;.:-_+*!?()/&{}[]\"'<>=%§@":
			print "Umgültiges Zeichen:",c
			print "Danach:",jsontext[i:i+100]
		i += 1
	for counter in range(len(tuple(findall('"text": "', jsontext[:])))):
		idx = tuple(findall('"text": "', jsontext))[counter]
		end = idx+9+jsontext[idx+9:].find("\",")
		new = jsontext[idx+9:end].replace("\n","<br>").replace("\t","").replace("\r","")
		jsontext = jsontext[0:idx+9]+new+jsontext[end:]
	#print jsontext
	#print "\n"*8
	try:
		#print "*"*50
		jsondecoded = json.loads(jsontext)
		#print "."*50
	except BaseException as e:
		print "jsonfiletopost: Error while parsing:",e
	#Parse json data
	try:
		post = Post(jsondecoded)
	except BaseException as e:
		print "jsonfiletopost: Error while converting:", e
		print traceback.format_exc()
		return
	return post

def help():
	print """
 - Facebook CommentCreator v 1.0 -

usage: cc.py -chjt [source] [destination]

Commands:

	-c source.json destination
		Create a post based on a json file. Creates the directory
		'destination', writes the output html file and a res directory from
		where images and css will be loaded.

	-h
		Print this help text.

	-p
		Print the json file, cc created based on the input file (just for debugging!)

	-t source.json
		Test wether the json file is in correct format. This should be used
		before -c to avoid deleting directories and resources multiple times.

(c) 2015 by Alexander Schaefer"""

def test():
	source = sys.argv[2]
	try:
		jsonfile = open(source, "r")
	except BaseException as e:
		print "Cant open file:",e
	try:
		testpost = jsonfile_to_post(jsonfile)
	except BaseException as e:
		print "Unknown error: %s" % str(e)
		sys.exit(1)
	print "Correct!"

def print_json():
	source = sys.argv[2]
	try:
		testpost = json_to_post(source)
	except BaseException as e:
		print "Unknown error: %s" % str(e)
		sys.exit(1)
	print testpost.to_JSON()

def create():
	if len(sys.argv) < 4:
		print "usage: cc.py -c source.json destination"
		sys.exit(1)
	source = sys.argv[2]
	destination = sys.argv[3]
	try:
		jsonfile = open(source, "r")
	except BaseException as e:
		print "create: Cant open file:",e
	try:
		post_object = jsonfile_to_post(jsonfile)
	except BaseException as e:
		print "create: error while parsing json file:",e
		sys.exit(1)
	if not path_exists(destination):
		makedirs(destination)
	try:
		f_html = open(destination+sep+"html_output.html", "w")
	except IOError as e:
		print "create: cannot create output file:",e
		sys.exit(1)
	else:
		try:
			html_post = create_html_post(post_object)
		except BaseException as e:
			print "create: cannot create html data:",e
			print traceback.format_exc()
		else:
			try:
				f_html.write(html_post)
			except BaseException as e:
				print "create: cannot write output file:",e
				print traceback.format_exc()
				sys.exit(1)
		finally:
			f_html.close()
	#makedirs(destination+sep+"res"+sep)
	try:
		makedirs(sep.join([destination,"base","people"]))
	except OSError as e:
		pass
	css_src = sep.join([RESPATH,"commentcreator.css"])
	css_dst = sep.join([destination,"base","commentcreator.css"])
	arrow_src = sep.join([RESPATH,"posting","arrow.png"])
	arrow_dst = sep.join([destination,"base","arrow.png"])
	black_src = sep.join([RESPATH,"posting","black.png"])
	black_dst = sep.join([destination,"base","black.png"])
	people_src = sep.join([RESPATH,"people","person_"])
	people_dst = sep.join([destination,"base","people","person_"])
	try:
		copy_file(css_src, css_dst)
		copy_file(arrow_src, arrow_dst)
		copy_file(black_src, black_dst)
		for i in xrange(0,21):
			copy_file(people_src+str(i)+".png",people_dst+str(i)+".png")
	except BaseException as e:
		print "create: Cannot write resource files: %s" % str(e)
		sys.exit(1)
	sys.exit(0)














































def recursive():
	if len(sys.argv) < 4:
		print "usage: cc.py -c source destination"
		sys.exit(1)
	spath = sys.argv[2]
	fnames = [f for f in listdir(spath) if (isfile(join(spath,f)) and splitext(f)[1] in (".json",) )]
	for filename in fnames:
		source = join(spath,filename)
		destination = sys.argv[3]
		try:
			jsonfile = open(source, 'r')#, 'utf-8', errors='ignore')
		except BaseException as e:
			print "create: Cant open file",filename,":",e
			raw_input()
			continue
		try:
			post_object = jsonfile_to_post(jsonfile)
		except BaseException as e:
			print "create: error while parsing json file",filename,":",e
			raw_input()
			continue
		if not path_exists(destination):
			makedirs(destination)
		try:
			f_html = open(destination+sep+splitext(filename)[0]+".html", "w")
		except IOError as e:
			print "create: cannot create output file",filename,":",e
			raw_input()
			continue
		else:
			try:
				html_post = create_html_post(post_object)
			except BaseException as e:
				print "create: cannot create html data",filename,":",e
				print traceback.format_exc()
				raw_input()
				continue
			else:
				try:
					f_html.write(html_post)
				except BaseException as e:
					print "create: cannot write output file",filename,":",e
					raw_input()
					continue
			finally:
				f_html.close()
	#makedirs(destination+sep+"res"+sep)
	try:
		makedirs(sep.join([destination,"base","people"]))
	except OSError as e:
		pass
	css_src = sep.join([RESPATH,"commentcreator.css"])
	css_dst = sep.join([destination,"base","commentcreator.css"])
	arrow_src = sep.join([RESPATH,"posting","arrow.png"])
	arrow_dst = sep.join([destination,"base","arrow.png"])
	black_src = sep.join([RESPATH,"posting","black.png"])
	black_dst = sep.join([destination,"base","black.png"])
	people_src = sep.join([RESPATH,"people","person_"])
	people_dst = sep.join([destination,"base","people","person_"])
	try:
		copy_file(css_src, css_dst)
		copy_file(arrow_src, arrow_dst)
		copy_file(black_src, black_dst)
		for i in xrange(0,21):
			copy_file(people_src+str(i)+".png",people_dst+str(i)+".png")
	except BaseException as e:
		print "create: Cannot write resource files: %s" % str(e)
		sys.exit(1)



	sys.exit(0)







































if __name__ == "__main__":
	#print f.read()
	#sys.exit(0)
	if len (sys.argv) < 2:
		print "usage: cc.py -hctr [source] [destination]"
		sys.exit(1)
	RESPATH = sep.join([dirname(abspath(sys.argv[0])),"..","base"])
	BIG_LIKE_BOX = """ <div class="header_like_box"><img class="big_likebox_img" src="%s" style="margin-top: -2px; float: left;"/>
<span style="float: left;">Gef&auml;llt mir</span>
<img class="big_likebox_img" src="%s" style="margin-top: 0px; float: left; margin-left:25px"/>
<span style="float: left;">Nachricht senden</span>
<img class="big_likebox_img" src="%s" style="margin-top: 0px; float: left; margin-left:25px"/>
<span style="float: left;">Teilen</span>
</div>""" % (
	assemble_path(
		RESPATH,
		"like.png"),
	assemble_path(
		RESPATH,
		"message.png"
	),
	assemble_path(
		RESPATH,
		"share14.png"
	)
)
	LIKE_BOX = """ <div class="like_box">Gef&auml;llt mir <span style="display:inline-block; width: 6px;"></span> Antworten
<span style="display:inline-block; width: 6px;"></span> Nachricht senden</div>
"""
	LIKE_BOX = ""
	cmd = sys.argv[1]
	if cmd == "-h":
		help()
	elif cmd == "-t":
		test()
	elif cmd == "-p":
		print_json()
	elif cmd == "-c":
		create()
	elif cmd == "-r":
		recursive()
	else:
		print "usage: cc.py -hctr [source] [destination]"
		sys.exit(1)
