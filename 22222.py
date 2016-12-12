# -*- coding:utf-8 -*-
__author__ = 'Djj'

from PyQt4.QtGui import (QMainWindow, QPushButton, QApplication,
                                     QVBoxLayout, QWidget)
from PyQt4.QtCore import (Qt, QObject, SIGNAL)
import anotherWindow
import sys

class OneWindow(QMainWindow):
    def __init__(self):
        super(OneWindow, self).__init__()
        self.setGeometry(100, 100, 600, 400)
        vLayout = QVBoxLayout()
        self.button = QPushButton("OK")
        vLayout.addWidget(self.button)
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)

        QObject.connect(self.button,SIGNAL("clicked()") , self.anotherWindow)

    def anotherWindow(self):
        print 'OK'
        another = anotherWindow.AnotherWindow()
        another.show()              #难道不是用这个show（）函数吗？
        another.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = OneWindow()
    w.show()
    app.exec_()




