#!/usr/bin/env python
# -*- coding:utf-8 -*-
# write to text

import subprocess
import time
import os,sys
import codecs
import threading

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
curDir = os.getcwd()
def getNow():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

hostname = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
h, e = hostname.communicate()
f = open(curDir + '/pingResult_'+ h.strip("\n") +'.txt', 'w')

index = 0
IPList = []
PingCMD = "ping -c 100 IP"
try:
    IPInfo = codecs.open(curDir + '/IP.txt','r','utf-8')
    data = IPInfo.readlines()
    for d in data:
        ipData = d.split(",")
        ipData[2] = ipData[2].replace("\n", "").replace("\r", "")
        IPList.append(ipData) 
except IOError as err:  
    print('File Error:'+str(err))
finally:
    if 'IPInfo' in locals(): 
        IPInfo.close()

def setFileData(ip, f, index):
    i = index
    CMD = PingCMD.replace("IP", ip[2])
    result=subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE)
    out, err = result.communicate()
    out = out.decode('utf8')
    cmd_out = out.rstrip().split("\n")
    try:
        lostStr = cmd_out[-2].split(",")[2].split(" ")[1]#+' Loss'
        #speedStr = cmd_out[-1].strip().split(" ")[-2].split("/")
        #speedStr = "Min = "+speedStr[0]+"ms，Max = "+speedStr[2]+"ms，Avg = "+speedStr[1]+"ms，mdev = "+speedStr[3]+"ms"
        speedStr = cmd_out[-1].split("/")[-3] 
        speedStr = speedStr + "ms"
    except:
        lostStr = cmd_out[-1].split(",")[2].split(" ")[1]#+' Loss'
        speedStr = "NoPing"
    mutex.acquire()# 取得锁 
    #f.write(ip[0]+"\t"+ip[1]+"\t"+ip[2]+"\t"+speedStr+"\t"+lostStr+"\n")
    f.write(ip[0]+" "+ip[1]+" "+ip[2]+" "+speedStr+" "+lostStr+"\n")
    print("finish %s %s %s" % (ip[0], ip[1], ip[2]))
    mutex.release()# 释放锁   
    
threads = [] 
if 0==len(IPList):
    print("no data")
else:
    print("start:", getNow())
    mutex = threading.Lock()# 创建锁
    for ip in IPList:
        index += 1
        a = threading.Thread(target=setFileData, args=(ip, f, index))
        a.start()        
        threads.append(a)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("end:", getNow())
f.close()
