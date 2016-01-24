# -*- coding: utf-8 -*-
import datetime
from PyQt4 import QtGui, QtSql, QtCore

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