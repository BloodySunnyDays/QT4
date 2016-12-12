# -*- coding:utf-8 -*-
__author__ = 'Djj'

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
import ShowExcept


qtCreatorFile = "Table.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #去掉最大化
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        #无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)
        #无法拉伸
        self.setFixedSize(720,540)
        self.setupUi(self)
        d1 = [{'我':1,'你':2,'他':3},{'我':4,'你':'小鸟','他':6}]
        self.Btn_CreatTable.clicked.connect(lambda : ConToTable(d1,self.Mytable))
        # self.Btn_CreatTable.command=lambda : ConToTable(d1,self.Mytable)

def ConToTable(Adict,Table):
    Ls = []
    t_dict = {}
    t_List = []
    for n in range(0,len(Adict)):
        for k,v in Adict[n].items():
            t_dict[k.decode('utf-8')] = v
        t_List.append(t_dict)
        t_dict ={}

    for k,v in t_List[0].items():
        Ls.append(k)
    Table.setColumnCount(len(Ls))
    Table.setRowCount(len(t_List))
    Table.setHorizontalHeaderLabels(Ls)
    #隐藏水平表头
    # Table.horizontalHeader().setVisible(False)
    #隐藏垂直表头
    Table.verticalHeader().setVisible(False)
    #禁止修改
    Table.setEditTriggers(Table.NoEditTriggers)
    #颜色字体
    for x in range(Table.columnCount()):
        headItem = Table.horizontalHeaderItem(x)   #获得水平方向表头的Item对象
        headItem.setFont(QFont('song',10,QFont.Bold))                        #设置字体
        headItem.setBackgroundColor(QColor(0,60,10))      #设置单元格背景颜色
        headItem.setTextColor(QColor(200,111,30))         #设置文字颜色

    for x in range(0,len(Ls)):
        for y in range(0,len(t_List)):
            name = Ls[x]
            value = t_List[y][name]
            newItem = QTableWidgetItem(str(value).decode('utf-8'))
            #文字居中
            newItem.setTextAlignment(Qt.AlignCenter)
            Table.setItem(y,x,newItem)


    # widget2 = QWidget(window.Qwidget1,Qt.Window)
    message = ShowExcept.Cls_Message(window,str('大鸟').decode('utf-8'))
    # widget2 = QWidget(window.Qwidget1,Qt.Window)
    # widget2.setWidget(message)
    # widget2.show()
    # message = ShowExcept.Cls_Dialog(window.Qwidget1,str('大鸟').decode('utf-8'))
    message.show()
    message.exec_()




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


