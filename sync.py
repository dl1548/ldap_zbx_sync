#!/usr/bin python
# -*- coding: utf-8 -*-

import json
import time
from jksync import zbx_api, ldap_api
from jksync.config import LDAP_SYNC_OU_USER, LDAP_SYNC_OU_GROUP


zbx_conn = zbx_api.Zbx()
zbx_user_list = zbx_conn.get_userlist()
# print(zbx_user_list)

ldap_conn = ldap_api.LdapToZbx()
if len(LDAP_SYNC_OU_USER) > 0:
    ldap_user_list = ldap_conn.search_ou_user()
# print user_list

ldap_group_user_list=[]
if len(LDAP_SYNC_OU_GROUP) > 0:
    for grp,ou in LDAP_SYNC_OU_GROUP.items():
        group_info = ldap_conn.search_ou_group(ou)
        if grp in group_info:
            user_list = group_info[grp]
            for member in user_list:
                ldap_group_user_list.append(member)
# print ldap_group_user_list


for username in ldap_user_list+ldap_group_user_list:
    if username not in zbx_user_list:
        try:
            zbx_conn.create_user(username)
            date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print date + " add user " + username
        except Exception as e:
            print 'connect error'