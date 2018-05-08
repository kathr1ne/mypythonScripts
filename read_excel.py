#!/usr/bin/env python
# -*- coding:utf-8 -*-
# read test

import xlrd
import os,sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
curDir = os.getcwd()

data = xlrd.open_workbook(curDir + '/ip.xlsx')
sheet = data.sheet_by_name('IP')
#print(sheet.nrows)  #行数
#print(sheet.ncols)  #列数


with open(curDir + '/IP.tmp', 'w') as f:
    for n in range(1, sheet.nrows):
        #print sheet.cell(n,0).value + '\n' + sheet.cell(n,1).value,sheet.cell(n,2).value,sheet.cell(n,3).value
        #for i in range(sheet.ncols):
            #text = sheet.cell_value(n, i).encode('utf-8')
            #f.write(text)
            #f.write('\n')
        l1 = sheet.cell(n,0).value
        l2 = sheet.cell(n,1).value
        l3 = sheet.cell(n,2).value
        l4 = sheet.cell(n,3).value
        f.write(l1 + '\n' + l2 + " " + l3 + " " + l4)
        f.write('\n')
        f.flush()

with open(curDir + '/IP.txt', 'w') as ip:
    CMD = "awk '{if($0 != \"\")print}' IP.tmp | awk 'BEGIN{OFS=\",\"}{if($0 ~ /[a-z]$/){City = $2;next};if(NF > 3)print City,$2,$3}'"
    out = os.popen(CMD) 
    line = out.read()#[:-1]
    ip.write(line)
    ip.flush()

tmp = curDir + '/IP.tmp'
if os.path.exists(tmp):
    os.remove(tmp)
