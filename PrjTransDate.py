# -*- coding:utf-8 -*-
__author__ = 'Djj'

import sys
from PyQt4 import uic,QtGui
from PyQt4.QtCore import Qt
import UnitConFunc as UF
import ConfigParser


sDir = UF.cur_file_dir() + '\\Config.ini'
config = ConfigParser.ConfigParser()
config.read(sDir)

sIP        = config.get("conn", "IP")
sDateBase  = config.get('conn', 'DateBase')
sUser      = config.get('conn', 'User')
sPassw     = config.get('conn', 'Paswd')
sWebSerIp  = config.get('conn', 'WebSerIp')
sDBType    = config.get('conn', 'DBType')
sParkCode  = config.get('conn', 'ParkCode')
sSleepTime = config.get('conn', 'sleeptime')
sFormatJson= config.get('conn', 'formatjson')

#数据库配置

# def WriteConfig(IP,DateBase,User,Paswd,WebSerIp,DBType,ParkCode,SleepTime):
#     try:
#         config.set("conn", "IP",IP)
#         config.set('conn', 'DateBase',DateBase)
#         config.set('conn', 'User',User)
#         config.set('conn', 'Paswd',Paswd)
#         if config.has_option('conn', 'WebSerIp'):
#             config.set('conn', 'WebSerIp',WebSerIp)
#         config.set('conn', 'DBType',DBType)
#         if config.has_option('conn', 'ParkCode'):
#             config.set('conn', 'ParkCode',ParkCode)
#         if config.has_option('conn', 'SleepTime'):
#             config.set('conn', 'SleepTime',SleepTime)
#         config.write(open(sDir, "w"))
#         UF.Show(window.ET_operatorText,'保存成功',True)
#     except:
#         UF.Show(window.ET_operatorText,'保存失败',True)

