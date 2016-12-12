# -*- coding:utf-8 -*-
__author__ = 'Djj'

import sys
from PyQt4 import QtGui, QtCore

class MyGui(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(250, 50)

        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        # Create a combo box with some choices
        self.combo_color = QtGui.QComboBox()
        self.vbox.addWidget(self.combo_color)
        items = 'Red Yellow Purple'.split()
        self.combo_color.addItems(items)
        self.connect(self.combo_color, QtCore.SIGNAL('activated(QString)'), self.use_choice)

        # add a checkbox next to the combobox which (un-)locks the the combo-choice
        self.checkbox_color = QtGui.QCheckBox('Lock Choice', self)
        self.vbox.addWidget(self.checkbox_color)
        self.connect(self.checkbox_color, QtCore.SIGNAL('stateChanged(int)'), self.lock_choice)

    def use_choice(self, text):
        # do something very useful with the choice
        print 'The current choice is: {choice}'.format(choice=text)

    def lock_choice(self):
        if self.checkbox_color.isChecked():
            self.combo_color.setEnabled(False)
            print 'Choice {choice} locked'.format(choice=self.combo_color.currentText())
        else:
            self.combo_color.setEnabled(True)
            print 'Choice unlocked'


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mygui = MyGui()
    mygui.show()
    app.exec_()