#!/usr/bin/python

import sys, os, threading, re, time
import tornado.web
import tornado.gen
import logging
import random
import hashlib, base64

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config
from handler import RequestHandler
from db_user import UserSQLHelper
from CCPRestSDK import REST
import ConfigParser

logger = logging.getLogger('web')

class AuthKeyHandler(RequestHandler):

	def sendsns(self,to,datas):
		accountSid = 'aaf98f8951858ab801518b3677e40ad5'
		accountToken = '5c3cdbdf6bf940c1b48b658070873219'
		appid = 'aaf98f8951e82e620151eb452b41046b'
		tempid = '58783'
		serverIP='sandboxapp.cloopen.com'
		serverPort='8883'
		softVersion='2013-12-26'
		rest = REST(serverIP,serverPort,softVersion)
		rest.setAccount(accountSid,accountToken)
		rest.setAppId(appid)
		result = rest.sendTemplateSMS(to,datas,tempid)
		return result

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		tel = self.body_json_object.get('tel')
		if tel is None or len(tel) == 0:
			self.exception_handle(config.tel_not_found, 'Missing argument \'tel\'')
			return
		if not re.match(r'^[1][0-9]{10}$', tel):
			self.exception_handle(config.tel_format_not_correct,'\'tel\' format is not correct')
			return
		user_type = self.body_json_object.get('type')
		if user_type is None:
			self.exception_handle(config.userid_or_password_wrong, 'Missing argument \'user type\'')
			return
		if int(user_type) == 0:
			user = yield UserSQLHelper.check_profile_by_tel(tel)
			if user == 1:
				self.exception_handle(config.user_exist,'tel is exit')
				return 
		code = random.randint(100000, 999999)
		logger.debug('Your auth code is %s' % code)

		# TODO Send SMS message
		ret = self.sendsns(tel,[code,'2'])
		logger.debug('ret: %s' % ret)
		#if not ret.has_key('statusCode') or cmp(ret['statusCode'],'000000') <> 0:
		#	self.exception_handle('auth SMS send failed')
		#	return
		r = common.get_redis_0()
		if r is None:
			self.exception_handle(config.connect_redis_failed, 'Invalid Redis connection')
			return
		try:
			r.set(tel, code, ex=config.AuthCode_ExpireTime) # Block ?
		except Exception, e:
			self.exception_handle(config.connect_redis_failed, 'The database operation failed (Redis.Set)AuthKeyHandler')
			return
		self.write(self.gen_result(0, 'key_success',{'key':code}))
		return

class CheckkeyHandler(RequestHandler):

	def check_key(self,key):
		if key is None or len(key) == 0:
			self.exception_handle(config.key_error,'Missing argument \'key\'')
			return False

		if len(key) <> 6:
			self.exception_handle(config.key_error,'Auth code format exception, %s' % key)
			return False

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		tel = self.body_json_object.get('tel')
		if tel is None or len(tel) == 0:
			self.exception_handle(config.tel_not_found, 'Missing argument \'tel\'')
			return
		if not re.match(r'^[1][0-9]{10}$', tel):
			self.exception_handle(config.tel_format_not_correct,'\'tel\' format is not correct')
			return
		key = self.body_json_object.get('key')
		if self.check_key(key) == False:
			return
		r = common.get_redis_0()
		if r is None:
			self.exception_handle(config.connect_redis_failed,'Invalid Redis connection')
			return
		xcode = None
		try:
			xcode = r.get(tel)
		except Exception, e:
			self.exception_handle(config.connect_redis_failed,'The database operation failed (Redis.Get)')
			return
		if xcode is None or xcode <> key:
			self.exception_handle(config.key_error,'The phone or pin you entered was incorrect. Please try again')
			return
		r.delete(tel)
		self.write(self.gen_result(0, 'key_is_right',self.body_json_object))
		return

