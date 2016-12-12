# -*- coding:utf-8 -*-
__author__ = 'Djj'

from PyQt4  import QtGui,uic
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFont,QColor,QTableWidgetItem,QTextCursor
import sys,os
import ConfigParser
import DbIntf
import oracle_db
import MySQL_db
import json
import threading


qtDialogFile = "ShowDialog.ui"

Ui_DialogWin,Qt.Window = uic.loadUiType(qtDialogFile)

global DBType,GTable,GColName
DBType = 0
GTable = ''
GColName =''
Fconnet = False

def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

sDir = cur_file_dir() + '\\Config.ini'
config = ConfigParser.ConfigParser()
config.read(sDir)

def WriteConfig(section,IP,DateBase,User,Paswd,WebSerIp,DBType,ParkCode,SleepTime):
    try:
        config.set(section, "IP",str(IP))
        config.set(section, 'DateBase',DateBase)
        config.set(section, 'User',User)
        config.set(section, 'Paswd',Paswd)
        if config.has_option(section, 'WebSerIp'):
            config.set(section, 'WebSerIp',WebSerIp)
        config.set(section, 'DBType',DBType)
        if config.has_option(section, 'ParkCode'):
            config.set(section, 'ParkCode',ParkCode)
        if config.has_option(section, 'SleepTime'):
            config.set(section, 'SleepTime',SleepTime)
        config.write(open(sDir, "w"))
        return 1
    except:
        return 0


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
    Ls.sort()
    Table.setColumnCount(len(Ls))
    Table.setRowCount(len(t_List))
    Table.setHorizontalHeaderLabels(Ls)
    #隐藏水平表头
    # Table.horizontalHeader().setVisible(False)
    #隐藏垂直表头
    Table.verticalHeader().setVisible(False)
    #禁止修改
    Table.setEditTriggers(Table.NoEditTriggers)
    #整行选择
    Table.setSelectionBehavior(Table.SelectRows)
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
            newItem = QTableWidgetItem(str(value))
            #文字居中
            newItem.setTextAlignment(Qt.AlignCenter)
            Table.setItem(y,x,newItem)

def ShowExce(sEx):
    pass

def comboxchange(ComboBox):
    global DBType
    DBType = ComboBox.currentIndex() + 1

def Show(TextEdit,S,bNewLine):
    if TextEdit.document().lineCount() > 30:
        TextEdit.setPlainText('')
    if not bNewLine:
        TextEdit.setPlainText(str(S).decode('utf-8'))
    else:
        TextEdit.moveCursor(QTextCursor.End)
        TextEdit.append(str(S).decode('utf-8'))

def getDBSection(DBsection):
    for i,x in enumerate(DBsection):
        if x[:6] <> 'DbInfo':
            DBsection.remove(x)
            getDBSection(DBsection)
    return DBsection

def TestDB(LabMess,DBType,user,pw,dbName,Ip):
    global Fconnet
    Fconnet = False
    if DBType == 2:
        MySQL_db.engine = None
        sSQL = 'select 1 as Count '
        MySQL_db.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))

        try:
            # Show(LabMess,'数据库连接失败。',True)
            info =  MySQL_db.select(sSQL)
            if info[0]['COUNT'] == 1:
                Show(LabMess,'数据库连接成功。',True)
                Fconnet =True
            else:
                Show(LabMess,'数据库连接失败。',True)
        except Exception,ex:
            Show(LabMess,'数据库连接失败，',True)
    if DBType == 1:
        oracle_db.engine = None
        sSQL = 'select 1 as Count from dual '
        oracle_db.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            # Show(LabMess,'数据库连接失败。',True)
            info =  oracle_db.select(sSQL)
            if info[0]['COUNT'] == 1:
                Show(LabMess,'数据库连接成功。',True)
                Fconnet =True
            else:
                Show(LabMess,'数据库连接失败。',True)
        except Exception,ex:
            Show(LabMess,'数据库连接失败，',True)
    if DBType == 0:
        DbIntf.engine = None
        sSQL = 'select 1 as Count  '
        DbIntf.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            # Show(LabMess,'数据库连接失败。',True)
            info =  DbIntf.select(sSQL)
            if info[0]['COUNT'] == 1:
                Show(LabMess,'数据库连接成功。',True)
                Fconnet =True
            else:
                Show(LabMess,'数据库连接失败。',True)
        except Exception,ex:
            Show(LabMess,'数据库连接失败，',True)

def AddDBinfo(DBTab,optab,combox,Aconfig):
    DBsection = Aconfig.sections()
    DBlist = getDBSection(DBsection)
    page = len(DBlist) + 1
    Aconfig.add_section('DbInfo'+str(page))
    Aconfig.set('DbInfo'+str(page),'DBType',0)
    Aconfig.set('DbInfo'+str(page),'IP','')
    Aconfig.set('DbInfo'+str(page),'DateBase','')
    Aconfig.set('DbInfo'+str(page),'User','')
    Aconfig.set('DbInfo'+str(page),'Paswd','')
    Aconfig.write(open(sDir, "w"))
    CreateTabAndItems(DBTab,optab,Aconfig)
    DBInfoUpadate(combox,Aconfig)
    # Aconfig.read(sDir)
    Show(optab,'添加成功',True)

