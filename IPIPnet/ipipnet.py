#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import datx
import codecs
from IPy import IP

ipip = datx.City("C:\workspace\ipipnet\mydata4vipweek2.datx")

for ip in IP('223.4.0.0/14'):
    if ipip.find(str(ip))[0] != "中国":
        print(ip, ipip.find(str(ip)))

'''
iprange = IP('52.84.0.0/15')
with open(r"C:\workspace\test.txt", 'a+') as f:
    for ip in iprange:
        ipinfo = ipip.find(str(ip))
        ipinfo.append(str(ip))
        line = "{} {}".format(ipinfo[-1], ipinfo[0])
        f.write(line + "\n")

#print(IP('{}-{}'.format(iphk[0], iphk[-1])))
#print(iphk[0], iphk[-1])
'''