class RegisterHandler(RequestHandler):

	def check_pwd(self,pwd):
		if pwd is None or len(pwd) == 0:
			self.exception_handle(config.userid_or_password_wrong, "Password is empty")
			return False
		if len(pwd) < 6:
			self.exception_handle(config.userid_or_password_wrong, "Password is short, must than 6 number")
			return False
		if len(re.findall('[0-9]',pwd)) > 0 and len(re.findall('[a-z]',pwd)) > 0:
			return True
		else:
			self.exception_handle(config.userid_or_password_wrong, "Password must has number and letter")
			return False
		return True

	def check_key(self,key):
		if key is None or len(key) == 0:
			self.exception_handle(config.key_error,'Missing argument \'key\'')
			return False

		if len(key) <> 6:
			self.exception_handle(config.key_error,'Auth code format exception, %s' % key)
			return False

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,'Request data format exception, %s' % self.request.uri)
			return
		userid = self.body_json_object.get('userid')
		if userid is None or len(userid) == 0:
			self.exception_handle(config.user_not_found,'Missing argument \'user accout\'')
			return
		userexit = yield UserSQLHelper.check_profile_by_uid(userid)
		if userexit  == 1:
			self.exception_handle(config.user_exist,'Userid is exit')
			return
		tel = self.body_json_object.get('tel')
		if tel is None or len(tel) == 0:
			self.exception_handle(config.tel_not_found,'Missing argument \'tel\'')
			return
		user = yield UserSQLHelper.check_profile_by_tel(tel)
		if user == 1:
			self.exception_handle(config.user_exist,'tel is exit')
			return 
		passwd = self.body_json_object.get('password')
		if passwd is None or len(passwd) == 0:
			self.exception_handle(config.userid_or_password_wrong,'Missing argument \'password\'')
			return
		# TODO Check password format
		if self.check_pwd(passwd) == False:
			return
		password_md5 = hashlib.md5(self.body_json_object['password']).hexdigest()
		print "password %s" % password_md5
		self.body_json_object['password'] = password_md5
		if not re.match(r'^[1][0-9]{10}$', tel):
			self.exception_handle(config.tel_format_not_correct,'\'tel\' format is not correct')
			return
		'''key = self.body_json_object.get('key')
		if self.check_key(key) == False:
			return
		r = common.get_redis_0()
		if r is None:
			self.exception_handle(config.connect_redis_failed,'Invalid Redis connection')
			return
		xcode = None
		try:
			xcode = r.get(tel)
		except Exception, e:
			self.exception_handle(config.connect_redis_failed,'The database operation failed (Redis.Get)')
			return
		if xcode is None or xcode <> key:
			self.exception_handle(config.key_error,'The phone or pin you entered was incorrect. Please try again')
			return
		r.delete(tel)'''
		self.body_json_object['updated_at'] = self.get_cur_time()
		id_ = yield UserSQLHelper.add_user(self.body_json_object)
		if id_ is None:
			self.exception_handle(config.execute_db_failed,'The database operation failed (MySQL.AddUser)')
			return
		self.body_json_object['userid'] = id_
		dt = self.body_json_object.get('updated_at')
		sdt = time.mktime(time.strptime(str(dt), '%Y-%m-%d %H:%M:%S'))
		self.body_json_object['updated_at'] = int(sdt)
		logger.debug(self.body_json_object)
		self.write(self.gen_result(0, 'register_success', self.body_json_object))
		return

class ForgetHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,'Request data format exception, %s' % self.request.uri)
			return
		tel = self.body_json_object.get('tel')
		if tel is None or len(tel) == 0:
			self.exception_handle(config.tel_not_found,'Missing argument \'tel\'')
			return
		if not re.match(r'^[1][0-9]{10}$', tel):
			self.exception_handle(config.tel_format_not_correct,'\'tel\' format is not correct')
			return
		request_password = self.body_json_object.get('password')
		if request_password is None or len(request_password) == 0:
			self.exception_handle(config.userid_or_password_wrong,'Missing argument \'password\'')
			return
		password_md5 = hashlib.md5(request_password).hexdigest()
		print "request_password %s" % password_md5
		request_password = password_md5
		code = self.body_json_object.get('key')
		if code is None or len(code) == 0:
			self.exception_handle(config.key_error,'Missing argument \'key\'')
			return
		if len(code) <> 6:
			self.exception_handle(config.key_error,'Auth code format exception, %s' % code)
			return
		r = common.get_redis_0()
		if r is None:
			self.exception_handle(config.connect_redis_failed,'Invalid Redis connection')
			return
		xcode = None
		try:
			xcode = r.get(tel)
		except Exception, e:
			self.exception_handle(config.connect_redis_failed,'The database operation failed (Redis.Get)')
			return
		if xcode is None or xcode <> code:
			self.exception_handle(config.key_error,'The phone or pin you entered was incorrect. Please try again')
			return
		updateusertime = self.body_json_object.get('updated_at')
		userid = user.get('userid',)
		try:
			yield UserSQLHelper.update_users_time(userid, updateusertime)
		except Exception, e:
			self.exception_handle(config.change_failed,'update users time failed (MySQL)')
		try:
			rc = yield UserSQLHelper.modify_password_by_tel(tel, request_password)
		except Exception, e:
			self.exception_handle(config.change_failed,'Password change failed (MySQL)')
		if rc is None:
			self.exception_handle(config.change_failed,'Password change failed (MySQL)')
			return
		if rc == 0:
			self.exception_handle(config.change_failed,'old password is the same as new password')
			return
		user = yield UserSQLHelper.fetch_profile(self.body_json_object['userid'])
		if user is None:
			self.exception_handle(config.execute_db_failed,'Get User failed (MySQL)')
			return
		del self.body_json_object['password']
		del self.body_json_object['key']
		self.body_json_object['nickname'] = user.get('nickname','hello')
		self.body_json_object['icon'] = user.get('icon','null')
		self.body_json_object['email'] = user.get('email','null')
		self.body_json_object['updated_at'] = self.get_cur_time()
		print self.body_json_object
		self.write(self.gen_result(0, 'Successfully changed', self.body_json_object))