def DelDBinfo(DBTab,optab,combox,Aconfig):
    DBsection = Aconfig.sections()
    DBlist = getDBSection(DBsection)
    page = len(DBlist)
    if page ==1:
        Show(optab,'只剩一个不能再删拉！',True)
    else:
        Aconfig.remove_option('DbInfo'+str(page),'DBType')
        Aconfig.remove_option('DbInfo'+str(page),'IP')
        Aconfig.remove_option('DbInfo'+str(page),'DateBase')
        Aconfig.remove_option('DbInfo'+str(page),'User')
        Aconfig.remove_option('DbInfo'+str(page),'Paswd')
        Aconfig.remove_section('DbInfo'+str(page))
        Aconfig.write(open(sDir, "w"))
        CreateTabAndItems(DBTab,optab,Aconfig)
        DBInfoUpadate(combox,Aconfig)
        # Aconfig.read(sDir)
        Show(optab,'删除成功',True)

def DBInfoUpadate(Combox,Aconfig):
    Aconfig.read(sDir)
    DBsection = Aconfig.sections()
    DBlist = getDBSection(DBsection)
    Combox.clear()
    Combox.addItems(DBlist)

def ChangeTransType(TransType):
    if TransType == 0:
        pass
    else:
        pass

def stateChanged(pListWidget,pCheckBox):
    ncount = pListWidget.count()
    for i in range(0,ncount):
        pitem = pListWidget.item(i)
        pWidget = pListWidget.itemWidget(pitem)
        pCheckBox = pWidget

def QryRule(section,TableRule,LabMess):
    Ip        = config.get(str(section), "IP")
    dbName  = config.get(str(section), 'DateBase')
    user      = config.get(str(section), 'User')
    pw     = config.get(str(section), 'Paswd')
    sDBType    = config.get(str(section), 'DBType')

    if sDBType == '2':
        MySQL_db.engine = None
        MySQL_db.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            sSQL = 'select ip,dbname,Dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
            Dinfo = MySQL_db.select(sSQL)
            ConToTable(Dinfo,TableRule)
        except:
            Show(LabMess,'查询失败，',True)

    if sDBType == '1':
        oracle_db.engine = None
        oracle_db.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            sSQL = 'select ip,dbname,Dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
            Dinfo = oracle_db.select(sSQL)
            ConToTable(Dinfo,TableRule)
        except:
            Show(LabMess,'查询失败，',True)

    if sDBType == '0':
        DbIntf.engine = None
        DbIntf.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            sSQL = 'select ip,dbname,Dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
            Dinfo = DbIntf.select(sSQL)
            ConToTable(Dinfo,TableRule)
        except:
            Show(LabMess,'查询失败，',True)

def DeleteRule(section,TableRule,LabMess):
    Ip        = config.get(str(section), "IP")
    dbName  = config.get(str(section), 'DateBase')
    user      = config.get(str(section), 'User')
    pw     = config.get(str(section), 'Paswd')
    DBType    = config.get(str(section), 'DBType')
    nRec = TableRule.currentRow()
    if nRec < 0:
        Show(LabMess,'未选择记录，',True)

    sIP= str(TableRule.item(nRec,5).text())
    sColName= str(TableRule.item(nRec,1).text())
    sDBName= str(TableRule.item(nRec,2).text())
    sDBType= str(TableRule.item(nRec,3).text())
    sTableName= str(TableRule.item(nRec,12).text())

    if DBType == '2':
        MySQL_db.engine = None
        MySQL_db.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            sSQL = "delete from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and ColName = ?"
            info =  MySQL_db.update(str(sSQL.encode('gbk')),sIP,sDBName,str(sDBType),str(sTableName),str(sColName))
            if info > 0:
                Show(LabMess,'删除成功，',True)
                TableRule.removeRow(nRec)

            sSQL = 'select ip,dbname,user,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
            Dinfo = MySQL_db.select(sSQL)
            if len(Dinfo)>0:
              ConToTable(Dinfo,TableRule)
        except:
            Show(LabMess,'删除失败，',True)

    if DBType == '1':
        oracle_db.engine = None
        oracle_db.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            sSQL = "delete from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and ColName = ?"
            info =  oracle_db.update(str(sSQL.encode('gbk')),sIP,sDBName,sDBType,sTableName,sColName)
            Show(LabMess,'删除成功，',True)
            TableRule.removeRow(nRec)

            sSQL = 'select ip,dbname,user,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
            Dinfo = oracle_db.select(sSQL)
            if len(Dinfo)>0:
              ConToTable(Dinfo,TableRule)
        except:
            Show(LabMess,'删除失败，',True)

    if DBType == '0':
        DbIntf.engine = None
        DbIntf.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        try:
            sSQL = "delete from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and ColName = ?"
            info =  DbIntf.update(str(sSQL.encode('gbk')),sIP,sDBName,str(sDBType),str(sTableName),str(sColName))
            if info > 0:
                Show(LabMess,'删除成功，',True)
                TableRule.removeRow(nRec)

            sSQL = 'select ip,dbname,user,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
            Dinfo = DbIntf.select(sSQL)
            if len(Dinfo)>0:
              ConToTable(Dinfo,TableRule)
        except:
            Show(LabMess,'删除失败，',True)