qtCreatorFile = "PrjTransDate.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        listDb = [
        self.tr('SQL Server'),
        self.tr('Oracl'),
        self.tr('MySQL'),
        ]
        self.cbbDatebase.clear()
        self.cbbDatebase.addItems(listDb)
        self.cbbDatebase.setCurrentIndex(int(sDBType))
        # self.cbbDatebase.currentIndexChanged.connect(lambda :UF.comboxchange(self.cbbDatebase))

        # self.Btn_Test.clicked.connect(lambda :UF.Cls_Dialog(str(UF.DBType)))
        # 测试代码
        # self.Btn_Test.clicked.connect(lambda :UF.Show(self.ET_operatorText,self.cbbDatebase.currentText(),False))
        self.Btn_Test.clicked.connect(lambda :UF.TestDB(self.ET_operatorText,self.cbbDatebase.currentIndex(),
                                                        self.ET_User.text(),self.ET_PassWord.text(),
                                                        self.ET_DbName.text(),self.ET_ip.text()))
        self.ET_ip.setText(sIP)
        self.ET_DbName.setText(sDateBase)
        self.ET_User.setText(sUser)
        self.ET_PassWord.setText(sPassw)
        self.Btn_Save.clicked.connect(lambda:showinfo(self))
        UF.CreateTabAndItems(self.tab_BD,self.ET_operatorText,config)
        self.Btn_AddDB.clicked.connect(lambda :UF.AddDBinfo(self.tab_BD,self.ET_operatorText,self.cbbDbInfoList,config))
        self.Btn_DelDB.clicked.connect(lambda :UF.DelDBinfo(self.tab_BD,self.ET_operatorText,self.cbbDbInfoList,config))
        UF.DBInfoUpadate(self.cbbDbInfoList,config)


        self.cbbDbInfoList.currentIndexChanged.connect(lambda :Change())
        def Change():
            UF.GColName = ''
            UF.GTable = ''
            clear()


        #动态下拉 可勾选 （未完成）测试代码
        self.pListWidget = QtGui.QListWidget()
        self.pLineEdit = QtGui.QLineEdit()
        for i in range(0,4):
            pItem = QtGui.QListWidgetItem(self.pListWidget)
            self.pListWidget.addItem(pItem)
            # pItem.setData('')
            pCheckBox = QtGui.QCheckBox()
            pCheckBox.setText('qter'+str(i))
            self.pListWidget.setItemWidget(pItem,pCheckBox)
            # pCheckBox.conncet(lambda :UF.stateChanged(self.pListWidget,pCheckBox))
        self.cbbTransfield.setModel(self.pListWidget.model())
        self.cbbTransfield.setView(self.pListWidget)
        self.cbbTransfield.setLineEdit(self.pLineEdit)
        self.pLineEdit.setReadOnly(True)
        #隐藏下拉框 暂时不用
        self.cbbTransfield.setVisible(False)

        #隐藏SQL语句  ET_SQL
        self.ET_SQL.setVisible(False)
        self.ET_Where.setVisible(False)

        # 菜单
        self.TableRule.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TableRule.customContextMenuRequested.connect(lambda :showContextMenu(self))

        def showContextMenu(self):  # 创建右键菜单
                self.TableRule.contextMenu = QtGui.QMenu(self)
                self.actionA = self.TableRule.contextMenu.addAction(u'删除')
                # self.actionA = self.view.contextMenu.exec_(self.mapToGlobal(pos))  # 1
                self.TableRule.contextMenu.popup(QtGui.QCursor.pos())  # 2菜单显示的位置
                self.actionA.triggered.connect(lambda :UF.DeleteRule('conn',self.TableRule,self.ET_operatorText))
                # self.view.contextMenu.move(self.pos())  # 3
                self.TableRule.contextMenu.show()


        #添加SQL按钮
        self.btn_AddSQL.clicked.connect(lambda :UF.AddSQL(self.ET_table.text(),self.ET_Key.text(),
                                                          self.ET_UpdateName.text(),self.ET_UpdateValue.text(),
                                                          self.ET_SQL.toPlainText(),self.ET_operatorText,
                                                          self.ET_SQL,self.ET_showUpdate,self.ET_Where))

        self.btn_AddRule.clicked.connect(lambda :UF.AddRule(self.cbbDbInfoList.currentText(),self.ET_operatorText,self.ET_SleepTime.text(),
                                                            self.ET_SQL.toPlainText(),self.ET_table.text(),self.ET_ColName.toPlainText(),
                                                            self.ET_table_Tag.text(),self.ET_ColName_Tag.toPlainText(),self.ET_Key.text(),
                                                            self.ET_UpdateName.text(),self.ET_UpdateValue.text(),self.TableRule,
                                                            self.ET_autoCol.text(),self.ET_seq.text(),self.ET_SpecialCol.text(),self.ET_SpecialRule.toPlainText()))
        self.btn_QryRule.clicked.connect(lambda :UF.QryRule('conn',self.TableRule,self.ET_operatorText))

        self.btn_Delete.clicked.connect(lambda :UF.DeleteRule('conn',self.TableRule,self.ET_operatorText))
        self.btn_Delete.setVisible(False)
        #清空
        self.btn_Clear.clicked.connect(lambda:clear())

        #获取字段
        self.btn_GetColName.clicked.connect(lambda:UF.GetColNames('conn',self.ET_table.text(),self.ET_ColName,self.ET_operatorText))
        self.btn_GetColName_Tag.clicked.connect(lambda:UF.GetColNames(self.cbbDbInfoList.currentText(),self.ET_table_Tag.text(),self.ET_ColName_Tag,self.ET_operatorText))

        self.btn_ChangeCols.clicked.connect(lambda :UF.ChangeCols(self.ET_ColName,self.ET_ColName_Tag,self.ET_operatorText))

        self.btn_TransStart.clicked.connect(lambda :UF.TransStart('conn',self.TableRule,self.ET_operatorText))




        def clear():
            window.ET_SQL.setPlainText('')
            window.ET_Where.setText('')
            window.ET_showUpdate.setText('')
            UF.GTable = ''
            UF.GColName = ''


        def showinfo(self):
            re = UF.WriteConfig('conn',self.ET_ip.text(),self.ET_DbName.text(),self.ET_User.text(),
                            self.ET_PassWord.text(),'',str(self.cbbDatebase.currentIndex()),'',3)
            if re == 1:
                UF.Show(window.ET_operatorText,'保存成功',True)
            else:
                UF.Show(window.ET_operatorText,'保存失败',True)







        # d1 = [{'我':1,'你':2,'他':3},{'我':4,'你':5,'他':6}]
        # self.Btn_CreatTable.clicked.connect(lambda : UF.ConToTable(d1,self.Mytable))
        # self.Btn_CreatTable.command=lambda : ConToTable(d1,self.Mytable)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())