# -*- coding: utf-8 -*-

class DayCountConvention:
    def __init__(self, name):
        self.name = name

    def yearfrac(self, startdate, enddate, **kwargs):
        raise NotImplemented()


class Act365(DayCountConvention):
    def __init__(self):
        DayCountConvention.__init__('Act/365')

    def YearFrac(self, startDate, endDate, **kwargs):
        return (endDate-startDate).days/365.