# 创建全局ThreadLocal对象:
local_DbLink = threading.local()


def TransStart(section,TableRule,LabMess):
    Ip        = config.get(str(section), "IP")
    dbName  = config.get(str(section), 'DateBase')
    user      = config.get(str(section), 'User')
    pw     = config.get(str(section), 'Paswd')
    DBType    = config.get(str(section), 'DBType')

    threads = []


    if DBType == '2':
        ComDbIntf = MySQL_db

    if DBType == '1':
        ComDbIntf = oracle_db

    if DBType == '0':
        ComDbIntf = DbIntf

    try:
        ComDbIntf.engine = None
        ComDbIntf.create_engine(user=str(user), password=str(pw), database=str(dbName), host=str(Ip))
        sSQL = 'select * from Trans_Rule'
        Dinfo = ComDbIntf.select(sSQL)
    except:
        Show(LabMess,'查询失败，',True)

    if len(Dinfo) > 0:
        for i in range(len(Dinfo)):
            sIp        = Dinfo[i]['IP']
            sdbName  = Dinfo[i]['DBNAME']
            suser      = Dinfo[i]['DBUSER']
            spw     = Dinfo[i]['PASSWORD']
            sDBType    = Dinfo[i]['DBTYPE']
            stable     = Dinfo[i]['TABLENAME']
            stable_Tag     = Dinfo[i]['TABLENAME_TAG']
            sCols      = Dinfo[i]['COLNAME']
            sUpValue      = Dinfo[i]['UPVALUE']
            supsql     = Dinfo[i]['UPSQL']
            ssql     = Dinfo[i]['SQL']
            ssql_tag     = Dinfo[i]['SQL_TAG']
            nSleeptime     = Dinfo[i]['SLEEPTIME']
            sKeyCol     = Dinfo[i]['KEYCOL']

            if DBType == '2':
                ssql_select = 'select ' + ssql + ' from ' + stable + ' where '+ sCols +' <> ' + sUpValue  \
                              + ' order by ' + sKeyCol + ' limit 30 '


            if DBType == '1':
                ssql_select = 'select ' + ssql + ' from ' + stable + ' where nvl('+ sCols +',0) <> ' + sUpValue + ' and rownum < 31 ' \
                           + ' order by ' + sKeyCol

            if DBType == '0':
                ssql_select = 'select top 30 ' + ssql + ' from ' + stable + ' where ISNULL('+ sCols +',0) <> ' + sUpValue  \
                           + ' order by ' + sKeyCol

            if sDBType == '2':
                ComDbIntf_Tag = MySQL_db

            if sDBType == '1':
                ComDbIntf_Tag = oracle_db

            if sDBType == '0':
                ComDbIntf_Tag = DbIntf
            try:
                ComDbIntf_Tag.engine = None
                ComDbIntf_Tag.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
                t1 = threading.Thread(target=TransThread,args=(ComDbIntf,ComDbIntf_Tag,ssql_select,stable_Tag,ssql_tag,supsql,sKeyCol,nSleeptime,sDBType,LabMess,))
                threads.append(t1)

            except:
                Show(LabMess,'目标数据库连接失败，',True)

    for th in threads:
        th.start()
        th.join()

