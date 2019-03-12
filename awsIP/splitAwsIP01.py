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
            #line = ' '.join(ipinfo)
            line = "{} {} {}".format(ipinfo[-1], ipinfo[0], ipinfo[1])
            f.write(line + '\n')

cmd = "awk '{print $2,$3}' test.ip | uniq -c"
out, err = shellcmd(cmd)
if out:
    lnum = out.split()[::3]

print lnum

ipnet = []
region = []
with open('/root/workspace/test.ip', 'r') as f:
	line = f.readlines()
	for l in line:
		ll = l.strip().split()
		ipnet.append(ll[0])
		region.append("{}{}".format(ll[1], ll[2]))

i = 0
n = 0
x = 0
while i < len(lnum):
	#print IP("{}-{}".format(ipnet[0], ipnet[int(lnum[0])-1]), make_net=True), region[int(lnum[0])-1]
	x = int(lnum[i])
	print IP("{}-{}".format(ipnet[0+n], ipnet[x-1]), make_net=True), region[x-1]
	print "{}-{}".format(ipnet[0+n], ipnet[x-1])
	i += 1
	x = int(lnum[i-1]) + int(lnum[i])
	n = int(lnum[i-1])
	#n = int(lnum[i-1]) + int(lnum[i])
	print "x: %s" % x
	print "i: %s" % i
	print "n: %s" % n
	print "{}-{}".format(ipnet[n], ipnet[x + n  - 1])
