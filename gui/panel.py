# -*- coding: utf-8 -*-
import datetime
from PyQt4 import QtGui, QtSql, QtCore


class CnptInfo(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        layout = QtGui.QGridLayout()
        dm = QtSql.QSqlQueryModel()
        self.q = 'SELECT * FROM CNPT'
        dm.setQuery(self.q)
        dv = QtGui.QTableView()
        header=[u'中文简称', u'中文全称', u'英文简称', u'官方网站']
        for i, h in enumerate(header):
            dm.setHeaderData(i, QtCore.Qt.Horizontal, h)
        dv.setModel(dm)
        dv.resizeRowsToContents()
        dv.resizeColumnsToContents()
        dv.setSortingEnabled(True)
        dv.setSelectionBehavior(QtGui.QTableView.SelectRows)
        layout.addWidget(dv, 0,0,1,2)
        self.newcnpt = QtGui.QPushButton(u'添加机构')
        self.newcnpt.clicked.connect(self.newinfo)
        layout.addWidget(self.newcnpt,1,0,1,1)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        layout.addWidget(self.ok,1,1,1,1)
        self.setLayout(layout)

class NewCnptInfo(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'机构信息')
        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel(u'机构中文全称'),0,0,1,1)
        self.name_full_cn = QtGui.QLineEdit()
        layout.addWidget(self.name_full_cn, 0, 1, 1, 1)
        layout.addWidget(QtGui.QLabel(u'机构中文简称'), 1, 0, 1, 1)
        self.name_short_cn = QtGui.QLineEdit()
        layout.addWidget(self.name_short_en, 1, 1, 1, 1)
        layout.addWidget(QtGui.QLabel(u'机构英文简称'), 2, 0, 1, 1)
        self.name_short_en = QtGui.QLineEdit()
        layout.addWidget(self.name_short_en, 2, 1, 1, 1)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        layout.addWidget(self.ok, 3, 1, 1, 1)
        self.cancel = QtGui.QPushButton(u'取消')
        self.cancel.clicked.connect(self.close)
        layout.addWidget(self.cancel, 3, 0, 1, 1)
        self.setLayout(layout)


