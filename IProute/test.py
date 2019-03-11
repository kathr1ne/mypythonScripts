#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import IPy
import logging

'''
print IPy.IP('10.0.0.0/16').overlaps('10.0.0.0/24')
ip = IPy.IP('192.168.120.0/28')
print ip.len()
for x in ip:
    print x

logging.basicConfig(level=logging.INFO,
                format = '%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s %(message)s',
                datefmt = '%F %T',
                filename = 'mytest.log',
                filemode = 'a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.debug("this is debug msg")
logging.info("this is info msg")
logging.warning("this is warning msg")
'''

with open('/home/kongshuai/workspace/iproute/CollectedIP.ip', 'r') as f:
    for line in f:
        if not line.startswith('#'):
            area = line.strip('\n').split()[0]
            ip = line.strip('\n').split()[-1]
            ipa = ip.split('.')[0]
            print area,ip,ipa
