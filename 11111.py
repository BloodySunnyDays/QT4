# -*- coding:utf-8 -*-
__author__ = 'Djj'


from PyQt4.Qt import *
from PyQt4.QtCore import  *
from PyQt4.QtGui import *


def main():
    print "main"


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    print type(Qt.WindowModal)
    widget1 = QWidget()
    widget1.resize(600,400)
    widget1.setStyleSheet(QString.fromUtf8("background:black"))


    widget2 = QWidget(widget1,Qt.Window)
    # widget2.setWindowModality(Qt.ApplicationModal)
    widget2.resize(400,200)
    widget2.setStyleSheet(QString.fromUtf8("background:red"))

    widget3 = QWidget(widget2,Qt.Window)
    # widget3.setWindowModality(Qt.ApplicationModal)
    widget3.setStyleSheet(QString.fromUtf8("background:white"))
    widget3.resize(300,100)

    widget1.show()
    widget2.show()
    widget3.show()
    app.exec_()