class CompanyInfo(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icons/tent.png'))
        self.setWindowTitle(u'公司基础信息（银监报备使用）')
        self.setFixedSize(450, 150)
        self.q = 'SELECT * FROM FIRMINFO'
        layout = QtGui.QVBoxLayout()
        self.ci = QtSql.QSqlQueryModel()
        self.ci.setQuery(self.q)
        header = [u'报告日期', u'上月末净资产', u'上季末净资本', u'上月末信托总资产', u'上季末风险资本']
        for i, h in enumerate(header):
            self.ci.setHeaderData(i, QtCore.Qt.Horizontal, h)
        self.civ = QtGui.QTableView()
        self.civ.setModel(self.ci)
        self.civ.setUpdatesEnabled(True)
        self.civ.resizeColumnsToContents()
        self.civ.resizeRowsToContents()
        self.civ.verticalHeader().hide()
        self.civ.setSelectionBehavior(QtGui.QTableView.SelectRows)
        layout.addWidget(self.civ)

        btOK = QtGui.QPushButton(u'确定')
        btOK.clicked.connect(self.accept)
        btCancel = QtGui.QPushButton(u'取消')
        btCancel.clicked.connect(self.close)
        btNew = QtGui.QPushButton(u'添加数据')
        btNew.clicked.connect(self.newrpt)
        btLayout = QtGui.QHBoxLayout()
        btLayout.addWidget(btNew)
        btLayout.addWidget(btCancel)
        btLayout.addWidget(btOK)
        layout.addLayout(btLayout)
        self.setLayout(layout)

    def newrpt(self):
        nci = NewCompInfo()
        if nci.exec_():
            rptDate = nci.rptDate.date().toPyDate()
            netasset_lm = nci.netasset_lm.text().toDouble()[0]
            netcap_lq = nci.netcap_lq.text().toDouble()[0]
            aum_lm = nci.aum_lm.text().toDouble()[0]
            riskcap_lq = nci.riskcap_lq.text().toDouble()[0]
            q = QtSql.QSqlQuery()
            try:
                q.exec_("""INSERT INTO FIRMINFO VALUES ('%s','%s','%s','%s','%s')""" % (rptDate, netasset_lm, netcap_lq, aum_lm, riskcap_lq))
                QtSql.QSqlDatabase().commit()
                self.ci.setQuery(self.q)
            except Exception, e:
                print e.message
                QtSql.QSqlDatabase().rollback()


class NewCompInfo(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel(u'报告日期'),0,0,1,1)
        td = datetime.date.today()
        self.rptDate = QtGui.QDateEdit(datetime.date(td.year, td.month, 1))
        layout.addWidget(self.rptDate,0,1,1,1)
        layout.addWidget(QtGui.QLabel(u'上月末净资产（亿元）'),1,0,1,1)
        self.netasset_lm = QtGui.QLineEdit()
        self.netasset_lm.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.netasset_lm, 1,1,1,1)
        layout.addWidget(QtGui.QLabel(u'上季末净资本（亿元）'),2,0,1,1)
        self.netcap_lq = QtGui.QLineEdit()
        self.netcap_lq.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.netcap_lq, 2,1,1,1)
        layout.addWidget(QtGui.QLabel(u'上月末信托总资产（亿元）'),3,0,1,1)
        self.aum_lm = QtGui.QLineEdit()
        self.aum_lm.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.aum_lm, 3,1,1,1)
        layout.addWidget(QtGui.QLabel(u'上季末风险资本'),4,0,1,1)
        self.riskcap_lq = QtGui.QLineEdit()
        self.riskcap_lq.setValidator(QtGui.QDoubleValidator())
        layout.addWidget(self.riskcap_lq, 4,1,1,1)
        self.cancel = QtGui.QPushButton(u'取消')
        self.cancel.clicked.connect(self.close)
        layout.addWidget(self.cancel, 5,0,1,1)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        layout.addWidget(self.ok, 5,1,1,1)
        self.setLayout(layout)


class HolidayPanel(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'假期设置')
        self.setWindowIcon(QtGui.QIcon('icons/tent.png'))
        self.setMaximumWidth(200)
        layout = QtGui.QVBoxLayout()
        self.holData = QtSql.QSqlTableModel()
        self.holData.setTable('holiday')
        self.holData.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.holData.select()
        self.holData.setHeaderData(0, QtCore.Qt.Horizontal, u'日期')
        self.holData.setHeaderData(1, QtCore.Qt.Horizontal, u'假期')
        self.holData.setHeaderData(2, QtCore.Qt.Horizontal, u'状态')
        self.holView = QtGui.QTableView()
        self.holView.setModel(self.holData)
        self.holView.resizeColumnsToContents()
        self.holView.resizeRowsToContents()
        self.holView.verticalHeader().hide()

        buttonLayout = QtGui.QHBoxLayout()
        self.btAdd = QtGui.QPushButton(u'添加假期')
        self.btAdd.clicked.connect(self.newHol)
        self.btConf = QtGui.QPushButton(u'确认修改')
        self.btConf.clicked.connect(self.submit)
        self.btCancel = QtGui.QPushButton(u'取消')
        self.btCancel.clicked.connect(self.close)
        buttonLayout.addWidget(self.btAdd)
        buttonLayout.addWidget(self.btConf)
        buttonLayout.addWidget(self.btCancel)
        layout.addLayout(buttonLayout)

        layout.addWidget(self.holView)
        self.setLayout(layout)

    def submit(self):
        self.holData.submitAll()

    def newHol(self):
        nh = NewHolPanel()
        if nh.exec_():
            date = nh.date.date()
            name = nh.nameList.currentText()
            status = nh.statusList.currentText()
            q = QtSql.QSqlQuery()
            try:
                q.exec_("""INSERT INTO HOLIDAY VALUES ('%s','%s','%s')""" % (date.toPyDate(), name, status))
                QtSql.QSqlDatabase().commit()
            except Exception, e:
                print e.message
                QtSql.QSqlDatabase().rollback()


