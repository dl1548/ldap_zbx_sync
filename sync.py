#!/usr/bin/python
#coding: utf-8

from moudle import get_ldap
from moudle import zbx
import time
#ldap相关信息，根据实际情况修改
ldap_url = 'ldap://xxx.xxx.xxx.xxx'
domain_name = u'xxxxx.cn'
ldap_user = u'xxxxxxxxx'
ldap_pwd = u'xxxxxxxxxx'
#ou的层级  1：没有层级，直接写。2：有层级则从内到外开始写多个ou
baseDN = u'ou=H,ou=IT,ou=Shanghai,ou=China,dc=xxxxxxx,dc=cn'

#获取ldap user列表
ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
ldap_user_list = ldap_conn.search_ou_user(baseDN)

print ldap_user_list

#zabbix相关信息,根据实际情况修改
zbx_host='xxx.xxx.xxx.xxx'
api_url="http://%s/zabbix/api_jsonrpc.php"%zbx_host
zbx_user="xxxxxxxx"
zbx_pwd="xxxxxxxxx"

groupname = 'ldap_zbx_sync' #新加zabbix用户分配到的组


zbx = zbx.Zbx(zbx_host,api_url,zbx_user,zbx_pwd)
zbx_user_list = zbx.get_userlist()

print zbx_user_list

'''
#创建用户
for username in ldap_user_list:
	if username not in zbx_user_list:
		try:
			zbx.create_user(username,groupname)
			date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print date + " add user " + username
		except Exception as e:
			print 'connect error'
#删除用户
for username in zbx_user_list:
	if username not in ldap_user_list:
		try:
			zbx.del_user(username)
			date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print date + " remove user " + username
		except Exception as e:
			print 'connect error'
'''
