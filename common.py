#!/usr/bin/python

import sys, os, uuid
import json
import tornado.web
import tornado_mysql.pools
import redis
import logging

reload(sys)
sys.setdefaultencoding('utf8')

import config

logger = logging.getLogger('webcuisine')

MYSQL_POOL = None
REDIS_CONNECTIONS_0 = None
REDIS_CONNECTIONS_1 = None
REDIS_CONNECTIONS_2 = None

if config.Mode == 'DEBUG':
	tornado_mysql.pools.DEBUG = True

def get_mysql_pool():
	global MYSQL_POOL
	if MYSQL_POOL is not None:
		return MYSQL_POOL
	try:
		MYSQL_POOL = tornado_mysql.pools.Pool(
			dict(unix_socket=config.MySQL_Unix_Socket,
				user=config.MySQL_User,
				passwd=config.MySQL_Passwd,
				db=config.MySQL_DB,
				charset=config.MySQL_CHARSET,
				cursorclass=tornado_mysql.cursors.DictCursor)
			)
	except Exception, e:
		logger.error('An error occurred while getting the MySQL connection pool: %s' % e)
		MYSQL_POOL = None
	return MYSQL_POOL

def get_redis_0():
	global REDIS_CONNECTIONS_0
	if REDIS_CONNECTIONS_0 is not None:
		return REDIS_CONNECTIONS_0
	try:
		REDIS_CONNECTIONS_0 = redis.Redis(
			unix_socket_path=config.Redis_Unix_Socket,
			db=0)
	except Exception, e:
		logger.error('An error occurred while getting the Redis connection instance: %s' % e)
		REDIS_CONNECTIONS_0 = None
	return REDIS_CONNECTIONS_0

def get_redis_1():
	global REDIS_CONNECTIONS_1
	if REDIS_CONNECTIONS_1 is not None:
		return REDIS_CONNECTIONS_1
	try:
		REDIS_CONNECTIONS_1 = redis.Redis(
			unix_socket_path=config.Redis_Unix_Socket,
			db=1)
	except Exception, e:
		logger.error('An error occurred while getting the Redis connection instance: %s' % e)
		REDIS_CONNECTIONS_1 = None
	return REDIS_CONNECTIONS_1

def get_redis_2():
	global REDIS_CONNECTIONS_2
	if REDIS_CONNECTIONS_2 is not None:
		return REDIS_CONNECTIONS_2
	try:
		REDIS_CONNECTIONS_2 = redis.Redis(
			unix_socket_path=config.Redis_Unix_Socket,
			db=2)
	except Exception, e:
		logger.error('An error occurred while getting the Redis connection instance: %s' % e)
		REDIS_CONNECTIONS_2 = None
	return REDIS_CONNECTIONS_2

def get_file_from_current_dir(_file_, filename):
	path = os.path.split(os.path.realpath(_file_))[0]
	return os.path.join(path, filename)

def pretty_print(jsonstr):
	if jsonstr is None or len(jsonstr) == 0:
		return jsonstr
	prettystr = '<html><body><pre><code>\r\n'
	try:
		obj = json.loads(jsonstr)
		prettystr += json.dumps(obj, indent=4, sort_keys=True)
	except Exception, e:
		logger.error('JSON parse failure (Pretty Print)')
		return jsonstr
	prettystr += '\r\n'
	prettystr += '</code></pre></body></html>'
	prettystr = prettystr.decode('unicode_escape')
	return prettystr

def strict_str(str_):
	str_ = str_.replace('"', '\\"')
	str_ = str_.strip()
	return str_

def request_log(method_text):
	def decorator(func):
		def wrapper(self, *args, **kwargs):
			if config.Mode == 'DEBUG':
				logger.debug(
				'Request URI: %s (%s)(%s)' % 
				(self.request.uri, self.request.remote_ip, method_text))
			return func(self, *args, **kwargs)
		return wrapper
	return decorator

class DateEncoder(json.JSONEncoder):
        def default(self, obj):
                if isinstance(obj, datetime):
                        return obj.__str__()
                elif isinstance(obj, decimal.Decimal):
                        return str(obj)
                else:
                        return json.JSONEncoder.default(self, obj)

def json_loads_body(func):
	def wrapper(self, *args, **kwargs):
		try:
			if self.request.body is None:
				pass;
			else:
				self.body_json_object = json.loads(self.request.body)
				print json.dumps(self.body_json_object, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
				#print json.dumps(self.body_json_object, sort_keys=True, cls=DateEncoder)
		except Exception, e:
			logger.error('JSON parse failure (Request Body)')
		return func(self, *args, **kwargs)
	return wrapper