def TransThread(ComDbIntf,ComDbIntf_Tag,sql_select,table_tag,sql_tag,upsql,keycol,sleeptime,DBType_Tag,LabMess):
    local_DbLink.Db = ComDbIntf
    local_DbLink.DbTag = ComDbIntf_Tag
    local_DbLink.sql_select = sql_select
    local_DbLink.table_tag = table_tag
    local_DbLink.sql_tag =sql_tag
    local_DbLink.upsql = upsql
    local_DbLink.keycol = keycol
    local_DbLink.sleeptime = sleeptime
    local_DbLink.DBType_Tag = DBType_Tag

    Dinfo1 = local_DbLink.Db.select(local_DbLink.sql_select)

    if len(Dinfo1) > 1 :
        for i in range(len(Dinfo1)):
            #获取关键字段
            sID = Dinfo1[i][local_DbLink.keycol]
            #完成更新语句
            local_DbLink.upsql = local_DbLink.upsql + ' where ' + local_DbLink.keycol + ' = ' + str(sID)
            #同步到目标数据库
            sInsertValues =''

            if local_DbLink.DBType_Tag == '2':
                list = str(local_DbLink.sql_tag).split(',')
                sValues  = Dinfo1[i]

                for n in range(len(list)):
                    strs = list[n]
                    if isinstance(sValues[strs],basestring):
                        name = sValues[strs].decode('gbk')
                    else:
                        name = sValues[strs]
                    sValues[strs] = name

                try:
                    info =  local_DbLink.DbTag.insert(str(local_DbLink.table_tag),**sValues)
                    if info == 1:
                        Show(LabMess,'同步到表:'+str(local_DbLink.table_tag)+'成功,关键字段:'+str(local_DbLink.keycol)+
                             ' ='+str(sID),True)
                    else:
                        pass
                        # Show(LabMess,'添加失败。',True)
                except Exception,ex:
                    pass
                    # Show(LabMess,'添加失败，',True)


            if local_DbLink.DBType_Tag == '1':
                pass



                # sSQL = "insert into Trans_Rule (Ip,dbName,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,SQL,tableName_Tag,SQL_Tag,KeyCol,ColName,UPvalue) " \
                #        "values('"+str(Ip)+"','"+ str(dbName) +"','"+ str(user) + "','"\
                #    + str(pw) +"','"+ str(DBType) +"','"+ str(sleeptime) +"','"+ str(updateSQL).upper() +"','"+ str(sTable) +"','"\
                #    + str(SQL).upper() +"','"+ str(sTable_Tag) +"','"+ str(SQL_Tag).upper() +"','"\
                #    + str(KeyCol).upper() +"','"+ str(ColName).upper() +"','"+ str(UPvalue) +"')"
                # try:
                #     info =  oracle_db.update(sSQL)
                #     if info == 1:
                #         Show(LabMess,'添加成功。',True)
                #         sSQL = 'select ip,dbname,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue from Trans_Rule'
                #         Dinfo = oracle_db.select(sSQL)
                #
                #         ConToTable(Dinfo,TableRule)
                #     else:
                #         Show(LabMess,'添加失败。',True)
                # except Exception,ex:
                #     Show(LabMess,'添加失败，',True)

            if local_DbLink.DBType_Tag == '0':
                sSQL_Insert = ''



    # sSQL = 'select * from Trans_Rule'
    # Dinfo2 = local_DbLink.DbTag.select(sSQL)



