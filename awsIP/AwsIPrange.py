#!/usr/bin/env python
# -*- utf-8 -*-
#

import requests

info = {}
region = []
url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.361'}
r = requests.get(url, headers=headers)
awsipv4 = r.json()['prefixes']

for i in awsipv4:
    region.append(i['region'])

for i in set(region):
    info[i] = []
    for n in awsipv4:
        if n['region'] == i:
            info[i].append(n['ip_prefix'])

for i in info:
    print("{}: {}".format(i, '\n'.join(x for x in info[i])))
