#!/bin/bash

apt-get install redis-server -y
/etc/init.d/redis-server stop

mkdir -p /var/lib/redis/6379
mkdir -p /var/lib/redis/6380
mkdir -p /var/run/redis

redis-server /root/redis-config/6379.conf
echo 'Service 6379 has been started'
redis-server /root/redis-config/6380.conf
echo 'Service 6380 has been started'