class NewHolPanel(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icons/tent.png'))
        self.setWindowTitle(u'新增假期')
        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel(u'日期'),0,0,1,1)
        self.date = QtGui.QDateEdit(datetime.datetime.today())
        self.date.setCalendarPopup(True)
        layout.addWidget(self.date,0,1,1,1)
        layout.addWidget(QtGui.QLabel(u'假期'),1,0,1,1)
        self.nameList = QtGui.QComboBox()
        self.nameList.addItems([u'元旦',u'春节',u'清明节',u'劳动节',u'端午节',u'中秋节',u'国庆节',u'其他'])
        self.nameList.setEditable(True)
        layout.addWidget(self.nameList,1,1,1,1)
        layout.addWidget(QtGui.QLabel(u'状态'),2,0,1,1)
        self.statusList = QtGui.QComboBox()
        self.statusList.addItems([u'预期',u'确定',u'工作'])
        layout.addWidget(self.statusList,2,1,1,1)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        layout.addWidget(self.ok,3,0,1,1)
        self.cancel = QtGui.QPushButton(u'取消')
        self.cancel.clicked.connect(self.close)
        layout.addWidget(self.cancel,3,1,1,1)
        self.setLayout(layout)


class ImportBalance(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icons/tent.png'))
        self.setWindowTitle(u'导入网银数据')
        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel(u'银行'),0,0,1,1)
        self.banks = QtGui.QComboBox()
        self.banks.addItems([u'建设银行', u'兴业银行'])
        self.banks.setEditable(False)
        layout.addWidget(self.banks,0,1,1,2)
        self.selectFile = QtGui.QPushButton(u'文件')
        self.selectFile.clicked.connect(self.getfile)
        layout.addWidget(self.selectFile,1,0,1,1)
        self.filename = QtGui.QLineEdit()
        self.filename.setEnabled(True)
        layout.addWidget(self.filename,1,1,1,2)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        layout.addWidget(self.ok,2,2,1,1)
        self.setLayout(layout)

    def getfile(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, u'选择网银数据文件', '', 'Excel file (*.xls *.xlsx)')
        self.filename.setText(fn)


class CashTrade(QtGui.QDialog):
    def __init__(self, accts, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowIcon(QtGui.QIcon('icons/tent.png'))
        self.setWindowTitle(u'现金流动')
        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel(u'交易日'), 0, 0, 1, 1)
        self.tradeDate = QtGui.QDateEdit(datetime.date.today())
        self.tradeDate.setCalendarPopup(True)
        layout.addWidget(self.tradeDate, 0, 1, 1, 1)
        layout.addWidget(QtGui.QLabel(u'账户'), 1, 0, 1, 1)
        self.acct = QtGui.QComboBox()
        self.acct.addItems(accts)
        layout.addWidget(self.acct, 1, 1, 1, 1)
        layout.addWidget(QtGui.QLabel(u'金额'), 2, 0, 1, 1)
        self.amount = QtGui.QLineEdit()
        self.amount.setValidator(QtGui.QDoubleValidator(-10000000000., 10000000000, 2))
        layout.addWidget(self.amount, 2, 1, 1, 1)
        layout.addWidget(QtGui.QLabel(u'流水号'), 3, 0, 1, 1)
        self.flow = QtGui.QLineEdit()
        layout.addWidget(self.flow, 3, 1, 1, 1)
        layout.addWidget(QtGui.QLabel(u'备注'), 4, 0, 1, 1)
        self.comment = QtGui.QLineEdit()
        layout.addWidget(self.comment, 4, 1, 1, 1)
        self.fileBtn = QtGui.QPushButton(u'指令')
        self.fileBtn.clicked.connect(self.getfile)
        layout.addWidget(self.fileBtn, 5, 0, 1, 1)
        self.filePath = QtGui.QLineEdit()
        self.filePath.setEnabled(False)
        layout.addWidget(self.filePath, 5, 1, 1, 1)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        layout.addWidget(self.ok, 6, 1, 1, 1)
        self.setLayout(layout)

    def getfile(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, u'选择指令扫描文件', '')
        self.filePath.setText(fn)