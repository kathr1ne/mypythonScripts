#!/usr/bin/env python
# -*- coding:utf-8 -*-
# karub1n@163.com

import time
import pickle
import os
from basicalarm import BasicInfoAlarm
 
class LogIncScaner(object):
    def __init__(self, log_file, seek_file='/tmp/log-inc-scan.seek.temp'):
        self.log_file = log_file
        self.seek_file = seek_file
 
    def scan(self):
        seek = self._get_seek()
        file_mtime = os.path.getmtime(self.log_file)
        if file_mtime <= seek['time']:
            print 'file mtime not change since last scan'
            seek['time'] = file_mtime
            self._dump_seek(seek)
            return []
 
        file_size = os.path.getsize(self.log_file)
        if file_size <= seek['position']:
            print 'file size not change since last scan'
            seek['position'] = file_size
            self._dump_seek(seek)
            return []
 
        print 'file changed,start to scan'
        with open(self.log_file, 'rb') as logfd:
            logfd.seek(seek['position'],os.SEEK_SET)
            matchs = logfd.readlines()
            seek = {'time':time.time(),'position': logfd.tell()}
            print seek
            self._dump_seek(seek)
        return matchs
 
    def _get_seek(self):
        seek = {'time':time.time(),'position':0}
        if os.path.exists(self.seek_file):
            with open(self.seek_file,'rb') as seekfd:
                    try:
                        seek = pickle.load(seekfd)
                    except:
                        pass
        print seek
        return seek
 
    def _dump_seek(self, seek):
        with open(self.seek_file,'wb') as seekfd:
            pickle.dump(seek,seekfd)
 
    def reset_seek(self):
        self._dump_seek({'time':time.time(),'position':0})
 
if __name__ == "__main__":
    scaner = LogIncScaner('/var/log/baseinfo_check.log')
    scaner.reset_seek()
    while True:
        matchs = scaner.scan()
        for l in matchs:
            line = l.strip().split()
            t = ' '.join(line[0:2])
            ip = line[2]
            level = line[3]
            item = line[4].strip(':')
            content = ' '.join(line[5::])
            BasicInfoAlarm.sendmessage(t, ip, item, content)
        time.sleep(5)
