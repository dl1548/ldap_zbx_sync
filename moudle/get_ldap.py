# -*- coding:utf-8 -*-
# Author: zili

import ldap

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
        except:
            return {'error':'bind failed'}
    def get_ou_guid(self,baseDN):
        searchFilter = '(&(objectClass=OrganizationalUnit))'
        results = self.con.search_s(baseDN,ldap.SCOPE_SUBTREE,searchFilter,['distinguishedName','objectGUID'])
        if results:
            for i in results:
                if i[0] == baseDN:
                    return i[1]['objectGUID']
        else:
            return {'error':'The ou was not found'}
                        
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
                # username = person[1]['userPrincipalName'][0].split('@')[0]
                # user_list.append(username)
            return user_list
        else:
            return {'error':'The ou_user was not found'}

    def  search_ou_group(self,baseDN):
        data_dict={}
        searchFilter = '(&(objectClass=group))'
        results = self.con.search_s(baseDN,ldap.SCOPE_SUBTREE,searchFilter)
        if results is not None:
            for i,allinfo in enumerate(results):
                i=[]
                if 'name' in allinfo[1]:
                    group=allinfo[1]['name'][0]
                if 'member' in allinfo[1]:
                    # for cn in allinfo[1]['member']:
                    #     v = cn.split(',')
                    #     member = v[0].split('=')
                    #     i.append(member[1])
                    for cn in allinfo[1]['member']:
                        loginname=self.search_ou_user(cn)
                        i.append(loginname[0])
                data_dict[group]=i
        
            return data_dict
        else:
            return {'error':'The ou_group was not found'}
