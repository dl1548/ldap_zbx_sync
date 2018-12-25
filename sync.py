#!/usr/bin/python
#coding: utf-8

from moudle import get_ldap,zbx
import time
#ldap相关信息，根据实际情况修改
ldap_url = 'ldap://192.168.1.98'
domain_name = u'jktest.cn'
ldap_user = u'Admin'
ldap_pwd = u'123qweASD'

baseDN = u'dc=jktest,dc=cn'
baseOU = u'ou=IT,ou=Shanghai,ou=China'

# baseOU下存在多个ou时填写ou_list,否则为空
ou_list=['IT Public']
#ou_list=[]
# ou下存在组时,且需要同步组成员时填写
ou_group_list=['testGroup']
#ou_group_list=[]

# user : 同步ou下用户
# group : 同步ou下组内成员
# all : 用户和组内成员全部同步
sync_option='all'


# zabbix相关信息,根据实际情况修改
zbx_host='192.168.1.100'
api_url="http://%s/zabbix/api_jsonrpc.php"%zbx_host
zbx_user="admin1"
zbx_pwd="zabbix"
#新加用户分配到的组(提前在zbx创建)
groupname = 'ldap_sync' 




'''
------------此处以上为可修改内容,以下勿动--------------
'''


ldap_user_list=[]
if sync_option=='user':
	if ou_list:
		for ou in ou_list:
			basedn = "ou=" + ou + ',' + baseOU + ',' + baseDN
			ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
			user_list = ldap_conn.search_ou_user(basedn)
			for member in user_list:
				ldap_user_list.append(member)
			print ldap_user_list
	else:
		basedn = baseOU + ',' + baseDN
		ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
		user_list = ldap_conn.search_ou_user(basedn)
		for member in user_list:
				ldap_user_list.append(member)
		print ldap_user_list

if sync_option=='group':
	if ou_list:
		for ou in ou_list:
			basedn = "ou=" + ou + ',' + baseOU + ',' + baseDN
			ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
			group_info = ldap_conn.search_ou_group(basedn)
			for g in ou_group_list:
				if g in group_info:
					user_list = group_info[g]
					for member in user_list:
						ldap_user_list.append(member)
		print ldap_user_list
	else:
		basedn = baseOU + ',' + baseDN
		ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
		group_info = ldap_conn.search_ou_group(basedn)
		for g in ou_group_list:
				if g in group_info:
					user_list = group_info[g]
					for member in user_list:
						ldap_user_list.append(member)
		print ldap_user_list

if sync_option=='all':
	if ou_list:
		for ou in ou_list:
			basedn = "ou=" + ou + ',' + baseOU + ',' + baseDN
			ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
			user_info = ldap_conn.search_ou_user(basedn)
			for member in user_info:
				ldap_user_list.append(member)
			group_info = ldap_conn.search_ou_group(basedn)
			if ou_group_list:
				for g in ou_group_list:
					if g in group_info:
						user_list = group_info[g]
						for member in user_list:
							ldap_user_list.append(member)	
		ldap_user_list=list(set(ldap_user_list))
	else:
		basedn = baseOU + ',' + baseDN
		ldap_conn = get_ldap.LdapToZbx(ldap_url,domain_name,ldap_user,ldap_pwd)
		user_info = ldap_conn.search_ou_user(basedn)
		for member in user_info:
				ldap_user_list.append(member)
		group_info = ldap_conn.search_ou_group(basedn)
		for g in ou_group_list:
				if g in group_info:
					user_list = group_info[g]
					for member in user_list:
						ldap_user_list.append(member)
		ldap_user_list=list(set(ldap_user_list))


zbx = zbx.Zbx(zbx_host,api_url,zbx_user,zbx_pwd)
zbx_user_list = zbx.get_userlist()

#创建用户
for username in ldap_user_list:
	if username not in zbx_user_list:
		try:
			zbx.create_user(username,groupname)
			date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print date + " add user " + username
		except Exception as e:
			print 'connect error'

# #删除用户
# for username in zbx_user_list:
# 	if username not in ldap_user_list:
# 		try:
# 			zbx.del_user(username)
# 			date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# 			print date + " remove user " + username
# 		except Exception as e:
# 			print 'connect error'

	