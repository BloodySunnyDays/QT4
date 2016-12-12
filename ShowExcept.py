# -*- coding:utf-8 -*-
__author__ = 'Djj'

from PyQt4 import QtCore, QtGui,uic,Qt
import sys

# qtMessageFile = "ShowMessage.ui"
qtMessageFile = "ShowDialog.ui"

qtDialogFile = "WidgetDialog.ui"

Ui_MessageWin,QtBaseClass = uic.loadUiType(qtMessageFile)

Ui_DialogWin,Qt.Window = uic.loadUiType(qtDialogFile)

class Cls_Message(QtGui.QDialog, Ui_MessageWin):
    def __init__(self,cls_Qwidget,sMess):
        super(Cls_Message,self).__init__()
        # QtGui.QDialog.__init__(self)
        # Ui_MessageWin.__init__(self)
        self.setupUi(self)
        self.TE_Message.setPlainText(sMess)

class Cls_Dialog(QtGui.QWidget, Ui_DialogWin):
    def __init__(self,cls_Qwidget,sMess):
        # super(Cls_Dialog, self).__init__(cls_Qwidget)
        QtGui.QWidget.__init__(self)
        Ui_DialogWin.__init__(self)
        self.Form = QtGui.QWidget(cls_Qwidget,Qt.Window)
        self.setupUi(self)
        self.TE_Message.setPlainText(sMess)


# try:
#     a=b
#     b=c
# except Exception,ex:
#     app = QtGui.QApplication(sys.argv)
#     window = Cls_Message(str(ex))
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     window = Cls_Message()
#     window.show()
#     sys.exit(app.exec_())