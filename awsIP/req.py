#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import requests

url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
r = requests.get(url)
awsipv4 = r.json()['prefixes']
globalip = []
for ip in awsipv4:
    if ip['region'] == 'GLOBAL':
        globalip.append(ip['ip_prefix'])

print set(globalip)
