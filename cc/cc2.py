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
	"res_path": u"../res",
	"css_path": u"../style/cc.css",
	"output_path": u"../output",
	"first_name": u"Alexander",
	"last_name": u"Schäfer123123",
	"image": u"dummy",
	"blur_image": True,
	"company_name": u"HHC Düsseldorf",
	"content": u"""!"§$%&/()=?*'ÄPÖ_:;:_Ä'*`?=)(/&%$§"¶¢[]{}≠¿•æœø∆∞µ~∫ƒ∂®†Ω""",
	"comments": [
		{
			"first_name": u"Kundendienst",
			"last_name": u"",
			"image": u"dummy",
			"blur_image": False,
			"content": u"""Guten Tag,

das können wir so nicht bestätigen!""",
			"answers": [
				{
					"first_name": u"Alexander",
					"last_name": u"Schäfer1231",
					"image": u"dummy",
					"blur_image": True,
					"content": u"""Antwort1!"""
				},
				{
					"first_name": u"Kundendienst",
					"image": u"dummy",
					"blur_image": False,
					"last_name": u"Schäfer",
					"content": u"""Antwort 2 Geht auch hier noch weiter :-)"""
				},
				{
					"first_name": u"Alexander",
					"last_name": u"Schäfer",
					"image": u"dummy",
					"blur_image": True,
					"content": u"""Antwort    3"""
				}
			]
		},
		{
			"first_name": u"Peter",
			"last_name": u"Maffay",
			"image": u"dummy",
			"blur_image": True,
			"content": u"Fake!",
			"answers": [
				{
					"first_name": u"Alexander",
					"last_name": u"Schäfer",
					"image": u"dummy",
					"blur_image": False,
					"content": u"""Fieß!"""
				}
			]
		}
	]
}

def encodeNewLines(string):
	return "<br />".join(string.split("\n"))

def encodeNewLinesFromData(data):
	data["content"] = encodeNewLines(data["content"])
	for comment in data["comments"]:
		comment["content"] = encodeNewLines(comment["content"])
		for answer in comment["answers"]:
			answer["content"] = encodeNewLines(answer["content"])

encodeNewLinesFromData(data)

html = renderer.render_name('cc-post', data)
f = open(OS_join(data["output_path"], "output.html"), "w")
f.write(html.encode("UTF-8"))
f.close()
