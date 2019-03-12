#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import sys
import datx
import requests
from IPy import IPSet, IP

reload(sys)
sys.setdefaultencoding('utf-8')

def getNow():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def getjson():
    url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
    r = requests.get(url)
    awsipv4 = r.json()['prefixes']
    globalip = []
    for ip in awsipv4:
        if ip['region'] == 'GLOBAL':
            globalip.append(ip['ip_prefix'])
    return set(globalip)

def writeipfile(ipnet):
    allip = []
    ipip = datx.City('/root/workspace/mydata4vipweek2.datx')
    iprange = IP(ipnet)
    for ip in iprange:
        ipinfo = ipip.find(str(ip))
        if ipinfo[0] == '中国':
            allip.append({ipinfo[1]:str(ip)})
        else:
            allip.append({ipinfo[0]:str(ip)})
    return allip

def ipdata():
    # country name
    c = []
    data = {}
    globalIP = '52.124.128.0/17'
    #for globalIP in getjson():
    allip = writeipfile(globalIP)
    #print allip
    # allip = [{'us':'ip1'}, {'hk':'ip2'} ...]
    for i in allip:
        c.append(i.keys()[0])
    # i = us set(c) all country | sort | uniq
    for i in set(c):
        data[i] = []
        for x in allip:
            try:
                # append ip1 ip2 ip3 ...
                data[i].append(x[i])
            except:
                pass
    # data = {'us': [ip1,ip2,ip3], 'hk':[ip4,ip5] ..}
    return data

def handleip(ips):
    i = 0
    ipset = IPSet()
    while i < len(ips):
        CIDR = IP("{}-{}".format(ips[i], ips[i+255]))
        ipset.add(CIDR)
        i += 256
    return ipset.prefixes

net= {}
data = ipdata()
print data
for r in data:
    net[r] = handleip(data[r])
    #print r, data[r]

#for i in net:
#    print "{}: {}".format(i, ' '.join([x.strNormal() for x in net[i]]))

#{1: {'hk': ['192.168.1.0', '192.168.2.0'], 'us': ['1.1.1.1', '2.2.2.2']}, 2: {'hk': ['192.168.111.0', '192.168.32.0'], 'us': ['1.0.0.0', '2.2.2.0']}}
