# -*- coding: utf-8 -*-
from login import LoginPage
from user import User
from PyQt4 import Qt, QtGui, QtCore, QtSql
import datetime
import dataview


class FwmDesktop(QtGui.QMainWindow):
    def __init__(self, td=None):
        QtGui.QMainWindow.__init__(self)
        self.td = td or datetime.date.today()
        self.initDB()
        login = LoginPage()
        if login.exec_():
            self.user = User(str(login.username.text()))
            self.initFromDB()
            self.createAction()
            self.createMenu()
            self.createPageWidgets()

            layout = QtGui.QHBoxLayout()
            self.centralWidget = QtGui.QWidget()
            self.centralWidget.setLayout(layout)
            self.setCentralWidget(self.centralWidget)
            self.treecontrol = TreeControl()
            self.treecontrol.clickSignal.connect(self.switchLayout)
            layout.addWidget(self.treecontrol)
            layout.addLayout(self.stackedLayout)

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
        self.loadFirmInfo()

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
        self.holAction = QtGui.QAction(QtGui.QIcon(r'icons/settings.png'), u'假期设置', self, shortcut='Ctrl+J', triggered=self.showHolidayPanel)
        self.exitAction = QtGui.QAction(QtGui.QIcon(r'icons/exit.png'), u'退出', self, triggered=QtGui.qApp.quit)


        self.addCash = QtGui.QAction(u'现金', self, shortcut='Ctrl+X', triggered=self.showCashPanel)

        self.aboutAction = QtGui.QAction(u"关于", self, triggered=self.about)

        self.minimize = QtGui.QAction(u'最小化', self, triggered=self.hide)
        self.maximize = QtGui.QAction(u'最大化',self, triggered=self.showMaximized)
        self.restore = QtGui.QAction(u'还原', self, triggered=self.showNormal)

    def createPageWidgets(self):
        self.stackedLayout = QtGui.QStackedLayout()
        # trade detail layout
        q1 = 'SELECT BOOK, TRADE_DATE, SETTLE_DATE, PROD_ID, SHARE_CLASS, PRICE, AMOUNT, COMMENT, TRADE_ID FROM TRADE'
        headers1 = [u'账户', u'交易日', u'交割日', u'代码', u'类型', u'价格', u'数量', u'备注', u'识别码']

        self.tradedatamodel = QtSql.QSqlQueryModel()
        self.tradedatamodel.setQuery(q1)
        for i, h in enumerate(headers1):
            self.tradedatamodel.setHeaderData(i, QtCore.Qt.Horizontal, h)

        self.tradeView = QtGui.QTableView()
        self.tradeView.setModel(self.tradedatamodel)

        self.stackedLayout.addWidget(self.tradeView)
        # TODO: Don't know why it crashes if setting different delegates
        # df = dataview.DateFormater('yyyy-MM-dd')
        # self.tradeView.setItemDelegateForColumn(1, df)
        # self.tradeView.setItemDelegateForColumn(2, df)
        nf = dataview.DoubleFormater(2, True)
        self.tradeView.setItemDelegateForColumn(5, nf)
        self.tradeView.setItemDelegateForColumn(6, nf)

        self.tradeView.resizeColumnsToContents()
        self.tradeView.resizeRowsToContents()
        self.tradeView.setSortingEnabled(True)
        self.tradeView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.tradeView.setMouseTracking(True)

        # acct info layout
        q2 = 'SELECT a.acctname, a.start_date, r.rmname, m.mgtname from acct a left outer join rm r on r.id=a.rm left outer join mgt_type m on m.id=a.mgt_type'
        headers2 = [u'账户', u'起始日', u'理财师', u'管理类型']
        self.acctdatamodel = QtSql.QSqlQueryModel()
        self.acctdatamodel.setQuery(q2)
        for i, h in enumerate(headers2):
            self.acctdatamodel.setHeaderData(i, QtCore.Qt.Horizontal, h)

        self.acctInfoView = QtGui.QTableView()
        self.acctInfoView.setModel(self.acctdatamodel)
        self.acctInfoView.resizeColumnsToContents()
        self.acctInfoView.resizeRowsToContents()
        self.acctInfoView.setSortingEnabled(True)
        self.stackedLayout.addWidget(self.acctInfoView)

        # asset pool
        self.assetPool = QtGui.QWidget()
        apLayout = QtGui.QVBoxLayout()
        apBtnLayout = QtGui.QHBoxLayout()
        cbrcRptBtn = QtGui.QPushButton(u'银监报备表头')
        cbrcRptBtn.clicked.connect(self.showRptPanel)
        apBtnLayout.addWidget(cbrcRptBtn)
        newCnpt = QtGui.QPushButton(u'发行人信息')
        newCnpt.clicked.connect(self.showCnptPanel)
        apBtnLayout.addWidget(newCnpt)
        newProducts = QtGui.QPushButton(u'添加产品')
        newProducts.clicked.connect(self.showNewProdDiag)
        apBtnLayout.addWidget(newProducts)
        apLayout.addLayout(apBtnLayout)

        self.prodView = QtGui.QTableView()
        apLayout.addWidget(self.prodView)
        self.assetPool.setLayout(apLayout)
        self.stackedLayout.addWidget(self.assetPool)

    def switchLayout(self, itemName):
        if itemName == Qt.QString(u'交易明细'):
            self.stackedLayout.setCurrentWidget(self.tradeView)
        elif itemName == Qt.QString(u'基本信息'):
            self.stackedLayout.setCurrentWidget(self.acctInfoView)
        elif itemName == Qt.QString(u'产品池'):
            self.stackedLayout.setCurrentWidget(self.assetPool)

    def showNewProdDiag(self):
        from diag_product import NewProductDialog
        npd = NewProductDialog()
        if npd.exec_():
            prodid = npd.code.text()
            issuer = npd.issuer.currentText()
            shareclass = npd.shareclass.text()
            windcode = npd.windcode.text()


    def showCnptPanel(self):
        from panel import CnptInfo
        ci = CnptInfo()
        if ci.exec_():
            pass

    def showHolidayPanel(self):
        from panel import HolidayPanel
        hol = HolidayPanel()
        if hol.exec_():
            pass

    def showRptPanel(self):
        from panel import CompanyInfo
        ci = CompanyInfo()
        if ci.exec_():
            pass

    def showCashPanel(self):
        from panel import CashTrade
        ct = CashTrade(self.accts)
        if ct.exec_():
            from trade import Trade
            t = Trade(ct.acct.currentText(),
                      ct.tradeDate.date().toPyDate(),
                      ct.tradeDate.date().toPyDate(),
                      ct.flow.text(), u'现金', 1., float(ct.amount.text()),
                      ct.comment.text(),
                      order_file=False,
                      conf_file=ct.filePath.text() or False)
            t.toDB()
            self.tradedatamodel.query().exec_()


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
        q = QtSql.QSqlQuery('SELECT ID, RMNAME FROM RM')
        self.rm = []
        while q.next():
            self.rm.append('%s(%s)'%(q.value(1).toString(), q.value(0).toString()))
        q = QtSql.QSqlQuery('SELECT ID FROM ACCT')
        self.accts = []
        while q.next():
            self.accts.append(q.value(0).toString())

    def loadTrades(self):
        self.balance = {}

    def loadFirmInfo(self):
        q = QtSql.QSqlQuery("SELECT MAX(RPTDATE), NETASSET_LASTMONTH, NETCAP_LASTQUAT, AUM_LASTMONTH, RISKCAP_LASTQUAT FROM FIRMINFO WHERE RPTDATE<='%s'" % (self.td))
        while q.next(): # should be only one record
            self.cbrcRptDate = q.value(0).toDate().toPyDate()
            self.netasset_lm = q.value(1).toDouble()[0]
            self.netcap_lq = q.value(2).toDouble()[0]
            self.aum_lm = q.value(3).toDouble()[0]
            self.riskcap_lq = q.value(4).toDouble()[0]

class TreeControl(QtGui.QTreeWidget):
    clickSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.setHeaderHidden(True)
        self.addItems(self.invisibleRootItem())
        self.itemClicked.connect(self.handleClicked)
        self.setMaximumWidth(120)

    def addItems(self, parent):
        trades_item = self.addParent(parent, u'资产' )
        self.addChild(trades_item, u'交易明细')
        self.addChild(trades_item, u'产品池')

        accts_item = self.addParent(parent, u'账户')
        self.addChild(accts_item, u'基本信息')
        self.addChild(accts_item, u'日历提醒')

        rm_item = self.addParent(parent, u'理财师')
        self.addChild(rm_item, u'基本信息')

    def addParent(self, parent, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setExpanded(True)
        return item

    def addChild(self, parent, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        return item

    def handleClicked(self, item):
        si = self.selectedItems()[0].text(0)
        self.clickSignal.emit(si)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dt = FwmDesktop()
    sys.exit(app.exec_())
