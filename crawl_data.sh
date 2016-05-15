#!/bin/bash
mysql -uroot -p123456 -e"CREATE DATABASE \`cuisine_crawl\` character set utf8;" && \
mysql -uroot -p123456 cuisine_crawl < ./cuisine_crawl.sql  &>> .log

#mysqldump cuisine_crawl -uroot -p > crawl_data.sql
