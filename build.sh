#!/bin/bash

if [[ $# != 1 ]];then
	echo "Usage: $0 [check|start|stop]"
	exit -1;
fi
if [[ $1 == "check" ]];then
	py=`which python`
	if  [[ "${py}x" == "x" ]];then
		echo "python comand not found,now installing python-dev......"
		apt-get install python-dev -y
	fi
	msql=`which mysqld`
	if [[ "${msql}x" == "x" ]];then
		echo "mysqld not found,now installing mysql-server......"
		echo "mysql-server mysql-server/root_password password 123456" | /usr/bin/debconf-set-selections
		echo "mysql-server mysql-server/root_password_again password 123456" | /usr/bin/debconf-set-selections
		apt-get install mysql-server -y
	fi
	pip=`which pip`
	if [[ "${pip}x" == "x" ]];then
		echo "pip not found,now installing python-pip......"
		apt-get install python-pip -y
	fi
	echo "install tornado for python plguin......"
	pip install tornado &> .log

	echo "install BeautifulSoup4 for python plguin......"
	pip install BeautifulSoup4 &>> .log

	echo "install Tornado-MySQL for python plguin......"
	pip install Tornado-MySQL &>> .log

	echo "install redis for python plguin......"
	pip install redis &>> .log

	redis=`which redis-server`
	if [[ "${redis}x" == "x" ]];then
		echo "redis-server not found,now installing redis-server......"
		apt-get install redis-server -y &>> .log
		#redis-server ./redis-config/6379.conf
	fi
	mkdir -p /var/lib/redis/6379
	mkdir -p /var/run/redis
	
	echo "start redis server port 6379......"
	echo "start mysql server and creat database......"
	/etc/init.d/mysql restart && \
        mysql -uroot -p123456 -e"CREATE DATABASE \`cuisinebook\` character set utf8;" && \
        mysql -uroot -p123456 cuisinebook < ./cuisinebook.sql  &>> .log
	

elif [[ $1 == "start" ]];then
	echo 'Server is running, listening on port 8083....'
	./webcuisine.py &
	ps > .pidfile
elif [[ $1 == "stop" ]];then
	pid=`cat .pidfile | grep "webcuisine.py" | awk '{print $1}'`
	kill -9 $pid
	echo "stop the webcuisine"
fi
