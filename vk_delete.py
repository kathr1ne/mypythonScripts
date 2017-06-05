#!/usr/bin/python
# -*- coding utf-8 -*-
# Description：del songs from disk
#
# @Auther:kongshuai

import os
import xlrd
import timeit

start = timeit.default_timer()
s = os.sep

#将需要遍历的磁盘作为一个列表 利用循环遍历
root = ['E:\Tmp','F:\TEst']
#excel的sheet默认命名为vk_delete
excel = xlrd.open_workbook(r'F:\workspace\vk_delete\delete3.xlsx')
sheet = excel.sheet_by_name('vk_delete')

#读取excel文件为列表
row_list = []
for row in range(0,sheet.nrows):
    temp = ""
    for col in range(0,sheet.ncols):
        temp += str(sheet.cell(row,col).value)
        row_list.append(temp)
        
#delete songs
for path in root:
    for dirs,paths,files in os.walk(path):
        for i in row_list:
            if i in files:
                os.remove(dirs + s + i)
      
end = timeit.default_timer()        #计算花费时间
print("Delete completed；spend times: %.2fs" % (end - start))
