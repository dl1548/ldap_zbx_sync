# -*- coding:utf-8 -*-
# Author: zili

import urllib
import requests
import json
from config import *


class Zbx():
    def __init__(self,
                 zbx_host=ZABBIX_HOST,
                 api_url=ZABBIX_API,
                 user=ZABBIX_USER,
                 password=ZABBIX_PWD):
        self.user = user
        self.password = password
        self.zbx_host = password
        self.api_url = api_url

    #登录，获取auth
    def login(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.password
            },
            "id": 0
        }
        headers = {"Content-Type": "application/json"}
        try:
            req = requests.post(self.api_url,
                                data=json.dumps(data),
                                headers=headers,
                                timeout=3)
            self.auth = req.json()["result"]
            #print(self.auth)
            return self.auth
        except:
            return "Get auth error"

    #获取指定组id
    def get_usrgrpid(self, groupname):
        self.login()
        data = {
            "jsonrpc": "2.0",
            "method": "usergroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": groupname
                },
                "status": 0
            },
            "auth": self.auth,
            "id": 1
        }
        try:
            req = requests.post(
                self.api_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json-rpc"},
                timeout=5)
            res_json = req.json()
            #print res_json
            return res_json['result'][0]['usrgrpid']

        except Exception as exc:
            return 'connect error-0'
        return 1

    #创建用户
    def create_user(self, user_info, groupname=ZABBIX_GROUP):
        self.login()
        group_id = self.get_usrgrpid(groupname)
        data = {
            "jsonrpc": "2.0",
            "method": "user.create",
            "params": {
                "alias": user_info[0],
                "surname": user_info[1],
                "name"   : user_info[2],
                "passwd": ZBX_NEW_USER_DEFAULT_PWD,
                "usrgrps": [{
                    "usrgrpid": group_id
                }],
            },
            "auth": self.auth,
            "id": 1
        }
        try:
            req = requests.post(
                self.api_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json-rpc"},
                timeout=5)
            res_json = req.json()
        except Exception as exc:
            return 'connect error-1'
        return 1

    #获取用户列表
    def get_userlist(self):
        user_list = []
        self.login()
        data = {
            "jsonrpc": "2.0",
            "method": "user.get",
            "params": {
                "output": "extend"
            },
            "auth": self.auth,
            "id": 1
        }
        try:
            req = requests.post(
                self.api_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json-rpc"},
                timeout=5)
            res_json = req.json()
            get_info = res_json['result']
            #get_info = res_json['result'][0]['alias']
            i = 0
            while i < get_info.__len__():
                user_list.append(get_info[i]['alias'])
                i += 1
            if 'guest' in user_list:
                user_list.remove('guest')
            return user_list
        except Exception as exc:
            return 'connect error-2'
        return 1

    #获取用户ID
    def get_userid(self, username):
        self.login()
        data = {
            "jsonrpc": "2.0",
            "method": "user.get",
            "params": {
                "output": "extend",
                "filter": {
                    "alias": username
                },
            },
            "auth": self.auth,
            "id": 1
        }
        try:
            req = requests.post(
                self.api_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json-rpc"},
                timeout=5)
            res_json = req.json()
            userid = res_json['result'][0]['userid']
            return userid
        except Exception as exc:
            return 'connect error-3'
        return 1

    #删除用户
    def del_user(self, username):
        self.login()
        data = {
            "jsonrpc": "2.0",
            "method": "user.delete",
            "params": [
                self.get_userid(username),
            ],
            "auth": self.auth,
            "id": 1
        }
        try:
            req = requests.post(
                self.api_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json-rpc"},
                timeout=5)
        except Exception as exc:
            return 'connect error-4'
        return 1
