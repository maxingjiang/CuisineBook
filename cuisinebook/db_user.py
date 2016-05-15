#!/usr/bin/python

import sys, os, uuid
import logging
import tornado.gen

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config
import pdb
logger = logging.getLogger('web')

class UserSQLHelper:

	@classmethod
	@tornado.gen.coroutine
	def add_user(cls, user):
		id_ = user.get('userid', str(uuid.uuid1()))
		password_ = user.get('password')
		if password_ is None or len(password_) == 0:
			logger.error('Missing field \'password\'')
			raise tornado.gen.Return(None)
		name_ = user.get('nickname', '')
		tel_ = user.get('tel', '')
		updatedat_ = user.get('updated_at', '')
		sql_statement = ('INSERT INTO `users` '
				'(`userid`, `password`, `nickname`, `tel`,  `created_at`, `updated_at`)'
				' VALUES '
				'(%s, %s, %s, %s, %s, %s)')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		try:
			yield pool.execute(sql_statement, (id_ , password_, name_, tel_, updatedat_, updatedat_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(id_)

	@classmethod
	@tornado.gen.coroutine
	def update_users_time(cls, id_, updatetime):
		sql_statement = ('UPDATE `users` SET `updated_at` = %s WHERE `userid` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (updatetime, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)

	@classmethod
	@tornado.gen.coroutine
	def modify_password(cls, id_, new_password):
		sql_statement = ('UPDATE `users` SET `password` = %s WHERE `userid` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (new_password, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)
	
	@classmethod
	@tornado.gen.coroutine
	def modify_password_by_tel(cls, tel, new_password):
		sql_statement = ('UPDATE `users` SET `password` = %s WHERE `tel` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (new_password, tel))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)


	@classmethod
	@tornado.gen.coroutine
	def update_profile(cls, profile):# TODO Avatar
		id_ = profile.get('userid')
		sql_statement = 'SELECT * FROM `users` WHERE `userid` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = yield pool.execute(sql_statement, (id_,))
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		raw_user = cur.fetchone()
		name_ = profile.get('nickname', raw_user.get('nickname'))
		tel_ = profile.get('tel', raw_user.get('tel'))
		email_ = profile.get('email', raw_user.get('email'))
		deviceid_ = profile.get('deviceid', raw_user.get('deviceid'))
		updatetime_ = profile.get('updated_at', raw_user.get('updated_at'))
		sql_statement = ('UPDATE `users` SET '
				'`nickname` = %s, '
				'`tel` = %s, '
				'`email` = %s, '
				'`deviceid` = %s, '
				'`updated_at` = %s'
				' WHERE '
				'`userid` = %s')
		cur = None
		try:
			cur = yield pool.execute(sql_statement,(name_, tel_, email_, deviceid_, updatetime_, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)

	@classmethod
	@tornado.gen.coroutine
	def fetch_profile(cls, id_):
		sql_statement = 'SELECT * FROM `users` WHERE `userid` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def fetch_profile_by_name(cls, name):
		sql_statement = 'SELECT * FROM `users` WHERE `nickname` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (name))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def fetch_avatar(cls, id_):
		sql_statement = 'SELECT `image64` FROM `icon` WHERE `userid` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None or cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		if profile is None:
			logger.error('Specific row not found')
			raise tornado.gen.Return(None)
		avatar = profile.get('image64')
		raise tornado.gen.Return(avatar)
		
	@classmethod
	@tornado.gen.coroutine
	def modify_user_avatar(cls, id_, icon_name, avatar_base64string):
		sql_statement = ('UPDATE `users` SET `icon` = %s WHERE `userid` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		travl = yield pool.begin()
		if travl is None:
			logger.error('Unknown connection travl')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield travl.execute(sql_statement, (icon_name, id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		icon_sql_statement = ('REPLACE INTO `icon` (`userid`, `icon`, `image64`) VALUES (%s,%s,%s);')
		icon_cur = None
		try:
			icon_cur = yield travl.execute(icon_sql_statement, (id_,icon_name, avatar_base64string))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if icon_cur is None:
			raise tornado.gen.Return(None)		
		travl.commit()
		raise tornado.gen.Return(cur.rowcount)

	@classmethod
	@tornado.gen.coroutine
	def update_icon(cls, id_, avatar_base64string):
		sql_statement = ('REPLACE INTO `icon` (`userid`, `image64`) VALUES (%s,%s);')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_, avatar_base64string))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)


	@classmethod
	@tornado.gen.coroutine
	def fetch_base_profile(cls, id_):
		sql_statement = ('SELECT `userid`, `nickname`, `icon`, `email` FROM `users` WHERE `id` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (id_))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None or cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def fetch_profile_by_tel(cls, tel):
		sql_statement = 'SELECT * FROM `users` WHERE `tel` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (tel,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None or cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def fetch_profile_by_uid(cls, uid):
		sql_statement = 'SELECT * FROM `users` WHERE `userid` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (uid,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None or cur.rowcount == 0:
			logger.error('User not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)

	@classmethod
	@tornado.gen.coroutine
	def check_profile_by_tel(cls, tel):
		sql_statement = 'SELECT * FROM `users` WHERE `tel` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (tel,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None or cur.rowcount == 0:
			raise tornado.gen.Return(0)
		else:
			raise tornado.gen.Return(1)

	@classmethod
	@tornado.gen.coroutine
	def check_profile_by_uid(cls, uid):
		sql_statement = 'SELECT * FROM `users` WHERE `userid` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (uid,))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None or cur.rowcount == 0:
			raise tornado.gen.Return(0)
		else:
			raise tornado.gen.Return(1)

	@classmethod
	@tornado.gen.coroutine
	def fetch_userid_by_icon(cls, icon):
		sql_statement = 'SELECT userid FROM `users` WHERE `icon` = %s'
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (icon))
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('icon not found')
			raise tornado.gen.Return(None)
		profile = cur.fetchone()
		raise tornado.gen.Return(profile)
