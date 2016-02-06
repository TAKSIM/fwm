# -*- coding: utf-8 -*-
import datetime
from PyQt4 import QtGui, QtSql, QtCore


class NewProductDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'添加产品')
        layout = QtGui.QGridLayout()

        q = QtSql.QSqlQuery('SELECT NAME_SHORT_CN FROM CNPT')
        cnpts = []
        while q.next():
            cnpts.append(q.value(0).toString())
        q = QtSql.QSqlQuery('SELECT DES FROM ASSET_TYPE')
        assettypes = []
        while q.next():
            assettypes.append(q.value(0).toString())

        layout.addWidget(QtGui.QLabel(u'发行人'),0,0,1,1)
        self.issuer = QtGui.QComboBox()
        self.issuer.addItems(cnpts)
        layout.addWidget(self.issuer,0,1,1,1)
        layout.addWidget(QtGui.QLabel(u'产品名称'),1,0,1,1)
        self.name = QtGui.QLineEdit()
        layout.addWidget(self.name,1,1,1,1)
        layout.addWidget(QtGui.QLabel(u'合同号/代码'),2,0,1,1)
        self.code = QtGui.QLineEdit()
        layout.addWidget(self.code, 2,1,1,1)
        layout.addWidget(QtGui.QLabel(u'万得代码'),3,0,1,1)
        self.windcode = QtGui.QLineEdit()
        layout.addWidget(self.windcode,3,1,1,1)
        layout.addWidget(QtGui.QLabel(u'份额类别'),4,0,1,1)
        self.shareclass = QtGui.QLineEdit()
        layout.addWidget(self.shareclass,4,1,1,1)
        layout.addWidget(QtGui.QLabel(u'入池分级'),5,0,1,1)
        self.rating = QtGui.QLineEdit()
        layout.addWidget(self.rating,5,1,1,1)
        layout.addWidget(QtGui.QLabel(u'备注'),6,0,1,1)
        self.comment = QtGui.QLineEdit()
        layout.addWidget(self.comment,6,1,1,1)
        self.file = QtGui.QPushButton(u'合同文件')
        self.file.clicked.connect(self.getfile)
        layout.addWidget(self.file,7,0,1,1)
        self.filepath = QtGui.QLineEdit()
        self.filepath.setEnabled(False)
        layout.addWidget(self.filepath,7,1,1,1)
        layout.addWidget(QtGui.QLabel(u'资产类别'),8,0,1,1)
        self.assetType = QtGui.QComboBox()
        self.assetType.addItems(assettypes)
        layout.addWidget(self.assetType,8,1,1,1)
        layout.addWidget(QtGui.QLabel(u'起始日'), 9,0,1,1)
        self.startdate = QtGui.QDateEdit(datetime.date.today())
        self.startdate.setCalendarPopup(True)
        layout.addWidget(self.startdate,9,1,1,1)
        endDateLayout = QtGui.QHBoxLayout()
        endDateLayout.addWidget(QtGui.QLabel(u'到期日'))
        self.enddate = QtGui.QDateEdit(datetime.date.today())
        self.enddate.setCalendarPopup(True)
        endDateLayout.addWidget(self.enddate)
        self.endless = QtGui.QCheckBox()
        self.endless.setChecked(False)
        self.endless.stateChanged.connect(self.endless_switch)
        self.endless.setText(u'长期产品')
        endDateLayout.addWidget(self.endless)
        layout.addLayout(endDateLayout,10,0,1,2)

        gbCBRC = QtGui.QGroupBox(u'银监报备')
        gbLayout = QtGui.QGridLayout()
        self.cbrcrpt = QtGui.QCheckBox()
        self.cbrcrpt.setChecked(False)
        self.cbrcrpt.stateChanged.connect(self.cbrcrpt_switch)
        self.cbrcrpt.setText(u'涉及关联交易')
        gbLayout.addWidget(self.cbrcrpt,0,0,1,1)
        gbLayout.addWidget(QtGui.QLabel(u'交易定价'),1,0,1,1)
        self.cbrcprice = QtGui.QLineEdit()
        self.cbrcprice.setEnabled(False)
        gbLayout.addWidget(self.cbrcprice,1,1,1,1)
        gbLayout.addWidget(QtGui.QLabel(u'市场同类业务报价'),2,0,1,1)
        self.cbrcpriceavg = QtGui.QLineEdit()
        self.cbrcpriceavg.setEnabled(False)
        gbLayout.addWidget(self.cbrcpriceavg, 2,1,1,1)
        gbCBRC.setLayout(gbLayout)
        layout.addWidget(gbCBRC,11,0,1,2)

        btnLayout = QtGui.QHBoxLayout()
        self.cancel = QtGui.QPushButton(u'取消')
        self.cancel.clicked.connect(self.close)
        btnLayout.addWidget(self.cancel)
        self.ok = QtGui.QPushButton(u'确定')
        self.ok.clicked.connect(self.accept)
        btnLayout.addWidget(self.ok)
        layout.addLayout(btnLayout,12,0,1,2)
        self.setLayout(layout)

    def getfile(self):
        fn = QtGui.QFileDialog.getOpenFileName(self, u'选择合同文件','')
        self.filepath.setText(fn)

    def cbrcrpt_switch(self, *args, **kwargs):
        if self.cbrcrpt.isChecked():
            self.cbrcprice.setEnabled(True)
            self.cbrcpriceavg.setEnabled(True)
        else:
            self.cbrcprice.setEnabled(False)
            self.cbrcpriceavg.setEnabled(False)

    def endless_switch(self, *args, **kwargs):
        if self.endless.isChecked():
            self.enddate.setEnabled(False)
        else:
            self.enddate.setEnabled(True)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dt = NewProductDialog()
    sys.exit(app.exec_())