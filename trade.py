# -*- coding: utf-8 -*-
import hashlib
from PyQt4 import QtSql

class Trade:
    def __init__(self, book, tradeDate, settleDate, prodID, shareClass, price, amount, comment='', order_file=False, conf_file=False, tradeID = None):
        self.book = book
        self.tradeDate = tradeDate
        self.settleDate = settleDate
        self.prodID = prodID
        self.shareClass = shareClass
        self.price = price
        self.comment = comment
        self.amount = amount
        self.order_file = order_file
        self.conf_file = conf_file
        if tradeID:
            self.tradeID = tradeID
        else:
            m = hashlib.md5()
            idstr = '%s%s%s%s%s%s%s' % (self.book, self.tradeDate, self.prodID, self.shareClass, self.price, self.amount, self.comment)
            m.update(idstr.encode('utf-8'))
            self.tradeID = m.hexdigest()

    @staticmethod
    def fromDB(record):
        tradeID, book, tradeDate, settleDate, prodID, shareClass, price, amount, comment, order_file, conf_file = record
        t = Trade(book, tradeDate, settleDate, prodID, shareClass, price, amount, comment, order_file=bool(order_file), conf_file=bool(conf_file),tradeID=tradeID)
        return t

    def toDB(self):
        try:
            q = QtSql.QSqlQuery()
            q.exec_("""INSERT INTO TRADE VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
                self.tradeID, self.book, self.tradeDate, self.settleDate, self.prodID, self.shareClass, self.price, self.amount, self.comment, self.order_file, self.conf_file))
            QtSql.QSqlDatabase().commit()
        except Exception, e:
            print e.message
            QtSql.QSqlDatabase().rollback()

    def uploadOrderFile(self):
        pass

    def uploadConfFile(self):
        pass

