#!/usr/bin/env python
# -*- coding: utf-8 -*-
# karub1n@163.com

import time
import subprocess
from basicalarm import BasicInfoAlarm

def shellcmd(CMD):
    r = []
    result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r.append(result.communicate())
    r.append(result.wait())
    return r

def getnow():
    return time.strftime('%F %T', time.localtime())

if __name__ == '__main__':
    t = getnow()
    cmd = "salt-run manage.down"
    errid = shellcmd(cmd)
    item = "salt-minion status"
    content = "Minion did not return. No response or No connect"
    for i in errid[0][0].split('\n'):
        if i:
            ip = i.strip('- ')
            BasicInfoAlarm.sendmessage(t, ip, item, content)
