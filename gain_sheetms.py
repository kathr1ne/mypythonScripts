#!/usr/bin/env python
# -*- coding:utf-8 -*-
# write pingResult to excel

import subprocess
import xlwt
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

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('pingTest', cell_overwrite_ok=True)
sheet.write(0, 0, "服务器地点")
sheet.write(0, 1, "运营商")
sheet.write(0, 2, "目标IP")
sheet.write(0, 3, "访问速度")
sheet.write(0, 4, "丢包率")

col0 = sheet.col(0)
col0.width = 256*20
col1 = sheet.col(1)
col1.width = 256*20
col2 = sheet.col(2)
col2.width = 256*20  
col3 = sheet.col(3)
col3.width = 256*70    
col4 = sheet.col(4)
col4.width = 256*20    

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

def setSheetData(ip, sheet, index):
    i = index
    CMD = PingCMD.replace("IP", ip[2])
    result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE)
    out, err = result.communicate()
    out = out.decode('utf8')
    cmd_out = out.rstrip().split("\n")
    try:
        lostStr = cmd_out[-2].split(",")[2].split(" ")[1]+' Loss'
        speedStr = cmd_out[-1].strip().split(" ")[-2].split("/")
        speedStr = "Min = "+speedStr[0]+"ms，Max = "+speedStr[2]+"ms，Avg = "+speedStr[1]+"ms，mdev = "+speedStr[3]+"ms"
    except:
        lostStr = cmd_out[-1].split(",")[2].split(" ")[1]+' Loss'
        speedStr = "NoPing, Please change the IP."
    mutex.acquire()#取得锁 
    sheet.write(i, 0, ip[0])
    sheet.write(i, 1, ip[1])
    sheet.write(i, 2, ip[2])
    sheet.write(i, 3, speedStr)
    sheet.write(i, 4, lostStr)
    print("finish %s %s" % (ip[0], ip[2]))
    mutex.release() # 释放锁   
    
threads = [] 
if 0==len(IPList):
    print("no data")
else:
    print("start:", getNow())
    mutex = threading.Lock() # 创建锁
    for ip in IPList:
        index += 1
        a = threading.Thread(target=setSheetData, args=(ip, sheet, index))
        a.start()        
        threads.append(a)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("end:", getNow())
    hostname = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)	
    h, e = hostname.communicate()	
    book.save(curDir + r'/pingResult_%s.xls'%h.split("\n")[0])
