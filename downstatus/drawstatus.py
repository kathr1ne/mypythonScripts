#!/usr/bin/env python
# -*- coding: utf-8 -*-
# karub1n@163.com

import os

with open('{}{}detector.json'.format(os.getcwd(), os.sep), 'r') as f:
    for line in f:
        print(line)

