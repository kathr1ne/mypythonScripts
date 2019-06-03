#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


import sys

def check_bit(src_ip):
    items = src_ip.split('.')
    for k, v in enumerate(items):
        if len(v) == 1:
            items[k] = '00' + v
        elif len(v) == 2:
            items[k] = '0' + v
        elif len(v) == 3:
            pass
    return '.'.join(items)

if __name__ == '__main__':
    src_ip = sys.argv[1]
    dst_ip = check_bit(src_ip)
    print dst_ip
