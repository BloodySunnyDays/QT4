# -*- coding:utf-8 -*-
__author__ = 'Djj'

import sys
from PyQt4 import QtGui
import base64

# app =QtGui.QApplication(sys.argv)
# widget = QtGui.QWidget()
# widget.resize(250, 150)
# widget.setWindowTitle('PyQt')
# widget.show()
# sys.exit(app.exec_())

T ='s e n d i n f o '
s1 = base64.b64encode(T)
print s1

s = 'cwBlAG4AZABpAG4AZgBvAA=='
s2 = base64.b64decode(s)
print s2