#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 

import logging
from IPy import IP

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
                # 地区
                area = line.strip('\n').split()[0]
                ip = line.strip('\n').split()[-1]
                ipa = ip.split('.')[0]
                # hk special default route, no ipset
                if area == 'hk':
                    ipset = '/home/kongshuai/ipset/setlist/us.list'
                else:
                    ipset = '/home/kongshuai/ipset/setlist/{}.list'.format(area)
                f = ipset.split('/')[-1]
                for i in get_ipnet(ipset, ipa):
                    if ip in IP(i):
                        flag = True
                        break
                    else:
                        flag = False
                if flag:
                    if area == 'hk':
                        logging.error("IP: {}({}) find in {} NetworkSegmen: {}".format(ip, area, f, i))
                    else:
                        logging.info("IP: {}({}) in NetworkSegment: {}, {}".format(ip, area, i, f))
                if not flag:
                    if area == 'hk':
                        logging.info("IP: {}({}) can't find it from {}".format(ip, area, f))
                    else:
                        logging.warning("IP: {}({}) can't find it from {}".format(ip, area, f))

if __name__ == '__main__':
    collectip = '/home/kongshuai/workspace/iproute/CollectedIP.ip'
    logging.basicConfig(level=logging.INFO,
                    format = '%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s %(message)s',
                    datefmt = '%F %T',
                    filename = 'mytest04.log',
                    filemode = 'w')
    check_ip()
