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
    def get_ou_guid(self,baseDN):
        searchFilter = '(&(objectClass=OrganizationalUnit))'
        results = self.con.search_s(baseDN,ldap.SCOPE_SUBTREE,searchFilter,['distinguishedName','objectGUID'])
        #return results
        for i in results:
            if i[0] == baseDN:
                return i[1]['objectGUID']
                        
    #SCOPE_BASE (基数：查询指定DN，也就是在DN中指定的那个，就只查这DN的)
    #SCOPE_ONELEVEL (一级：查询指定DN下的一级子目录，不会查子目录的子目录)
    #SCOPE_SUBTREE (子树：查询指定DN下的所有目录，包括指定DN) 
    def search_ou_user(self,baseDN):
        user_list=[]
        searchFilter = '(&(objectClass=person))' #只查找objectClass=person的
        results = self.con.search_s(baseDN,ldap.SCOPE_SUBTREE,searchFilter)
        if results is not None:
            for person in results:
                username = person[1]['sAMAccountName'][0]
                user_list.append(username)
            return user_list
