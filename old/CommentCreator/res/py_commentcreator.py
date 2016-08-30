# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res/commentcreator.ui'
#
# Created: Sat Jan 30 12:35:51 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1237, 725)
        self.webView = QtWebKit.QWebView(Form)
        self.webView.setGeometry(QtCore.QRect(12, 12, 520, 701))
        self.webView.setMinimumSize(QtCore.QSize(520, 0))
        self.webView.setMaximumSize(QtCore.QSize(520, 16777215))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(540, 12, 559, 711))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_compile = QtGui.QPushButton(self.widget)
        self.button_compile.setMinimumSize(QtCore.QSize(0, 0))
        self.button_compile.setObjectName(_fromUtf8("button_compile"))
        self.horizontalLayout.addWidget(self.button_compile)
        self.button_export_html = QtGui.QPushButton(self.widget)
        self.button_export_html.setObjectName(_fromUtf8("button_export_html"))
        self.horizontalLayout.addWidget(self.button_export_html)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_new = QtGui.QPushButton(self.widget)
        self.button_new.setMinimumSize(QtCore.QSize(0, 0))
        self.button_new.setObjectName(_fromUtf8("button_new"))
        self.horizontalLayout.addWidget(self.button_new)
        self.button_open = QtGui.QPushButton(self.widget)
        self.button_open.setMinimumSize(QtCore.QSize(0, 0))
        self.button_open.setObjectName(_fromUtf8("button_open"))
        self.horizontalLayout.addWidget(self.button_open)
        self.button_save = QtGui.QPushButton(self.widget)
        self.button_save.setMinimumSize(QtCore.QSize(0, 0))
        self.button_save.setObjectName(_fromUtf8("button_save"))
        self.horizontalLayout.addWidget(self.button_save)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.line_postname = QtGui.QLineEdit(self.widget)
        self.line_postname.setReadOnly(True)
        self.line_postname.setObjectName(_fromUtf8("line_postname"))
        self.horizontalLayout_2.addWidget(self.line_postname)
        self.button_get_path = QtGui.QPushButton(self.widget)
        self.button_get_path.setObjectName(_fromUtf8("button_get_path"))
        self.horizontalLayout_2.addWidget(self.button_get_path)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.code_field = QtGui.QTextEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setBold(True)
        font.setWeight(75)
        self.code_field.setFont(font)
        self.code_field.setObjectName(_fromUtf8("code_field"))
        self.verticalLayout.addWidget(self.code_field)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.button_compile.setText(_translate("Form", "Compile!", None))
        self.button_export_html.setText(_translate("Form", "Export HTML", None))
        self.button_new.setText(_translate("Form", "Neu", None))
        self.button_open.setText(_translate("Form", "Öffnen", None))
        self.button_save.setText(_translate("Form", "Speichern", None))
        self.label.setText(_translate("Form", "Dateipfad", None))
        self.button_get_path.setText(_translate("Form", "...", None))

from PyQt4 import QtWebKit
