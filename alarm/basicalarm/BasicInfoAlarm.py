#!/usr/bin/python
# -*- coding=utf-8 -*-
# karub1n@163.com

import os
import sys
import time
import json
import requests
import logging
from configparser import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

def get_times():
    return int(time.time())

def get_token(corpid, secret):
    conf = os.getcwd() + '/basicalarm/BasicInfoAlarm.ini'
    cfg = ConfigParser()
    cfg.read(conf)
    access_token = cfg.get('token', 'access_token')
    difft = get_times() - int(cfg.get('token', 'expires_time'))
    if difft < 7200:
        token = access_token
        logging.info("Use the already obtained token")
    else:
        tokenurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        Data = {"corpid": corpid, "corpsecret": secret}
        r = requests.get(url=tokenurl, params=Data)
        if r.json()['errmsg'] == 'ok':
            token = r.json()['access_token']
            logging.info("Re-request token.")
            cfg.set('token', 'access_token', token)
            cfg.set('token', 'expires_time', str(get_times()))
            with open(conf, 'w') as f:
                cfg.write(f)
        else:
            logging.warning("r.json()['errmsg']")
    return token

def sendmessage(*args):
    Corpid = "ww79103287186dce91"
    Secret = "B4qfZEfo_6F9-IS6K6_cDIcNmDTEszn81mYz4q-l4Jc"
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(get_token(Corpid, Secret))
    wechat_json = {
        "touser":"@all",
        "msgtype": "text",
        "agentid": "1000004",
        "text": {
            "content": "[Qeeu node Basic Info Alarm]\nIP: {}\nitem: {}\ntime: {}\ncontent: {}".format(args[1], args[2], args[0], args[3])
        },
        "safe": "0"
    }
    response = requests.post(url, data=json.dumps(wechat_json, ensure_ascii=False, encoding='utf8'))
    if response.json()['errmsg'] == 'ok':
        logging.info("Sendmessage api response is ok")
    else:
        logging.warning(response.json()['errmsg'])

def setlog(log):
	logging.basicConfig(level=logging.INFO,
                format = '%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s %(message)s',
                datefmt = '%F %T',
                filename = log,
                filemode = 'w')

setlog(os.getcwd() + '/basicalarm/BasicInfoAlarm.log')

if __name__ == '__main__':
    title = "test"
    content = "just test"
    sendmessage(title, content)
