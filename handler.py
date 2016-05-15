#!/usr/bin/python

import sys, os, uuid
import json, time
import tornado.web
import tornado_mysql.pools
import redis
import logging
from datetime import datetime
import decimal

reload(sys)
sys.setdefaultencoding('utf8')

import common
import config

logger = logging.getLogger('web')

class DateEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.__str__()
    if isinstance(obj, decimal.Decimal):
            return str(obj)
    return json.JSONEncoder.default(self, obj)

class RequestHandler(tornado.web.RequestHandler):

	def write(self, trunk):
		if type(trunk) == int:
			trunk = str(trunk)
		super(RequestHandler, self).write(trunk)

	def gen_result(self, code, message, result):
		# TODO JWT
		res = '{ '
		res += '"code": %s, ' % code
		res += '"message": "%s"' % message
		if result is None or len(result) == 0:
			res += ' }'
			return res
		if not isinstance(result, basestring) and type(result) <> int:
			result = json.dumps(result, sort_keys=True, cls=DateEncoder)
			res += ',"result": %s' % result
			res += ' }'
		return res

	def exception_handle(self, code, message):
		# TODO missing code
		logger.error(message)
		self.write(self.gen_result(code, message, ''))
		return

	def session_set(self, uid):
		uu = str(uuid.uuid1())
		r = common.get_redis_1()
		if r is None:
			logger.error('Invalid Redis connection')
			return None
		try:
			r.set(uu, uid, ex=config.Cookie_ExpireTime)
			self.set_secure_cookie('session_id', uu)
		except Exception, e:
			logger.error('The database operation failed (Redis.Set set)')
			return None
		return uu

	def session_rm(self):
		uu = self.get_secure_cookie('session_id')
		if uu is None:
			return
		r = common.get_redis_1()
		if r is None:
			logger.error('Invalid Redis connection')
			return None
		try:
			r.delete(uu)
			self.set_secure_cookie('session_id', '')
		except Exception, e:
			logger.error('The database operation failed (Redis.Rm)')
			return None

	def session_get(self):
	#	return '111'
		uu = self.get_secure_cookie('session_id')
		if uu is None:
			return
		r = common.get_redis_1()
		if r is None:
			logger.error('Invalid Redis connection')
			return None
		try:
			return r.get(uu)
		except Exception, e:
			logger.error('The database operation failed (Redis.Get)')
			return None

	def get_cur_time(self):
		return time.strftime('%Y-%m-%d %X',time.localtime(time.time()))

