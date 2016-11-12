#! /usr/bin/python
# coding: utf-8

import pystache
from os.path import join as OS_join
import sys
import json

class PartialsLoader(object):

	def __init__(self):
		self.templateLoader = pystache.loader.Loader(file_encoding='utf-8')
		self.templateDir = "../template"

	def get(self, templateName):
		return self.templateLoader.load_file(OS_join(self.templateDir,templateName))

renderer = pystache.Renderer(
	file_extension = "html",
	search_dirs = "../template/",
	file_encoding = 'utf-8'
)

def encodeNewLines(string):
	return "<br />".join(string.split("\n"))

def encodeNewLinesFromData(data):
	data["content"] = encodeNewLines(data["content"])
	for comment in data["comments"]:
		comment["content"] = encodeNewLines(comment["content"])
		for answer in comment["answers"]:
			answer["content"] = encodeNewLines(answer["content"])

path = sys.argv[1]
with open(path, "r") as json_file:
	json_file_text = json_file.read().replace("\\n", "<br>")
	print json_file_text
	json_file = json.loads(json_file_text)


	#encodeNewLinesFromData(data)

	html = renderer.render_name('cc-post', json_file)
	f = open(OS_join(json_file["output_path"], "output.html"), "w")
	f.write(html.encode("UTF-8"))
	f.close()
