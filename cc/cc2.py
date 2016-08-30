#! /usr/bin/python
# coding: utf-8

import pystache
from os.path import join as OS_join

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

data = {
	"css_path": u"../style/cc.css",
	"first_name": u"Alexander",
	"last_name": u"Schäfer",
	"company_name": u"Heinrich Heine Consulting e.V.",
	"content": u"""Ich finde euch scheiße!! :-(
Füher wäre alles größer und besser gewesen!

Euer Alex.""",
	"comments": [
		{
			"first_name": u"Kundendienst",
			"last_name": u"",
			"content": u"""Guten Tag,

das können wir so nicht bestätigen!""",
			"answers": [
				{
					"first_name": u"Alexander",
					"last_name": u"Schäfer",
					"content": u"""Fieß!"""
				}
			]
		},
		{
			"first_name": u"Kundendienst",
			"last_name": u"",
			"content": u"""Guten Tag,

das können wir so nicht bestätigen!""",
			"answers": [
				{
					"first_name": u"Alexander",
					"last_name": u"Schäfer",
					"content": u"""Fieß!"""
				}
			]
		}
	]
}

html = renderer.render_name('facebook_template', data)
f = open("output.html", "w")
f.write(html.encode("UTF-8"))
f.close()
