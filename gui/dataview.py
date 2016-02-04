# -*- coding: utf-8 -*-
from PyQt4 import Qt


class DateFormater(Qt.QItemDelegate):
    def __init__(self, date_format):
        Qt.QStyledItemDelegate.__init__(self)
        self.date_format = date_format

    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        pass

    def displayText(self, value, locale):
        return value.toDate().toString(self.date_format)


class DoubleFormater(Qt.QStyledItemDelegate):
    def __init__(self, numdigits, comma=True):
        Qt.QStyledItemDelegate.__init__(self)
        self.numdigits = numdigits
        self.comma = comma

    def displayText(self, value, locale):
        v, s = value.toDouble()
        if s:
            if self.comma:
                return '{:,}'.format(round(v, self.numdigits))
            else:
                return format(v, '.{0}f'.format(self.numdigits))
        else:
            return 'NaN'
