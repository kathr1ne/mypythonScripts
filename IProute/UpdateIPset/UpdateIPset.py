#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 

import IPy
import logging

def get_ipnet(ipset, ipa):
    net = []
    with open(ipset, 'r') as f:
        for line in f:
            if line.startswith(ipa):
                net.append(line.strip('\n'))
    return net

def check_ip():
    with open(collectip, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                ip = line.strip('\n')
                ipa = ip.split('.')[0]
                for i in get_ipnet(ipset, ipa):
                    if ip in IPy.IP(i):
                        flag = True
                        print "IP: {} in Network segment: {}".format(ip, i)
                        break
                    else:
                        flag = False
                if not flag:
                    print "IP: {} can't find it from {}".format(ip, ipset)

if __name__ == '__main__':
    ipset = '/home/kongshuai/ipset/setlist/us.list'
    collectip = '/home/kongshuai/workspace/iproute/CollectedIP.ip'
    check_ip()
