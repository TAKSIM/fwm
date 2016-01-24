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

            layout = QtGui.QHBoxLayout()
            self.treecontrol = TreeControl()
            layout.addWidget(self.treecontrol)
            layout.addWidget(self.acctInfoView)
            self.centralWidget = QtGui.QWidget()
            self.centralWidget.setLayout(layout)
            self.setCentralWidget(self.centralWidget)
            self.resize(800, 600)
            self.setWindowTitle(u'家族信托投资管理平台 - {0}'.format(self.user.name))
            self.statusBar().showMessage(u'准备就绪')
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
        self.loadTrades()

    def createMenu(self):
        self.mb = self.menuBar()
        m1 = self.mb.addMenu(u'&系统')
        m1.addAction(self.rbAction)
        m1.addAction(self.holAction)
        m1.addAction(self.exitAction)

        m2 = self.mb.addMenu(u'&交易')
        m2.addAction(self.addCash)

        m3 = self.mb.addMenu(u'&帮助')
        m3.addAction(self.aboutAction)

    def createAction(self):
        self.rbAction = QtGui.QAction(QtGui.QIcon(r'icons/balance.png'), u'导入网银数据', self, shortcut='Ctrl+W', triggered=self.showImportBalance)
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

    def showImportBalance(self):
        from panel import ImportBalance
        ib = ImportBalance()
        if ib.exec_():
            from PyQt4.QtCore import QFile
            if QFile.exists(ib.filename.text()):
                from pivot import readbalance
                nb = readbalance(unicode(ib.filename.text()), bank='ccb')
                self.balance.update(nb)
            else:
                QtGui.QMessageBox.about(self, u'文件不存在', ib.filename.text())

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
        self.acctdatamodel = QtSql.QSqlQueryModel()
        self.acctdatamodel.setQuery('SELECT a.acctname, a.start_date, r.rmname, m.mgtname from acct a left outer join rm r on r.id=a.rm left outer join mgt_type m on m.id=a.mgt_type')
        self.acctdatamodel.setHeaderData(0, QtCore.Qt.Horizontal, u'账户')
        self.acctdatamodel.setHeaderData(1, QtCore.Qt.Horizontal, u'起始日')
        self.acctdatamodel.setHeaderData(2, QtCore.Qt.Horizontal, u'理财师')
        self.acctdatamodel.setHeaderData(3, QtCore.Qt.Horizontal, u'管理类型')
        self.acctInfoView = QtGui.QTableView()
        self.acctInfoView.setSortingEnabled(True)
        # self.acctInfoView.horizontalHeader().setSortIndicatorShown(True)
        # self.acctInfoView.horizontalHeader().setSortIndicator(0, QtCore.Qt.DescendingOrder)
        self.acctInfoView.setModel(self.acctdatamodel)
        self.acctInfoView.resizeColumnsToContents()
        self.acctInfoView.resizeRowsToContents()
        self.acctInfoView.verticalHeader().hide()
        # q = QtSql.QSqlQuery()
        # q.exec_('SELECT * FROM ACCT')
        # data=[]
        # while q.next():
        #     data.append([q.value(0).toString(),
        #                  q.value(1).toString(),
        #                  q.value(2).toDate().toPyDate(),
        #                  q.value(3).toString(),
        #                  q.value(4).toInt()[0],
        #                  q.value(5).toString(),
        #                  q.value(6).toString()])
        # col = ['id', 'name', 'startdate', 'rm', 'mgttype', 'branch', 'acctno']
        # self.accts = pd.DataFrame(data, columns=col)

    def loadTrades(self):
        self.balance = {}


class TreeControl(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.addItems(self.treeWidget.invisibleRootItem())
        self.treeWidget.itemClicked.connect(self.handleClicked)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

    def addItems(self, parent):
        trades_item = self.addParent(parent, u'交易' )
        accts_item = self.addParent(parent, u'账户')
        rm_item = self.addParent(parent, u'理财师')

        self.addChild(trades_item, u'交易明细')

        q = QtSql.QSqlQuery('SELECT ID FROM ACCT')
        while q.next():
            self.addChild(accts_item, q.value(0).toString())

        q = QtSql.QSqlQuery('SELECT ID, RMNAME FROM RM')
        while q.next():
            self.addChild(rm_item, '%s(%s)' % (q.value(1).toString(), q.value(0).toString()))

    def addParent(self, parent, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setExpanded(False)
        return item

    def addChild(self, parent, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        return item

    def handleClicked(self, item):
        print item.text(0)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dt = FwmDesktop()
    sys.exit(app.exec_())
