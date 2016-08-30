#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4.uic import loadUi
from PyQt4.QtCore import QUrl
from os import sep
from os import getcwd
from os.path import isfile
from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox
from res import py_commentcreator
from src import cc
import json
from collections import OrderedDict

import pprint

class CCMainWindow(QMainWindow):

	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		print getcwd()
		self.ui = py_commentcreator.Ui_Form()
		self.ui.setupUi(self)
		self.ui.retranslateUi(self)
		# self.ui = loadUi(sep.join(["res","mainwindow.ui"]))
		self.setup_attributes()
		self.setup_ui()
		self.show()

		self.pp = pprint.PrettyPrinter(indent=4)

	def setup_attributes(self):
		self.json_filestruct = None
		self.post_name = ""
		self.json_code = ""
		self.html_code = ""
		self.file_path = ""

	def setup_ui(self):
		self.ui.line_postname.setText(self.post_name)
		self.ui.code_field.setText(self.json_code)
		self.ui.webView.settings().setObjectCacheCapacities(0,0,0)
		self.ui.button_new.clicked.connect(self.handler_new)
		self.ui.button_open.clicked.connect(self.handler_open)
		self.ui.button_save.clicked.connect(self.handler_save)
		self.ui.button_compile.clicked.connect(self.handler_compile)
		self.ui.button_get_path.clicked.connect(self.handler_get_path)

	def get_ordered_json_string(self, post):
		ordered = OrderedDict([
			("meta", OrderedDict([
				("made_by", post["meta"]["made_by"])
			])),
			("persons", []),
			("author", post["author"]),
			("to", post["to"]),
			("date", post["date"]),
			("text", post["text"]),
			("likes", post["likes"]),
			("shares", post["shares"]),
			("comments", [])
		])
		for person in post["persons"]:
			ordered["persons"].append(
				OrderedDict([
					("id", person["id"]),
					("data", OrderedDict([
						("first_name", person["data"]["first_name"]),
						("last_name", person["data"]["last_name"]),
						("image", person["data"]["image"])
					]))
				])
			)
		for comment in post["comments"]:
			current = OrderedDict([
				("author", comment["author"]),
				("text", comment["text"]),
				("likes", comment["likes"]),
				("answers", [])
			])
			for answer in comment["answers"]:
				current["answers"].append(
					OrderedDict([
						("author", answer["author"]),
						("text", answer["text"]),
						("likes", answer["likes"])
					])
				)
			ordered["comments"].append(current)
		return json.dumps(ordered, indent=4, separators=(',', ': '))

	def handler_new(self, event):
		self.setup_attributes()
		self.open_file(sep.join([getcwd(),"res","emptypost.json"]))

	def handler_open(self, event):
		fname = QFileDialog.getOpenFileName(
			self,
			"Open file",
			getcwd()
		)
		if not isfile(fname):
			return
		self.open_file(fname)

	def open_file(self, fname):
		with open(fname, "r") as jsonfile:
			json_text = jsonfile.read()
			self.file_path = fname
			self.json_filestruct = json.loads(json_text)
			self.post_name = self.json_filestruct["name"]
			self.json_code = self.get_ordered_json_string(self.json_filestruct["post"])
			# self.json_code = self.json_code.replace("&auml;",r"ä")
			# self.json_code = self.json_code.replace("&ouml;",r"ö")
			# self.json_code = self.json_code.replace("&uuml;",r"ü")
			# self.json_code = self.json_code.replace("&Auml;",r"Ä")
			# self.json_code = self.json_code.replace("&Uuml;",r"Ü")
			# self.json_code = self.json_code.replace("&Ouml;",r"Ö")
			# self.json_code = self.json_code.replace("&szlig;",r"ß")
			# self.json_code = self.json_code.replace("<br>","\n")
			self.html_code = self.json_filestruct["html"]
			self.ui.line_postname.setText(fname)
			self.ui.code_field.setText(self.json_code)
			with open("1111111.html", "w") as f:
				f.write(self.html_code)

			self.ui.webView.setHtml(self.html_code)
			self.ui.webView.settings().setObjectCacheCapacities(0,0,0)

	def handler_save(self, event):
		self.handler_compile(None)
		# evtl die self attribute aktualisieren
		self.json_filestruct["name"] = self.post_name
		self.json_filestruct["post"] = json.loads(self.json_code)
		self.json_filestruct["html"] = self.html_code
		try:
			with open(self.file_path, "w") as f:
				final_json = json.dumps(
					self.json_filestruct,
					indent=4,
					separators=(',', ': ')
				)
				f.write(final_json)
				QMessageBox.information(
					self,
					"Datei gesichert",
					"Datei wurde gespeichert"
				)
		except IOError as e:
			QMessageBox.critical(self,
				"Datei nicht gefunden",
				"Fehler: %s" % str(e)
			)

	def handler_compile(self, event):
		self.json_code = unicode(self.ui.code_field.toPlainText())
		# self.json_code = self.json_code.replace("ä","&auml;")
		# self.json_code = self.json_code.replace("ö","&ouml;")
		# self.json_code = self.json_code.replace("ü","&uuml;")
		# self.json_code = self.json_code.replace("Ä","&Auml;")
		# self.json_code = self.json_code.replace("Ü","&Uuml;")
		# self.json_code = self.json_code.replace("Ö","&Ouml;")
		# self.json_code = self.json_code.replace("ß","&szlig;")
		# self.json_code = self.json_code.replace("\n","<br>")
		self.json_filestruct["post"] = json.loads(self.json_code)
		url = QUrl("file://" + sep.join([getcwd(), "base"]))
		#print url
		cc.RESPATH = "file://" + sep.join([getcwd(), "base"])
		html = cc.create_html_post(cc.Post(self.json_filestruct["post"]))
		self.html_code = html
		self.ui.webView.setHtml(self.html_code, url)

	def handler_get_path(self, event):
		path = QFileDialog.getSaveFileName(
			self,
			"Get Directory",
			getcwd()
		)
		if path == "":
			return
		self.ui.line_postname.setText(path)
		self.file_path = path










