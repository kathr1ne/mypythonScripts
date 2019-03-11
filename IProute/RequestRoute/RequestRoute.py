#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import time
import requests

def requestroute(url, num):
	while num <= 10:
		r = requests.get(url)
		print r.status_code
		if r.status_code is requests.codes.ok:
			return r.text
			break
		else:
			print("Requests get failed, Please check")
			num = num + 1
			print(num)
			time.sleep(5)
			return requestroute(url, num)


if __name__ == '__main__':
	num = 0
	url = 'http://operation.qeeyou.cn:8000/loadpage/noderoute'
	route = requestroute(url, num)
	with open('noderoute.txt', 'w') as f:
		f.write(route)
