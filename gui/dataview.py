# -*- coding: utf-8 -*-
from PyQt4 import QtSql, QtCore, QtGui, Qt


class QueryTableModel(QtSql.QSqlQueryModel):
    def __init__(self, query, headerdata, parent=None, *args):
        Qt.QAbstractTableModel.__init__(self, parent, *args)
        self.setQuery(query)
        self.headerdata = headerdata
        for i, h in enumerate(self.headerdata):
            self.setHeaderData(i, QtCore.Qt.Horizontal, h)

    def refresh(self):
        self.query().exec_()


class QueryTableView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.verticalHeader().hide()

    def setFormats(self, colformats):
        for f in colformats:
            self.setItemDelegateForColumn(f[0], f[1])

class DateFormater(Qt.QStyledItemDelegate):
    def __init__(self, date_format):
        Qt.QStyledItemDelegate.__init__(self)
        self.date_format = date_format

    def displayText(self, value, locale):
        return value.toDate().toString(self.date_format)
