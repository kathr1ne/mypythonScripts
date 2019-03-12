#!/usr/bin/env python
# -*- cooding:utf-8 -*-
#

a = [{'aa': '111'}, {'aa': '222'}, {'bb': '333'}, {'dd': '444'}]
print a

c = []
for i in a:
	c.append(i.keys()[0])

country = set(c)

data = {}
for i in country:
	data[i] = []
	b = a[:]
	for x in a:
		try:
			data[i].append(x[i])
			b.remove(x)
			print a
		except:
			pass
	a = b[:]

print a
print data
