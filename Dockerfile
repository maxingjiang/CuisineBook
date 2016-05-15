FROM ubuntu:14.04.3

MAINTAINER codemeow codemeow@yahoo.com

RUN cp /etc/apt/sources.list /etc/apt/sources.list.raw
ADD https://github.com/codemeow5/software/raw/master/ubt_sources_list_aliyun.txt /etc/apt/sources.list
RUN apt-get update && apt-get install wget -y

RUN apt-get install python-pip build-essential python-dev -y
RUN echo "mysql-server mysql-server/root_password password 123456" | /usr/bin/debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password 123456" | /usr/bin/debconf-set-selections
RUN apt-get install mysql-server -y
RUN pip install tornado
RUN pip install BeautifulSoup4
RUN pip install Tornado-MySQL
RUN pip install redis

EXPOSE 80

RUN echo Asia/Shanghai > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata

COPY web.py /root/
COPY common.py /root/
COPY config.py /root/
COPY handler.py /root/
COPY travellers.sql /root/
RUN /etc/init.d/mysql restart && \
	mysql -uroot -p123456 -e"CREATE DATABASE \`travellers\`" && \
	mysql -uroot -p123456 travellers < /root/travellers.sql
COPY redis-start.sh /root/
RUN mkdir /root/redis-config
COPY redis-config /root/redis-config/
RUN mkdir /root/travellers
COPY travellers /root/travellers/
RUN /root/redis-start.sh
CMD /etc/init.d/mysql restart && \
	/root/redis-start.sh && \
	/usr/bin/python /root/web.py

