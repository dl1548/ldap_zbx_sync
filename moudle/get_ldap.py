#coding: utf-8
import ldap
'''
import requests
import urllib
import json
'''
class LdapToZbx():
    def __init__(self,ldap_url,domain_name,admin_user,admin_pwd):
        self.ldap_url = ldap_url
        self.domain_name = domain_name
        self.admin_user = admin_user
        self.admin_pwd = admin_pwd
        ldap_user = '%s@%s' %(admin_user,domain_name)
        self.con = ldap.initialize(ldap_url) #初始连接
        self.con.protocol_version = ldap.VERSION3 #LDAP 版本
        try:
            self.con.simple_bind_s(ldap_user,admin_pwd)
        #except ldap.LDAPError,err:
        except:
#            self.ldap_error = 'Connect to %s failed, Error:%s.' %(ldap_url,err.message['desc'])
            return 'connect ldap error'

    def search_ou_user(self,baseDN):
        user_list=[]
        searchFilter = '(&(objectClass=person))' #只查找objectClass=person的
        results = self.con.search_s(baseDN,ldap.SCOPE_SUBTREE,searchFilter)
        if results is not None:
            for person in results:
                username = person[1]['sAMAccountName'][0]
                user_list.append(username)
            return user_list
