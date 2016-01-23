# -*- coding: utf-8 -*-
class Asset:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def fullname(self):
        return self.name

    def denominated(self):
        return 'CNY'

    def cashflow(self):
        return None

class Cash(Asset):
    def __init__(self, flowid):
        Asset.__init__(flowid, u'现金')

class FixedIncomeAsset(Asset):
    def __init__(self, code, name, rtn, dcc, compfreq=1):
        Asset.__init__(code, name)