def AddRule(section,LabMess,sleeptime,updateSQL,sTable,SQL,sTable_Tag,SQL_Tag,KeyCol,ColName,UPvalue,TableRule,autoCol,seq,SpecialCol,SpecialRule):
    from collections import Counter
    global Fconnet
    Fconnet = False
    if updateSQL == '':
        Show(LabMess,'没有添加更新条件',True)
        return 0
    if SQL == '':
        Show(LabMess,'没有获取字段',True)
    if SQL_Tag == '':
        Show(LabMess,'没有获取目标字段',True)
    if sTable == '':
        Show(LabMess,'没有输入表名',True)
    if sTable_Tag == '':
        Show(LabMess,'没有输入目标表名',True)
        return 0
    # if SQL.find(ColName) < 0:
    #     Show('更新关键字'+str(ColName)+'不在字段中!')
    if str(SQL).find(str(KeyCol).upper()) < 0:
        Show(LabMess,'主键'+str(KeyCol)+'不在字段中!',True)
        return 0

    list1 = str(SQL).split(',')
    list2 = str(SQL_Tag).split(',')
    if len(list1) <> len(list2):
        Show(LabMess,'字段数不一致',True)
        return 0
    CountDict1 = Counter(list1)
    CountDict2 = Counter(list2)

    for k,v in CountDict1.iteritems():
        if v > 1:
            Show(LabMess,'同步字段'+k +'重复了,请检查',True)
            return 0

    for k,v in CountDict2.iteritems():
        if v > 1:
            Show(LabMess,'目标字段'+k +'重复了,请检查',True)
            return 0

    #等待保存的数据库信息
    Ip        = config.get(str(section), "IP")
    dbName  = config.get(str(section), 'DateBase')
    user      = config.get(str(section), 'User')
    pw     = config.get(str(section), 'Paswd')
    DBType    = config.get(str(section), 'DBType')
    #数据库配置
    sIp        = config.get('conn', "IP")
    sdbName  = config.get('conn', 'DateBase')
    suser      = config.get('conn', 'User')
    spw     = config.get('conn', 'Paswd')
    sDBType    = config.get('conn', 'DBType')
    if sDBType == '2':
        MySQL_db.engine = None
        sSQL = 'Create Table If Not Exists Trans_Rule(Ip varchar(32), '\
                'dbName varchar(32),'\
                'dbuser varchar(32),'\
                'passWord varchar(32),'\
                'DBType   varchar(8),'\
                'SleepTime   varchar(8),'\
                'UPSQL    varchar(1024),'\
                'tableName    varchar(32),'\
                '`SQL`    varchar(1024),'\
                'SQL_Tag    varchar(1024),'\
                'tableName_Tag    varchar(32),'\
                'KeyCol      varchar(32),'\
                'ColName      varchar(32),'\
                'UPvalue      varchar(32),'\
                'autoCol      varchar(32),'\
                'seq          varchar(32),'\
                'SpecialCol   varchar(32),'\
                'SpecialRule  varchar(1024) );'
        MySQL_db.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
        try:
            info =  MySQL_db.update(sSQL)
            # Show(LabMess,'表创建成功。',True)
            Fconnet =True
        except Exception,ex:
            Show(LabMess,'表创建失败，',True)

        #检查是否存在
        # sSQL = "select count(1) as Count from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and ColName = ? and tableName_Tag=? "
        sSQL = "select count(1) as Count from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and tableName_Tag=? "
        try:
            # info =  MySQL_db.select(str(sSQL.encode('gbk')),Ip,dbName,str(DBType),str(sTable),str(ColName),str(sTable_Tag))
            info =  MySQL_db.select(str(sSQL.encode('gbk')),Ip,dbName,str(DBType),str(sTable),str(sTable_Tag))
            if info[0]['COUNT'] > 0:
                Show(LabMess,'已存在相同的规则。',True)
                bAdd = False
            else:
                bAdd = True
        except Exception,ex:
            bAdd = False
            Show(LabMess,'添加失败，',True)

        #插入
        # sSQL = "insert into Trans_Rule values('"+str(Ip)+"','"+ str(dbName) +"','"+ str(user) + "','"\
        #        + str(pw) +"',"+ sDBType +","+ sleeptime +",'"+ str(updateSQL) +"','"+ str(sTable) +"','"\
        #        + str(KeyCol) +"','"+ str(ColName) +"','"+ str(UPvalue) +"');"
        # u1 = dict(Ip=str(Ip), dbName=str(dbName), user=str(user), passWord=str(pw), DBType=sDBType,SleepTime=sleeptime
        #           ,UPSQL=str(updateSQL),tableName=str(sTable),KeyCol=str(KeyCol),ColName=str(ColName),UPvalue=str(UPvalue))
        if bAdd == True:
            sSQL = "insert into Trans_Rule values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            try:
                info =  MySQL_db.update(str(sSQL.encode('gbk')),Ip,dbName,user,pw,str(DBType),str(sleeptime),str(updateSQL).upper(),
                                        str(sTable),str(SQL).upper(),str(SQL_Tag).upper(),str(sTable_Tag),str(KeyCol).upper(),str(ColName).upper(),str(UPvalue),
                                        str(autoCol).upper(),str(seq),str(SpecialCol).upper(),str(SpecialRule))
                if info == 1:
                    Show(LabMess,'添加成功。',True)
                    sSQL = 'select ip,dbname,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
                    Dinfo = MySQL_db.select(sSQL)

                    ConToTable(Dinfo,TableRule)
                else:
                    Show(LabMess,'添加失败。',True)
            except Exception,ex:
                Show(LabMess,'添加失败，',True)

    if sDBType == '1':
        oracle_db.engine = None

        sSQL = 'select count(*) as count from user_tables where table_name = ? '
        oracle_db.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
        try:
            N =  oracle_db.select(str(sSQL.encode('gbk')),'TRANS_RULE')
            if N[0]['COUNT'] <= 0:
                sSQL = "Create Table  Trans_Rule(Ip varchar(32), "\
                "dbName varchar(32),"\
                "dbuser varchar(32),"\
                "passWord varchar(32),"\
                "DBType   varchar(16),"\
                "SleepTime   varchar(16),"\
                "UPSQL    varchar(1024),"\
                "tableName    varchar(32),"\
                "SQL    varchar(1024),"\
                "SQL_Tag    varchar(1024),"\
                "tableName_Tag    varchar(32),"\
                "KeyCol      varchar(32),"\
                "ColName      varchar(32),"\
                "UPvalue      varchar(32),"\
                "autoCol      varchar(32),"\
                "seq          varchar(32),"\
                "SpecialCol   varchar(32),"\
                "SpecialRule  varchar(1024) )"
                try:
                    info =  oracle_db.update(sSQL)
                except Exception,ex:
                    Show(LabMess,'表创建失败，',True)
        except Exception,ex:
            Show(LabMess,'表创建失败，',True)

        #检查是否存在
        sSQL = "select count(1) as Count from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and ColName = ?"
        try:
            info =  oracle_db.select(str(sSQL.encode('gbk')),Ip,dbName,str(DBType),str(sTable),str(ColName))
            if info[0]['COUNT'] > 0:
                Show(LabMess,'已存在相同的规则。',True)
                bAdd = False
            else:
                bAdd = True
        except Exception,ex:
            bAdd = False
            Show(LabMess,'添加失败，',True)


        if bAdd == True:
            sSQL = "insert into Trans_Rule (Ip,dbName,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,SQL,tableName_Tag,SQL_Tag,KeyCol,ColName,UPvalue,"\
                    "autoCol,seq,SpecialCol,SpecialRule) " \
                   "values('"+str(Ip)+"','"+ str(dbName) +"','"+ str(user) + "','"\
               + str(pw) +"','"+ str(DBType) +"','"+ str(sleeptime) +"','"+ str(updateSQL).upper() +"','"+ str(sTable) +"','"\
               + str(SQL).upper() +"','"+ str(sTable_Tag) +"','"+ str(SQL_Tag).upper() +"','"\
               + str(KeyCol).upper() +"','"+ str(ColName).upper() +"','"+ str(UPvalue) +"','"\
               + str(autoCol).upper() +"','"+ str(seq) +"','" + str(SpecialCol).upper() +"','" + str(SpecialRule)  +"')"
            try:
                info =  oracle_db.update(sSQL)
                if info == 1:
                    Show(LabMess,'添加成功。',True)
                    sSQL = 'select ip,dbname,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
                    Dinfo = oracle_db.select(sSQL)

                    ConToTable(Dinfo,TableRule)
                else:
                    Show(LabMess,'添加失败。',True)
            except Exception,ex:
                Show(LabMess,'添加失败，',True)

    if sDBType == '0':
        DbIntf.engine = None

        sSQL = 'SELECT count(1) as count FROM    sysobjects WHERE   xtype= ? and name = ? '
        DbIntf.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
        try:
            N =  DbIntf.select(str(sSQL.encode('gbk')),'U','TRANS_RULE')
            if N[0]['COUNT'] <= 0:
                sSQL = "Create Table  Trans_Rule(Ip varchar(32), "\
                "dbName varchar(32),"\
                "dbuser varchar(32),"\
                "passWord varchar(32),"\
                "DBType   varchar(16),"\
                "SleepTime   varchar(16),"\
                "UPSQL    varchar(1024),"\
                "tableName    varchar(32),"\
                "SQL    varchar(1024),"\
                "SQL_Tag    varchar(1024),"\
                "tableName_Tag    varchar(32),"\
                "KeyCol      varchar(32),"\
                "ColName      varchar(32),"\
                "UPvalue      varchar(32),"\
                "autoCol      varchar(32),"\
                "seq          varchar(32),"\
                "SpecialCol   varchar(32),"\
                "SpecialRule  varchar(1024) )"
                try:
                    info =  DbIntf.update(sSQL)
                except Exception,ex:
                    Show(LabMess,'表创建失败，',True)
        except Exception,ex:
            Show(LabMess,'表创建失败，',True)

        #检查是否存在
        sSQL = "select count(1) as Count from Trans_Rule where Ip = ? and dbName = ? and DBType = ? and tableName = ? and ColName = ?"
        try:
            info =  DbIntf.select(str(sSQL.encode('gbk')),Ip,dbName,str(DBType),str(sTable),str(ColName))
            if info[0]['COUNT'] > 0:
                Show(LabMess,'已存在相同的规则。',True)
                bAdd = False
            else:
                bAdd = True
        except Exception,ex:
            bAdd = False
            Show(LabMess,'添加失败，',True)


        if bAdd == True:
            sSQL = "insert into Trans_Rule (Ip,dbName,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,SQL,tableName_Tag,SQL_Tag,KeyCol,ColName,UPvalue, " \
                   "autoCol,seq,SpecialCol,SpecialRule)"\
                   "values('"+str(Ip)+"','"+ str(dbName) +"','"+ str(user) + "','"\
               + str(pw) +"','"+ str(DBType) +"','"+ str(sleeptime) +"','"+ str(updateSQL).upper() +"','"+ str(sTable) +"','"\
               + str(SQL).upper() +"','"+ str(sTable_Tag) +"','"+ str(SQL_Tag).upper() +"','"\
               + str(KeyCol).upper() +"','"+ str(ColName).upper() +"','"+ str(UPvalue) +"','"\
               + str(autoCol).upper() +"','"+ str(seq) +"','" + str(SpecialCol).upper() +"','" + str(SpecialRule)  +"')"
            try:
                info =  DbIntf.update(sSQL)
                if info == 1:
                    Show(LabMess,'添加成功。',True)
                    sSQL = 'select ip,dbname,dbuser,passWord,DBType,SleepTime,UPSQL,tableName,KeyCol,ColName,UPvalue,autoCol,seq,SpecialCol,SpecialRule from Trans_Rule'
                    Dinfo = DbIntf.select(sSQL)

                    ConToTable(Dinfo,TableRule)
                else:
                    Show(LabMess,'添加失败。',True)
            except Exception,ex:
                Show(LabMess,'添加失败，',True)

