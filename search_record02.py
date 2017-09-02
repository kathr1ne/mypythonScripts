#!/usr/bin/python
# coding: utf-8
#
# Email: kongs@broadtech.com.cn

import re
import os,sys
from optparse import OptionParser

s = os.sep
path = '/IF_UPLOAD/ok'
Type = '14'

#options
op = OptionParser()
op.add_option("-d", help="search date(re) eg:20170901(16|17)", metavar="DATE")
op.add_option("-p", help="search phonenum eg:13330749988", metavar="PHONE")
op.add_option("-o", help="output file eg:/tmp/data01.txt", metavar="FILE")

options, args = op.parse_args()
Date = options.d
Phone = options.p
outfile = options.o

if not Date or not Phone or not outfile:
    op.print_help()
    sys.exit(1)

for i in range(1,13):
    root = '/data' + str(i) + path
    for dirpath,dirname,filename in os.walk(root):
        for fn in filename:
            name = dirpath + s + fn
            m = re.search(Type + '.*' + Date + '.*',name)
            if m != None:
                match = dirpath + s + m.group(0)
                fp = open(match,'r')
                for line in fp.readlines():
                    lines = line.strip()
                    if Phone in lines:
                        output = sys.stdout
                        with open(outfile,'a') as file:
                            sys.stdout = file
                            print lines
