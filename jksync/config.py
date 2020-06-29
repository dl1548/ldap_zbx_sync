#!/usr/bin python
# -*- coding: utf-8 -*-

# ZABBIX 设置
ZABBIX_HOST = u'192.168.1.93'
ZABBIX_USER = u'admin'
ZABBIX_PWD = u'zabbix'
ZABBIX_GROUP = u'tttt'
ZBX_NEW_USER_DEFAULT_PWD = u'jkstack'
ZABBIX_API=u"http://%s/monitor/api_jsonrpc.php"%ZABBIX_HOST

# AD-LDAP设置
LDAP_USER = u'Admin'
LDAP_PWD = u'123qweASD'
LDAP_DOMAIN_NAME = u'jktest.cn'
LDAP_URL = u'ldap://192.168.1.98'
LDAP_BASE_DN = u'dc=jktest,dc=cn'

# 同步OU下用户，不需要则为空
LDAP_SYNC_OU_USER = [
    #'ou=IT,ou=Shanghai,ou=China',
    'ou=IT Public,ou=IT,ou=Shanghai,ou=China',
]

# 同步OU下的组内成员，不需要则为空
LDAP_SYNC_OU_GROUP = {
    # 组：组所在ou
    'group-t':'ou=IT,ou=Shanghai,ou=China',
}
