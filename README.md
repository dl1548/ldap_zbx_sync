ldap_zbx_sync
#### 安装依赖
yum -y install python-devel libevent-devel openldap-devel

##### 下载pip包，安装pip

##### 安装模块
requests 

urllib3 

pyOpenSSL

requests

gevent

python-ldap


##### 定时执行即可
`* */3 * * * /usr/bin/python /$path/sync.py >>/tmp/ldap_zbx_sync.log 2>&1`