def GetColNames(section,ET_Table,ET_ColName,LabMess):
    #数据库配置
    sIp        = config.get(str(section), "IP")
    sdbName  = config.get(str(section), 'DateBase')
    suser      = config.get(str(section), 'User')
    spw     = config.get(str(section), 'Paswd')
    sDBType    = config.get(str(section), 'DBType')
    try:
        if sDBType == '0':
            DbIntf.engine = None

            sSQL = 'SELECT column_name FROM INFORMATION_SCHEMA.columns WHERE TABLE_NAME= ? '
            DbIntf.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
            ColNames =  DbIntf.select(str(sSQL.encode('gbk')),str(ET_Table))

        if sDBType == '1':
            oracle_db.engine = None

            sSQL = 'select COLUMN_NAME from user_tab_cols where  table_name =upper(?) '
            oracle_db.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
            ColNames =  oracle_db.select(str(sSQL.encode('gbk')),str(ET_Table))

        if sDBType == '2':
            MySQL_db.engine = None

            sSQL = 'select COLUMN_NAME from information_schema.COLUMNS where table_name = ? '
            MySQL_db.create_engine(user=str(suser), password=str(spw), database=str(sdbName), host=str(sIp))
            ColNames =  MySQL_db.select(str(sSQL.encode('gbk')),str(ET_Table))


        if len(ColNames) ==0:
            Show(LabMess,'获取字段失败，',True)
            return 0
        data_string = ''
        for colname in ColNames:
            name = colname['COLUMN_NAME'].decode('gbk')
            colname['COLUMN_NAME'] = name

        data_string =  ','.join([colname['COLUMN_NAME'] for colname in ColNames])

        # data_string = 'select ' + data_string + 'from ' + str(ET_Table)

        # data_string = json.dumps(ColNames, ensure_ascii=False)
        ET_ColName.setPlainText(data_string)

    except Exception,ex:
        Show(LabMess,'获取字段失败，',True)

