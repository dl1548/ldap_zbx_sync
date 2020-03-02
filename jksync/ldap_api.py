# -*- coding:utf-8 -*-
# Author: zili

import ldap
from config import *


class LdapToZbx():
    def __init__(self,
                 ldap_url=LDAP_URL,
                 domain_name=LDAP_DOMAIN_NAME,
                 admin_user=LDAP_USER,
                 admin_pwd=LDAP_PWD):
        self.ldap_url = LDAP_URL
        self.domain_name = LDAP_DOMAIN_NAME
        self.admin_user = LDAP_USER
        self.admin_pwd = LDAP_PWD
        self.ldap_user = '%s@%s' % (LDAP_USER, LDAP_DOMAIN_NAME)

        self.con = ldap.initialize(LDAP_URL)
        self.con.protocol_version = ldap.VERSION3
        try:
            self.con.simple_bind_s(self.ldap_user, self.admin_pwd)
        except:
            return {'error': 'bind failed'}

    def get_ou_guid(self, baseDN):
        searchFilter = '(&(objectClass=OrganizationalUnit))'
        results = self.con.search_s(baseDN, ldap.SCOPE_SUBTREE, searchFilter,
                                    ['distinguishedName', 'objectGUID'])
        if results:
            for i in results:
                if i[0] == baseDN:
                    return i[1]['objectGUID']
        else:
            return {'error': 'The ou was not found'}

    #SCOPE_BASE (基数：查询指定DN，也就是在DN中指定的那个，就只查这DN的)
    #SCOPE_ONELEVEL (一级：查询指定DN下的一级子目录，不会查子目录的子目录)
    #SCOPE_SUBTREE (子树：查询指定DN下的所有目录，包括指定DN)
    def search_ou_user(self, baseDN=LDAP_SYNC_OU_USER):
        user_list = []
        searchFilter = '(&(objectClass=person))'
        try:
            for ou in baseDN:
                results = self.con.search_s(ou + ',' + LDAP_BASE_DN,
                                            ldap.SCOPE_ONELEVEL, searchFilter)
                if results is not None:
                    for person in results:
                        # print(person[1])
                        if isinstance(person[1],dict) and 'sAMAccountName' in person[1].keys():
                            username = person[1]['sAMAccountName'][0].split('@')[0]
                            user_list.append(username)
                        else:
                            username = person[1]['userPrincipalName'][0]
                            user_list.append(username)
            return user_list
        except Exception as e:
            return str(e)

    # group下 SCOPE_ONELEVEL 无法取得组内成员要使用SCOPE_SUBTREE
    def search_group_user(self, baseDN=LDAP_SYNC_OU_USER):
        user_list = []
        searchFilter = '(&(objectClass=person))'
        results = self.con.search_s(baseDN, ldap.SCOPE_SUBTREE, searchFilter)
        if results is not None:
            for person in results:
                # print(person[1])
                if isinstance(person[1],dict) and 'sAMAccountName' in person[1].keys():
                    username = person[1]['sAMAccountName'][0].split('@')[0]
                    user_list.append(username)
                else:
                    username = person[1]['userPrincipalName'][0]
                    user_list.append(username)                    
            return user_list

    def search_ou_group(self, baseDN):
        data_dict = {}
        searchFilter = '(&(objectClass=group))'
        results = self.con.search_s(baseDN + ',' + LDAP_BASE_DN,
                                    ldap.SCOPE_ONELEVEL, searchFilter)
        # print results
        if results is not None:
            for i, allinfo in enumerate(results):
                i = []
                if 'name' in allinfo[1]:
                    group = allinfo[1]['name'][0]
                if 'member' in allinfo[1]:
                    # for cn in allinfo[1]['member']:
                    #     v = cn.split(',')
                    #     member = v[0].split('=')
                    #     i.append(member[1])
                    for cn in allinfo[1]['member']:
                        loginname = self.search_group_user(cn)
                        if loginname:
                            i.append(loginname[0])
                data_dict[group] = i

            return data_dict
        else:
            return {'error': 'The ou_group was not found'}
