#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import subprocess


def shellcmd(CMD):
    result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.communicate()

def checkroute():
    dic = {'sg':'gre2', 'us':'gre3', 'eu':'gre5', 'jp':'gre6', 'kr':'gre7', 'main':'main', 'vpn0':'gre1'}
    for d in dic:
        cmd = "ip route show table {}".format(d)
        out, err = shellcmd(cmd)
        if not out:
            cmd = "ip route add default dev {} table {}".format(dic[d], d)
            print(cmd)

checkroute()
