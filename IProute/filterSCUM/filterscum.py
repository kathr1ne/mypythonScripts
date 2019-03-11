#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 

from IPy import IP

def get_ipnet(ipset, ipa):
    net = []
    with open(ipset, 'r') as f:
        for line in f:
            if line.startswith(ipa):
                net.append(line.strip('\n'))
    return net

def check_ip():
    with open(scumip, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                ip = line.strip('\n')
                ipa = ip.split('.')[0]
                for i in get_ipnet(smartroute, ipa):
                    if ip in IP(i):
                        flag = True
                        break
                    else:
                        flag = False
                if flag:
                    print "IP: {} in Network segment: {}".format(ip, i)
                if not flag:
                    print "IP: {} can't find it from {}".format(ip, smartroute)

if __name__ == '__main__':
    #smartroute = '/home/kongshuai/workspace/iproute/filterSCUM/smartroute.html'
    smartroute = '/home/kongshuai/workspace/iproute/filterSCUM/America.txt'
    scumip = './scum.ip'
    check_ip()
