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

def writeipfile(ipnet, data, index):
    print "start Thread-{} {}".format(index, getNow())
    c = []
    allip = []
    ipipDatx = '/root/workspace/mydata4vipweek2.datx'
    ipip = datx.City(ipipDatx)
    iprange = IP(ipnet)
    for ip in iprange:
        ipinfo = ipip.find(str(ip))
        if ipinfo[0] == '中国':
            allip.append({ipinfo[1]:str(ip)})
        else:
            allip.append({ipinfo[0]:str(ip)})

    # get Lock
    # mutex.acquire()
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
    # release Lock
    # mutex.release()
    print "end Thread-{} {}".format(index, getNow())

def handleip(ips):
    tdata = {}
    for country in ips:
        i = 0
        ipset = IPSet()
        while i < len(ips[country]):
            CIDR = IP("{}-{}".format(ips[country][i], ips[country][i+255]))
            ipset.add(CIDR)
            i += 256
        tdata[country] = ipset.prefixes
        #print "{} {}".format(tdata[country], country)
    return tdata

if __name__ == '__main__':
    index = 0
    data = {}
    threads = []
    # create Lock
    #mutex = threading.Lock()
    #getjson = ['205.251.192.0/19']
    for globalIP in getjson():
    #for g in getjson:
        t = threading.Thread(target=writeipfile, args=(globalIP, data, index))
        t.start()
        threads.append(t)
        index += 1
    # wait thread done
    for th in threads:
        th.join()
    print "end all Threads %s" % getNow()
    #for d in data[0]:
    #    print d, len(data[0][d])
    
    net= {}
    for n in data:
        net[n] = handleip(data[n])
    
    for tx in net:
        for ty in net[tx]:
            print "Thread-{} {} {}".format(tx, ty, [x.strNormal() for x in net[tx][ty]])
