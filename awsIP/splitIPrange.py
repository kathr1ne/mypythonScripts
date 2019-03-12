#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import sys
import datx
import time
import requests
import threading
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

def writeipfile(ipNet, data, index):
    print "start Thread-{} {}".format(index, getNow())
    # country set, allip[{'us':'ip1'}, {'us':'ip2'}, {'hk':'ip3'}]
    c, allip = [], []
    ipip = datx.City(ipipDatx)
    iprange = IP(ipNet)
    for ip in iprange:
        ipinfo = ipip.find(str(ip))
        if ipinfo[0] == '中国':
            allip.append({ipinfo[1]:str(ip)})
        else:
            allip.append({ipinfo[0]:str(ip)})

    # data = {0: {'us':['ip1, ip2']}, 1: {'hk'}:['ip3, ip4']}
    # set(c) = ([hk, us, jp, kr...])
    data[index] = {}
    for i in allip:
        c.append(i.keys()[0])
    for i in set(c):
        data[index][i] = []
        for x in allip:
            try:
                data[index][i].append(x[i])
            except:
                pass
    print "end Thread-{} {}".format(index, getNow())

def handleip(ips):
    # convert IP to CIDR
    tdata = {}
    for country in ips:
        i = 0
        ipset = IPSet()
        while i < len(ips[country]):
            CIDR = IP("{}-{}".format(ips[country][i], ips[country][i+255]))
            ipset.add(CIDR)
            i += 256
        tdata[country] = ipset.prefixes
    return tdata

if __name__ == '__main__':
    start = time.time()
    index = 0
    net, data, threads = {}, {}, []
    ipipDatx = '/root/workspace/mydata4vipweek2.datx'
    prefiex = ['52.219.32.0/21']
    #for ipNet in getjson():
    for ipNet in prefiex:
        t = threading.Thread(target=writeipfile, args=(ipNet, data, index))
        t.start()
        threads.append(t)
        index += 1
    # wait threads done
    for th in threads:
        th.join()
    print "end all Threads %s" % getNow()

    for n in data:
        net[n] = handleip(data[n])
    # net= {0: {'us':[net1, net2]}, 1: {'hk'}:[net3, net4]} 
    for tx in net:
        for ty in net[tx]:
            print "Thread-{} {} {}".format(tx, ty, ' '.join([x.strNormal() for x in net[tx][ty]]))
    end = time.time()
    print "spend times {0:.2f}s".format(end-start)
