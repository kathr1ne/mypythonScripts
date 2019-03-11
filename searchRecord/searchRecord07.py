#!/usr/bin/python
# coding: utf-8
# Email: kongs@broadtech.com.cn
#

import re
import os,sys
from optparse import OptionParser

s = os.sep
path = '/IF_UPLOAD/ok'
#Type = '14'

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

def walkFiles(root):
    #for dirpath,dirname,filename in os.walk(root):
    list1 = []
    if os.path.exists(root):
        filename = os.listdir(root)
        for fn in filename:
            #m = re.search('^14.*' + Date + '.*',fn)
            pat = re.compile('^14.*' + Date + '.*')
            m = pat.search(fn)
            if m:
                m = root + s + m.group(0)
                list1.append(m)
    return list1

def openfile(list2):
    list3 = []
    for i in list2:
        with open(i,'r') as fp:
            for line in fp.readlines():
                if Phone in line:
                    lines = line.strip()
                    list3.append(lines+'\n')
    with open(outfile,'a') as f:
        #f.write(lines + '\n')
        f.writelines(list3)
        #sys.stdout = f
        #print lines

def main():
    list1 = list2 = []
    for i in range(1,13):
        root = '/data' + str(i) + path
        list1 = walkFiles(root)
	list2 = list1 + list2
    openfile(list2)
        

if __name__ == "__main__":
    main()
