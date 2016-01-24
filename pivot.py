# -*- coding: utf-8 -*-
import pandas as pd


def readbalance(filename, bank='ccb'):
    if bank == 'ccb':
        data = pd.read_excel(filename, header=0, skiprows=3, skip_footer=1, index_col=0)
        balance = data.iloc[:,2].to_dict()
        return balance
    else:
        raise NotImplemented()


if __name__ == '__main__':
    pass
