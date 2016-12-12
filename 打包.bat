@echo off
F:\Python27WorkSp\QT4
pyinstaller -w  PrjTransDate.py

copy /y F:\Python27WorkSp\QT4\PrjTransDate.ui F:\Python27WorkSp\WebService_PDC\dist\PrjTransDate
copy /y F:\Python27WorkSp\QT4\WidgetDialog.ui F:\Python27WorkSp\WebService_PDC\dist\PrjTransDate

copy /y F:\Python27WorkSp\QT4\dist\Config.ini F:\Python27WorkSp\QT4\dist\PrjTransDate
copy /y F:\Python27WorkSp\QT4\dist\_mssql.pyd F:\Python27WorkSp\QT4\dist\PrjTransDate
md F:\Python27WorkSp\QT4\dist\PrjTransDate\log



