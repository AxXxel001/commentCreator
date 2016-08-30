import sys
from os import sep
from PyQt4.QtGui import QApplication
from src import mainwindow

if __name__ == "__main__":
	print "los gehts"
	app = QApplication(sys.argv)
	window = mainwindow.CCMainWindow()
	sys.exit(app.exec_())