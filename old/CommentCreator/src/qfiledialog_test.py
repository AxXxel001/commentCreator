#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we select a file with a
QtGui.QFileDialog and display its contents
in a QtGui.QTextEdit.

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4 import QtGui


class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.textEdit = QtGui.QPushButton("Push me")
        self.setCentralWidget(self.textEdit)

        self.textEdit.clicked.connect(self.showDialog)      
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()
        
    def showDialog(self):

        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data) 
                                
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()