class LoginHandler(RequestHandler):

	def is_phone_num(self,userid):
		if not re.match(r'^[1][0-9]{10}$',userid):
			return False
		return True

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,
				'Request data format exception, %s' % self.request.uri)
			return
		userid = self.body_json_object.get('userid')
		if userid is None or len(userid) == 0:
			self.exception_handle(config.user_not_found,'Missing argument \'user accout\'')
			return
		user = None
		if self.is_phone_num(userid):
			user = yield UserSQLHelper.fetch_profile_by_tel(userid)
		else:
			user = yield UserSQLHelper.fetch_profile_by_uid(userid)
		if user is None:
			self.exception_handle(config.user_not_found,'User not found')
			return

		request_password = self.body_json_object.get('password')
		if request_password is None or len(request_password) == 0:
			self.exception_handle(config.userid_or_password_wrong,'Missing argument \'password\'')
			return
		password_md5 = hashlib.md5(request_password).hexdigest()
		print "request_password %s" % password_md5
		request_password = password_md5
		password = user.get('password', '')
		if request_password <> password:
			self.exception_handle(config.userid_or_password_wrong,'Incorrect password')
			return
		self.body_json_object['nickname'] = user.get('nickname','hello')
		self.body_json_object['icon'] = user.get('icon','null')
		self.body_json_object['updated_at'] = self.get_cur_time();
		self.body_json_object['tel'] = user.get('tel','');
		updateusertime = self.body_json_object.get('updated_at')
		userid = user.get('userid',)
		if userid is None:
			self.exception_handle(config.user_not_found,'User not found')
			return
		try:
			yield UserSQLHelper.update_users_time(userid, updateusertime)
		except Exception, e:
			self.exception_handle(config.change_failed,'update users time failed (MySQL)')
		self.write(self.gen_result(0, 'login_success', self.body_json_object))

class LogoutHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,
				'Request data format exception, %s' % self.request.uri)
			return
		self.session_rm()
		self.write(self.gen_result(0, 'logout_success',None))

class UUpdateHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('GET')
	def get(self):
		id_ = None
		session_id_ = self.session_get()
		if self.request.arguments.has_key('id'):
			id_ = self.get_argument('id')
		if id_ is None or len(id_) == 0:
			id_ = session_id_
		if id_ is None or len(id_) == 0:
			self.exception_handle(config.user_not_found,'Missing argument \'id\'')
			return
		user = None
		if id_ <> session_id_:
			user = yield UserSQLHelper.fetch_base_profile(id_)
		else:
			user = yield UserSQLHelper.fetch_profile(id_)
		if user is None:
			self.exception_handle(config.user_not_found,'User not found')
			return
		self.write(self.gen_result(0, 'Account profile', user))
		return

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(config.user_not_found,
				'Session timeout')
			return
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,
				'Request data format exception, %s' % self.request.uri)
			return
		self.body_json_object['userid'] = uid
		self.body_json_object['updated_at'] = self.get_cur_time()
		rc = yield UserSQLHelper.update_profile(self.body_json_object)
		if rc is None:
			self.exception_handle(config.update_userinfo_failed,'The database operation failed (MySQL.UpdateProfile)')
			return
		if  rc == 0:
			self.exception_handle(config.update_userinfo_failed,'There is no info to update')
			return
		updateusertime = self.get_cur_time()
		try:
			yield UserSQLHelper.update_users_time(uid, updateusertime)
		except Exception, e:
			self.exception_handle(config.change_failed,'update users time failed (MySQL)')
		user = yield UserSQLHelper.fetch_profile(uid)
		if user is None:
			self.exception_handle(config.execute_db_failed,'Get User failed (MySQL.FecthProfile)')
			return
		logger.debug("posid: %s" % uid)
		pos = yield PosSQLHelper.get_pos(uid)
		defaultpos = {}
		if pos is None:
			defaultpos['lon'] = 0
			defaultpos['lat'] = 0
			defaultpos['time'] = self.get_cur_time()
		else:
			defaultpos = pos

		self.body_json_object['userid'] = uid
		self.body_json_object['nickname'] = user.get('nickname','hello')
		self.body_json_object['icon'] = user.get('icon','null')
		self.body_json_object['tel'] = user.get('tel')
		self.body_json_object['email'] = user.get('email','null')
		self.body_json_object['pos'] = pos;
		self.write(self.gen_result(0, 'update_success',self.body_json_object))

class ResetHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(config.user_not_found,
				'Session timeout')
			return
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,
				'Request data format exception, %s' % self.request.uri)
			return
		user = yield UserSQLHelper.fetch_profile_by_uid(uid)
		if user is None:
			self.exception_handle(config.user_not_found,'User not found')
			return

		old_password = self.body_json_object.get('old_password')
		if old_password is None or len(old_password) == 0:
			self.exception_handle(config.userid_or_password_wrong,'Missing argument \'old_password\'')
			return
		password_md5 = hashlib.md5(old_password).hexdigest()
		print "old_password %s" % password_md5
		old_password = password_md5
		password = user.get('password', '')
		logger.debug("old_password,password:%s,%s" % (old_password,password))
		if old_password <> password:
			self.exception_handle(config.userid_or_password_wrong,'Incorrect password')
			return
		new_password = self.body_json_object.get('new_password')
		if new_password is None or len(new_password) == 0:
			self.exception_handle(config.userid_or_password_wrong,'Missing argument \'new_password\'')
			return
		password_md5 = hashlib.md5(new_password).hexdigest()
		print "new_password %s" % password_md5
		new_password = password_md5
		if old_password == new_password:
			self.exception_handle(config.userid_or_password_wrong,'old password is the same as new password')
			return
		try:
			rc = yield UserSQLHelper.modify_password(uid, new_password)
		except Exception, e:
			self.exception_handle(config.reset_failed,'Password change failed (MySQL)')
			return
		if rc is None or rc == 0:
			self.exception_handle(config.reset_failed,'Record is 0, Password change failed (MySQL)')
			return
		updateusertime = self.get_cur_time()
		try:
			yield UserSQLHelper.update_users_time(uid, updateusertime)
		except Exception, e:
			self.exception_handle(config.change_failed,'update users time failed (MySQL)')
		user = yield UserSQLHelper.fetch_profile(uid);
		if user is None:
			self.exception_handle(config.execute_db_failed,'Get User failed (MySQL)')
			return
		self.session_rm()
		self.body_json_object['userid'] = user['userid']
		self.body_json_object['nickname'] = user['nickname']
		self.body_json_object['icon'] = user['icon']
		self.body_json_object['tel'] = user['tel']
		self.body_json_object['email'] = user['email']
		self.body_json_object['updated_at'] = user['updated_at']
		print self.body_json_object
		self.write(self.gen_result(0, 'modify_password_success', self.body_json_object))

class GetUserHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(config.user_not_found,'Session timeout')
			return
		user = yield UserSQLHelper.fetch_profile(uid)
		if user is None:
			self.exception_handle(config.user_not_exit,'Get User failed (MySQL.FecthProfile)')
			return
		pos = yield PosSQLHelper.get_pos(uid)
		defaultpos = {}
		if pos is None:
			defaultpos['lon'] = 0
			defaultpos['lat'] = 0
			defaultpos['time'] = self.get_cur_time()
		else:
			defaultpos = pos

		self.body_json_object['userid'] = uid
		self.body_json_object['nickname'] = user.get('nickname','hello')
		self.body_json_object['type'] = '0'
		self.body_json_object['icon'] = user.get('icon','null')
		self.body_json_object['tel'] = user.get('tel')
		self.body_json_object['email'] = user.get('email','null')
		self.body_json_object['updated_at'] = user.get('updated_at')
		self.body_json_object['pos'] = defaultpos
		self.write(self.gen_result(0, 'get_success',self.body_json_object))

class AvatarHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('GET')
	def get(self):
		id_ = None
		if self.request.arguments.has_key('id'):
			id_ = self.get_argument('id')
		if id_ is None or len(id_) == 0:
			self.exception_handle(config.user_not_found,'Missing argument \'id\'')
			return
		avatar = yield UserSQLHelper.fetch_avatar(id_)
		if avatar is None or len(avatar) == 0:
			self.exception_handle(config.execute_db_failed,'Specific avatar not found')
			return
		#try:
		#	avatar = base64.b64decode(avatar)
		#except Exception, e:
		#	self.exception_handle('Base64 decoding failure')
		#	return
		self.set_header('Content-Type', 'image/*')
		self.write(avatar)
		return


	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(config.user_not_found,
				'Session timeout')
			return
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,
				'Request data format exception, %s' % self.request.uri)
			return
		icon_name = self.body_json_object.get('icon')
		if icon_name is None or len(icon_name) == 0:
			self.exception_handle(config.icon_not_exit,'Specific icon name not found')
			return
		avatar = self.body_json_object.get('image64')
		if avatar is None or len(avatar) == 0:
			self.exception_handle(config.icon_not_exit,
				'Missing argument \'icon\'')
			return
		rc = yield UserSQLHelper.modify_user_avatar(uid, icon_name, avatar)
		if rc is None or rc == 0:
			self.exception_handle(config.update_icon_failed,'The database operation failed (MySQL.modify_user_avatar)')
			return
		#image64rc = yield UserSQLHelper.update_icon(uid, avatar)
		#if image64rc is None or image64rc == 0:
			#self.exception_handle('The database operation failed (MySQL.update_icon)')
			#return
		updateusertime = self.get_cur_time()
		try:
			yield UserSQLHelper.update_users_time(uid, updateusertime)
		except Exception, e:
			self.exception_handle(config.change_failed,'update users time failed (MySQL)')
		self.write(self.gen_result(0, 'update_icon_success',None))

class GetIconHandler(RequestHandler):
        @tornado.gen.coroutine
        @common.request_log('GET')
        def get(self):
		icon = None
		if self.request.arguments.has_key('icon'):
			icon = self.get_argument('icon')
                logger.debug('icon: %s' % icon)
		user = yield UserSQLHelper.fetch_userid_by_icon(icon)
		if user is None:
			self.exception_handle(config.user_not_found,'get user failed (MySQL.GetIconHandler)')
			return
                uid = user.get('userid','')
                logger.debug('uid: %s ' % uid);
                if uid is None or len(uid) == 0:
                        self.exception_handle(config.user_not_found,'Session timeout')
                        return

                try:
                        avatar = yield UserSQLHelper.fetch_avatar(uid)
                        if avatar is None or len(avatar) == 0:
                                self.exception_handle(config.icon_not_exit,'Specific avatar not found')
                                return
                except Exception as e:
                        self.exception_handle(config.icon_not_exit,'Specific avatar not found')
                        return
		avatart = base64.b64decode(str(avatar))
                self.set_header('Content-Type', 'image/*')
                self.write(avatar)
	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		uid = self.session_get()
		if uid is None or len(uid) == 0:
			self.exception_handle(config.user_not_found,'Session timeout')
			return
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error,'Request data format exception, %s' % self.request.uri)
			return
		avatar = yield UserSQLHelper.fetch_avatar(uid)
		if avatar is None or len(avatar) == 0:
			self.exception_handle(config.icon_not_exit,'Specific avatar not found')
			return
		#try:
			#avatar = base64.b64decode(avatar)
		#except Exception, e:
		#	self.exception_handle('Base64 decoding failure')
		#	return
		self.body_json_object['userid'] = uid
		self.body_json_object['image64'] = avatar
		self.body_json_object['updated_at'] = self.get_cur_time()

		self.write(self.gen_result(0, 'get_icon_success',self.body_json_object))

