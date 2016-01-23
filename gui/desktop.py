# -*- coding: utf-8 -*-
from login import LoginPage
from user import User
from PyQt4 import Qt, QtGui, QtCore, QtSql
import numpy as np
import pandas as pd


class FwmDesktop(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initDB()
        login = LoginPage()
        if login.exec_():
            self.user = User(str(login.username.text()))
            self.initFromDB()
            self.createAction()
            self.createMenu()

            layout = QtGui.QVBoxLayout()
            self.centralWidget = QtGui.QWidget()
            self.centralWidget.setLayout(layout)
            self.setCentralWidget(self.centralWidget)
            self.resize(800, 600)
            self.setWindowTitle(u'家族信托投资管理平台 - {0}'.format(self.user.name))

            self.show()
        else:
            QtGui.qApp.quit()

    def initDB(self, host='caitcfid.mysql.rds.aliyuncs.com', port=3306, dbname='fwm'):
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(host)
        self.db.setPort(port)
        self.db.setDatabaseName(dbname)
        self.db.setUserName('hewei')
        self.db.setPassword('wehea1984')
        if not self.db.open():
            raise Exception(u'无法连接数据库')

    def initFromDB(self):
        self.loadAccounts()
        self.loadHolidays()

    def createMenu(self):
        self.mb = self.menuBar()
        m1 = self.mb.addMenu(u'&系统')
        m1.addAction(self.holAction)
        m1.addAction(self.exitAction)

        m2 = self.mb.addMenu(u'&交易')
        m2.addAction(self.addCash)

        m3 = self.mb.addMenu(u'&帮助')
        m3.addAction(self.aboutAction)

    def createAction(self):
        self.exitAction = QtGui.QAction(QtGui.QIcon(r'icons\exit.png'), u'退出', self, triggered=QtGui.qApp.quit)
        self.holAction = QtGui.QAction(QtGui.QIcon(r'icons\settings.png'), u'假期设置', self, shortcut='Ctrl+J', triggered=self.showHolidayPanel)

        self.addCash = QtGui.QAction(u'现金', self, shortcut='Ctrl+X', triggered=self.showCashPanel)

        self.aboutAction = QtGui.QAction(u"关于", self, triggered=self.about)

        self.minimize = QtGui.QAction(u'最小化', self, triggered=self.hide)
        self.maximize = QtGui.QAction(u'最大化',self, triggered=self.showMaximized)
        self.restore = QtGui.QAction(u'还原', self, triggered=self.showNormal)

    def showHolidayPanel(self):
        from panel import HolidayPanel
        hol = HolidayPanel()
        if hol.exec_():
            pass

    def showCashPanel(self):
        pass

    def about(self):
        QtGui.QMessageBox.about(self, u"关于", u"家族信托投资交易管理平台")

    def loadHolidays(self):
        q = QtSql.QSqlQuery()
        self.hols = []
        q.exec_(u"'SELECT HOLDATE FROM HOLIDAY WHERE HOLSTATUS<>'工作'")
        while q.next():
            self.hols.append(q.value(0).toDate().toPyDate())
        self.workdays=[]
        q.exec_(u"'SELECT HOLDATE FROM HOLIDAY WHERE HOLSTATUS='工作'")
        while q.next():
            self.workdays.append(q.value(0).toDate().toPyDate())

    def loadAccounts(self):
        q = QtSql.QSqlQuery()
        q.exec_('SELECT * FROM ACCT')
        data=[]
        while q.next():
            data.append([q.value(0).toString(),
                         q.value(1).toString(),
                         q.value(2).toDate().toPyDate(),
                         q.value(3).toString(),
                         q.value(4).toInt()[0],
                         q.value(5).toString(),
                         q.value(6).toString()])
        col = [u'账户', u'起始日', u'理财师', u'管理类型', u'开户行', u'银行账号']
        self.accts = pd.DataFrame.from_items(data, columns=col)
        pass


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dt = FwmDesktop()
    sys.exit(app.exec_())
