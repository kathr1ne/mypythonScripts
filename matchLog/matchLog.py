#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import re
import sys
import time

def getpubip():
    with open('/etc/myshell/new_baseinfo', 'r') as f:
        for line in f:
            if line.startswith('nodeip'):
                ip = line.strip('\n').split('=')
                pubip = ip[1].strip()
    return pubip 

class Log:

    def __init__(self, log_file, match_str, re_ip, re_email, limit_value):
        self.log_file = log_file
        self.match_str = match_str
        self.re_ip = re_ip
        self.re_email = re_email
	self.limit_value = limit_value

    def match_IP(self):
        IP = []
	email = []
        ip_pat = re.compile(self.re_ip)
	email_pat = re.compile(self.re_email)
        with open(self.log_file, 'r') as f:
            line = f.readline()
            while line:
                if self.match_str in line:
                    IP.append(ip_pat.search(line).group())
		    try:
                        email.append(email_pat.search(line).group())
		    except AttributeError:
			pass
                line = f.readline()
        return IP, email

    def getlogtime(self):
	off = -50
        with open(self.log_file, 'r') as f:
            first_line = f.readline()
            while True:
                f.seek(off, 2)
                lines = f.readlines()
                if len(lines) >= 2:
                    last_line = lines[-1]
                    break
                off *= 2
        start_time = time.mktime(time.strptime(first_line[0:24],"%a %b %d %H:%M:%S %Y"))
        end_time = time.mktime(time.strptime(last_line[0:24],"%a %b %d %H:%M:%S %Y"))
        return end_time - start_time

    def count_IP(self):
	# return len(self.match_IP()[0])
        c = 0
        countIP = {}
        for key in self.match_IP()[0]:
            countIP[key] = countIP.get(key, 0) + 1
        for key in countIP:
	    if countIP[key] <= self.limit_value:
                c += countIP[key]
        return c

if __name__ == '__main__':
    try:
        limit_value = int(sys.argv[1])
    except IndexError:
        limit_value = 100
    # match IP
    re_ip = r'(?<![\.\d])(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])'
    # match Email
    re_email = r'(\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14})'
    loger = Log('./openvpn.log', '--ping-exit', re_ip, re_email, limit_value)
    count_all = loger.count_IP()
    time_all = loger.getlogtime()
    print 'Ping exit IP count: {}\nTotal log time: {}s\nAverage/(h): {}'.format(count_all, time_all, count_all/(time_all/60/60))
    print len(loger.match_IP()[0])
