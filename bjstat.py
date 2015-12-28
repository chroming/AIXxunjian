# -*- coding:utf-8 -*-

import xlrd

def stat(xls):
    col0 = table.col_values(0)
    col2 = table.col_values(2)
    cols0 = list(set(col0))
    cols2 = list(set(col2))
    for c0 in col0:
        cpn = []
        for nc in range(table.ncols):
            if table.cell(nc, 0).value == c0
                cpn.append(nc, 2)
            cpns = list(set(cpn))
            for n in range(cpn):
                cnumb = cpn.count(cpns[n])

xlsdata = xlrd.open_workbook('/Users/chroming/logtmp/xls/xunjian.xls')
xlstable = xlsdata.sheets()[0]
stat(xlstable)