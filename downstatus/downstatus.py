#!/usr/bin/env python
# -*- coding: utf-8 -*-
# karub1n@163.com

import re
import sys
import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime, timedelta, timezone

service = sys.argv[1]
url = 'https://downdetector.com/status/{}'.format(service)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

def str2datetime(s):
    """ str2datetime return str HH:MM"""
    d = datetime.strptime(s[0:-6], '%Y-%m-%dT%H:%M:%S.%f')
    dt = d.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-11)))
    return dt.strftime('%H:%M')

'''
def has_cht(tag):
    return tag.has_attr('class') and tag.has_attr('href') and tag.has_attr('title')

ServerName = []
for i in soup.find_all(has_cht):
    ServerName.append(i['href'])
'''
'''
"""re.sub replace str"""
rep = {'date':'"date"', 'value':'"value"', chr(39):chr(34)}
rep = dict((re.escape(k), v) for k, v  in rep.items())
pattern = re.compile("|".join(rep.keys()))
r = pattern.sub(lambda m: rep[re.escape(m.group(0))], c)
'''
x = []
y = []
pat = re.compile(r'{.*date.*value.*}')
r = str(soup.find_all('script')[13])
xy = r.replace('date', '"date"').replace('value', '"value"').replace(chr(39), chr(34)).strip()
for i in pat.findall(xy):
    x.append(str2datetime(json.loads(i)['date']))
    y.append(json.loads(i)['value'])

# l = [(int(i[11:13])+13)%24 for i in x]
# plt.plot(x, y)
fig, ax = plt.subplots(1,1)
ax.plot(x, y)
plt.xlabel('Last 24 hours')
plt.ylabel('User reports')
plt.title('{} problems'.format(sys.argv[1]))
ax.xaxis.set_major_locator(ticker.MultipleLocator(12))

plt.show()

print(len(x))
