#!/usr/bin/python
# coding: utf-8
#

import os,sys
import re
import timeit

start = timeit.default_timer()
s = os.sep
root = ['/data1','/data2','/data3','/data4','/data5','/data6','/data7','/data8','/data9','/data10','/data11','/data12']
path = '/IF_UPLOAD/ok'
Date = '20170901(16|17)'
Phone = '15102217661'
Type = '14'

for i in range(12):
    p = root[i]+path
    for dirpath,dirname,filename in os.walk(p):
        for fn in filename:
            name = dirpath + s + fn
            m = re.search(Type + '.*' + Date + '.*',name)
            if m != None:
                match = dirpath + s + m.group(0)
                fp = open(match,'r')
                for line in fp.readlines():
                    lines = line.strip()
                    if Phone in lines:
                        #print lines
                        output = sys.stdout
                        with open('/tmp/data3.txt','a') as file:
                            sys.stdout = file
                            print lines
