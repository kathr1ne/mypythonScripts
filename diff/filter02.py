#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

fd = {}

def diffnet(file1, file2):
    net = []
    with open(file1, 'r') as f:
		lines = f.readlines()
		count = len(lines)
		for d in xrange(count): 
			fd[d] = lines[d].strip()
	
    with open(file2, 'r') as f:
        for l in f.readlines():
			if l.strip() not in fd.values():
				net.append(l.strip())
        return net

new = 'sg.list'
old = 'sg.list.old'
print(diffnet(new, old))
print("######")
print(diffnet(old, new))
