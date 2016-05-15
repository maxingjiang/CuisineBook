#!/usr/bin/python

import os

VERSION = '0.0.1'

Mode = 'DEBUG'
#Mode = 'RELEASE'

## MySQL Configuration

MySQL_Unix_Socket = '/var/run/mysqld/mysqld.sock'
MySQL_User = 'root'
MySQL_Passwd = '123456'
MySQL_DB = 'cuisinebook'
MySQL_CHARSET = 'utf8'


# Host Ip
Hostip = '192.168.211.133:8083'
## Redis Configuration

Redis_Unix_Socket = '/var/run/redis/redis-6379.sock'

AuthCode_ExpireTime = 60 * 60 * 10
Cookie_ExpireTime = 60 * 60 * 24 * 30

#error code
json_parameter_error = -1
keyword_error = -2
userid_or_password_wrong = -3
tel_not_found = -4
tel_format_not_correct = -5
connect_redis_failed = -6
user_not_found = -7
logout_failed = -8
reset_failed = -9
change_failed = -10
update_userinfo_failed = -11
user_not_exit = -12
icon_not_exit = -13
update_icon_failed = -14
user_exist = -15
user_not_exist = -16
cuisine_exit = -20
add_cuisine_failed = -21
get_cuisine_failed = -22
product_exit = -23
add_product_failed = -24
get_product_failed = -25
add_image_failed = -26
get_image_failed = -27
image_exit = -28
image_not_exit = -29