def ChangeCols(ET_ColName,ET_ColName_Tag,LabMess):
    if ET_ColName == '':
        Show(LabMess,'没有获取字段',True)
        return 0
    if ET_ColName_Tag == '':
        Show(LabMess,'没有获取目标字段',True)
        return 0
    list1 = str(ET_ColName.toPlainText()).split(',')
    list2 = str(ET_ColName_Tag.toPlainText()).split(',')
    #取差
    # listdiff = list(set(list2).difference(set(list1)))

    if len(list1) <> len(list2):
        Show(LabMess,'字段数不一致',True)
        return 0
    ssql = ''
    listc = []
    for v in range(len(list1)):
        if list1[v] == list2[v]:
            listc.append(list1[v])
        else:
            if list1[v].find(' as ') > 0 :
                listc.append(list1[v])
                continue
            listc.append('%s as %s' %(list1[v],list2[v]))

    ssql =  ','.join([colname for colname in listc])

    ET_ColName.setPlainText(ssql)




def CreateTabAndItems(MainTab,OpTab,config):
        MainTab.clear()
        DBsection = config.sections()
        DBlist = getDBSection(DBsection)

        newtb = locals()
        newLab1 = locals()
        newLab2 = locals()
        newLab3 = locals()
        newLab4 = locals()
        newLab5 = locals()
        #下拉
        newComDbType = locals()
        #文本框
        newET_IP = locals()
        newET_DbName = locals()
        newET_user = locals()
        newET_Passw = locals()
        #按钮
        newBtn_Test = locals()
        newBtn_Save = locals()

        for i in xrange(1,len(DBlist)+1):

            sIP        = config.get(DBlist[i-1], "IP")
            sDateBase  = config.get(DBlist[i-1], 'DateBase')
            sUser      = config.get(DBlist[i-1], 'User')
            sPassw     = config.get(DBlist[i-1], 'Paswd')
            sDBType    = config.get(DBlist[i-1], 'DBType')

            newtb['newtb%s' % i] = QtGui.QWidget()
            newLab1['newLab1%s' % i] = QtGui.QLabel(newtb['newtb%s' % i])
            newLab2['newLab2%s' % i] = QtGui.QLabel(newtb['newtb%s' % i])
            newLab3['newLab3%s' % i] = QtGui.QLabel(newtb['newtb%s' % i])
            newLab4['newLab4%s' % i] = QtGui.QLabel(newtb['newtb%s' % i])
            newLab5['newLab5%s' % i] = QtGui.QLabel(newtb['newtb%s' % i])


            newComDbType['newComDbType%s' % i] = QtGui.QComboBox(newtb['newtb%s' % i])
            newComDbType['newComDbType%s' % i].resize(160,22)
            newET_IP['newET_IP%s' % i] = QtGui.QLineEdit(newtb['newtb%s' % i])
            newET_IP['newET_IP%s' % i].resize(160,21)
            newET_DbName['newET_DbName%s' % i] = QtGui.QLineEdit(newtb['newtb%s' % i])
            newET_DbName['newET_DbName%s' % i].resize(160,21)
            newET_user['newET_user%s' % i] = QtGui.QLineEdit(newtb['newtb%s' % i])
            newET_user['newET_user%s' % i].resize(160,21)
            newET_Passw['newET_Passw%s' % i] = QtGui.QLineEdit(newtb['newtb%s' % i])
            newET_Passw['newET_Passw%s' % i].resize(160,21)
            newET_Passw['newET_Passw%s' % i].setEchoMode(QtGui.QLineEdit.Password)
            #赋值
            newET_IP['newET_IP%s' % i].setText(sIP)
            newET_DbName['newET_DbName%s' % i].setText(sDateBase)
            newET_user['newET_user%s' % i].setText(sUser)
            newET_Passw['newET_Passw%s' % i].setText(sPassw)

            listDb = [
            'SQL Server',
            'Oracl',
            'MySQL',
            ]
            newComDbType['newComDbType%s' % i].clear()
            newComDbType['newComDbType%s' % i].addItems(listDb)
            newComDbType['newComDbType%s' % i].setCurrentIndex(int(sDBType))

            #按钮
            newBtn_Test['newBtn_Test%s'% i] = QtGui.QPushButton(newtb['newtb%s' % i])
            newBtn_Test['newBtn_Test%s'% i].resize(93,28)
            newBtn_Save['newBtn_Save%s'% i] = QtGui.QPushButton(newtb['newtb%s' % i])
            newBtn_Save['newBtn_Save%s'% i].resize(93,28)

            y = 32
            x = 90
            n =0
            m =1
            newLab1['newLab1%s' % i].setText(u'数据库类型：')
            newLab1['newLab1%s' % i].move(10,10+y*n)
            #下拉
            newComDbType['newComDbType%s' % i].move(10+x*m,10+y*n)
            n+=1
            newLab2['newLab2%s' % i].setText(u'数据库地址：')
            newLab2['newLab2%s' % i].move(10,10+y*n)
            newET_IP['newET_IP%s' % i].move(10+x*m,10+y*n)
            n+=1
            newLab3['newLab3%s' % i].setText(u'数据库名称：')
            newLab3['newLab3%s' % i].move(10,10+y*n)
            newET_DbName['newET_DbName%s' % i].move(10+x*m,10+y*n)
            n+=1
            newLab4['newLab4%s' % i].setText(u'数据库用户：')
            newLab4['newLab4%s' % i].move(10,10+y*n)
            newET_user['newET_user%s' % i].move(10+x*m,10+y*n)
            n+=1
            newLab5['newLab5%s' % i].setText(u'数据库密码：')
            newLab5['newLab5%s' % i].move(10,10+y*n)
            newET_Passw['newET_Passw%s' % i].move(10+x*m,10+y*n)

            #按钮
            newBtn_Test['newBtn_Test%s'% i].setText(u'测试')
            newBtn_Test['newBtn_Test%s'% i].move(23,170)
            newBtn_Test['newBtn_Test%s'% i].clicked.connect(lambda :TestDbOnTab())
            newBtn_Save['newBtn_Save%s'% i].setText(u'记住设置')
            newBtn_Save['newBtn_Save%s'% i].move(155,170)
            newBtn_Save['newBtn_Save%s'% i].clicked.connect(lambda:showinfo())
            def TestDbOnTab():
                n = MainTab.currentIndex() + 1
                TestDB(OpTab,newComDbType['newComDbType%s' % n].currentIndex(),
                                        newET_user['newET_user%s' % n].text(),newET_Passw['newET_Passw%s' % n].text(),
                                        newET_DbName['newET_DbName%s' % n].text(),newET_IP['newET_IP%s' % n].text())

            def showinfo():
                n = MainTab.currentIndex() + 1
                re = WriteConfig(DBlist[n-1],newET_IP['newET_IP%s' % n].text(),
                                            newET_DbName['newET_DbName%s' % n].text(),
                                            newET_user['newET_user%s' % n].text(),
                                            newET_Passw['newET_Passw%s' % n].text(),'',
                                            str(newComDbType['newComDbType%s' % n].currentIndex()),'',3)
                if re == 1:
                    Show(OpTab,'保存成功',True)
                else:
                    Show(OpTab,'保存失败',True)

                # if re == 1:
                #     mes = Cls_Dialog(u'保存成功')
                #     mes.show()
                # else:
                #     mes = Cls_Dialog(u'保存失败')
                #     mes.show()

            MainTab.addTab(newtb['newtb%s' % i],'DBinfo'+str(i))

