# GOGO

# secrets formats

## FULL_CONF

IPSec gateway x.x.x.x
IPSec ID group 
IPSec secret group_key 
Xauth username username 
Xauth password password

## FULL_HOSTS

name1 ansible_host=x.x.x.x ansible_user=username ansible_passwd=password
name1 ansible_host=x.x.x.x ansible_user=username ansible_passwd=password
...
name1 ansible_host=x.x.x.x ansible_user=username ansible_passwd=password

[all:vars]
ansible_python_interpreter=/usr/bin/python3.6
