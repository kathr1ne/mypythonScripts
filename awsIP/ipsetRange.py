#!/usr/bin/env python
# -*- coding: utf-8-*-
#

from IPy import IP, IPSet

s = IPSet()
CIDR = []
region = []

#us = []
with open('iprange.txt', 'r') as f:
    for l in f.readlines():
        s.add(IP(l.strip().split()[0], make_net = True))
            #print l.strip().split()
#            line = l.strip().split()
#            CIDR.append(line[0])
#            region.append(line[1])
#
'''
print CIDR
setr = set(region)
for r in setr:
    print r,region.count(r)

'''
print s
