#!/usr/bin/env python
# coding: utf8
#

import time
import random
from multiprocessing.dummy import Pool
#from multiprocessing import Pool

data = [3,9,1,5,8,2,4]

def addnum(n):
    sum = 0
    for i in range(500):
        sum += n

    time.sleep(n+1)
    print "%d: %d" % (n, sum)

#map(addnum, data)
pool = Pool(7)
pool.map(addnum, data)
pool.close()
pool.join()