def AddSQL(Table,Key,ColName,ColValue,sSQL,OpTab,SQLEdt,showUpdate,WhereEdt):
    global GTable,GColName
    if Table == '':
        Show(OpTab,'请输入表名',True)
        return 0
    if Key == '':
        Show(OpTab,'请输入键值',True)
        return 0
    if ColName == '':
        Show(OpTab,'请输入更新字段',True)
        return 0
    if ColValue == '':
        Show(OpTab,'请输入更新后的值',True)
        return 0
    if (GTable ==  Table) and (GColName == ColName):
        Show(OpTab,'相同的表名和值',True)
        return 0

    if sSQL =='':
        TempSQL = 'update ' + str(Table) + ' set ' + str(ColName) + ' = ' + str(ColValue)
    else:
        TempSQL = sSQL + ',' +str(ColName) + ' = ' + str(ColValue)

    TempWhere = ' where ' + str(Key) + ' = #WHERE# '
    SQLEdt.setPlainText(TempSQL)
    WhereEdt.setText(TempWhere)
    showUpdate.append(ColName + '   ' + ColValue)
    GTable = Table
    GColName =ColName



class Cls_Dialog(QtGui.QWidget, Ui_DialogWin):
    def __init__(self,sMess):
        super(Cls_Dialog,self).__init__()
        # QtGui.QWidget.__init__(self)
        # Ui_DialogWin.__init__(self)
        self.setupUi(self)
        self.TE_Message.setPlainText(sMess)
        self.Btn_OK.clicked.connect(lambda :self.close())

