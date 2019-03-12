#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import sys
import datx
import subprocess
from IPy import IP

reload(sys)
sys.setdefaultencoding('utf-8')

def shellcmd(CMD):
    result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.communicate()

def writeipfile():
    ipip = datx.City('/root/workspace/mydata4vipweek2.datx')
    iprange = IP('52.84.0.0/15')
    with open('/root/workspace/test.ip', 'a') as f:
        for ip in iprange:
            ipinfo = ipip.find(str(ip))
            ipinfo.append(str(ip))
            us.append({ipinfo[0]:str(ip)})
            #line = ' '.join(ipinfo)
            line = "{} {} {}".format(ipinfo[-1], ipinfo[0], ipinfo[1])
            #f.write(line + '\n')

def net():
    i = 0
    with open('/root/workspace/test.ip', 'r') as f:
        line = f.readlines()
        while i < len(line):
            start = line[i].strip().split()[0]
            end = line[i+255].strip().split()
            if end[1] == "中国":
                region = end[2]
            else:
                region = end[1]
                #region = "{} {}".format(end[1], end[2])
            CIDR = IP("{}-{}".format(start, end[0]))
            print "{} {}".format(CIDR, region)
            i += 256

us = []
writeipfile()
print us
