#!/usr/bin/python
# -*- coding:utf-8 -*-
#

from __future__ import division
import os,sys

def Mem():
    mem = os.popen("free -m").read()
    Mem = mem.split("\n")[1]
    buffer_cache = mem.split("\n")[2]
    total = Mem.split()[1]
    used = buffer_cache.split()[2]
    used_percent = int(used)/int(total)*100
    return used_percent

def Cpu():
    CPU = os.popen("sar 5 3").read()
    idle = CPU.split()[-1]
    cpu_percent = (100 - float(idle))
    return cpu_percent

def disk(root):
    disk = os.statvfs(root)
    if root == "/":
        disk_percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail) + 1
    else:
        disk_percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail)
    return disk_percent

def main():
    log = "/usr/local/Monitor/Salt/checkComputer/server_info.log"
    with open (log,'w+') as f:
        root = ["/"]
        for i in range(13):
            root.append("/data" + str(i))
        for d in root:
            if os.path.exists(d) and d == "/":
                print >> f, "%s使用率:%.0f%%" % (d,disk(d)),
            elif os.path.exists(d):
                print >> f, "%s使用率:%.0f%%" % (d[1:],disk(d)),
            else:
                pass
        print >> f, "CPU使用率:%.2f%%" % Cpu(),
        print >> f, "内存使用率:%.2f%%" % Mem()

if __name__ == "__main__":
    main()
