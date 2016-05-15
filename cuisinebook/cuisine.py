#!/usr/bin/python

import sys, os, threading, re, uuid
import tornado.web
import tornado.gen
import logging
import random
import hashlib
import base64, json,time

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config
from handler import RequestHandler
from db_cuisine import CuisineBookSQLHelper
from db_cuisine import CuisineImageSQLHelper
from db_cuisine import ProductSQLHelper
from CCPRestSDK import REST
import ConfigParser

logger = logging.getLogger('cuisineweb')

class DateEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.__str__()
		elif isinstance(obj, decimal.Decimal):
			return str(obj)
		else:
			return json.JSONEncoder.default(self, obj)

class UpdateCuisineBookHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kBCookBookId = self.body_json_object.get('kBCookBookId')
		if kBCookBookId is None or len(kBCookBookId) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kBCookBookId\'')
			return
		#kBCookerId = self.body_json_object.get('kBCookerId')
		#if kBCookerId is None or len(kBCookerId) == 0:
		#	self.exception_handle(config.keyword_error, 'Missing argument \'kBCookerId\'')
		#	return
		#print 'kBCookerId:%s' % kBCookerId	
		kBDishName = self.body_json_object.get('kBDishName')
		if kBDishName is None or len(kBDishName) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kBDishName\'')
			return
		kBCookSteps = self.body_json_object.get('kBCookSteps')
		if kBCookSteps is None or len(kBCookSteps) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kBCookSteps\'')
			return
		self.body_json_object['kBCookSteps'] = json.dumps(kBCookSteps, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		
	#	if kBFoodMaterials is None or len(kBFoodMaterials) == 0:
	#		self.exception_handle(config.keyword_error, 'Missing argument \'kBFoodMaterials\'')
	#		return
		kBFoodMaterials = self.body_json_object.get('kBFoodMaterials')
		self.body_json_object['kBFoodMaterials'] = json.dumps(kBFoodMaterials, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		self.body_json_object['kBCreateTime'] = time.time()*1000
		#cur_ = yield CuisineBookSQLHelper.check_cuisinebook(kBCookBookId)
		#if cur_ <> 0:
		#	self.exception_handle(config.cuisine_exit,'kBCookBookId is exit')
		#	return
		id_ = yield CuisineBookSQLHelper.add_cuisinebook_all(self.body_json_object)
		if id_ is None:
			self.exception_handle(config.add_cuisine_failed,'The database operation failed (MySQL.Addcuisine)')
			return
		self.write(self.gen_result(0, 'add cuisine succeed',self.body_json_object))
		return
	

class GetCuisineBookHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		cuisineBookId = self.body_json_object.get('cuisineBookId')
		if cuisineBookId is None or len(cuisineBookId) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'cuisineBookId\'')
			return
		
		cuisinebook = yield CuisineBookSQLHelper.get_cuisinebook(cuisineBookId)
		if cuisinebook is None:
			self.exception_handle(config.get_cuisine_failed,'Get cuisine failed (MySQL.FecthProfile)')
			return

		self.body_json_object['kBCookBookId'] = cuisinebook.get('kBCookBookId')
		self.body_json_object['kBCookerId'] = cuisinebook.get('kBCookerId', '')
		self.body_json_object['kBDishName'] = cuisinebook.get('kBDishName', '')
		self.body_json_object['kBFavorNums'] = cuisinebook.get('kBFavorNums', '0')
		self.body_json_object['kBDescription'] = cuisinebook.get('kBDescription', '')
		self.body_json_object['kBTips'] = cuisinebook.get('kBTips', '')
		self.body_json_object['kBFoodMaterials'] = json.loads(cuisinebook.get('kBFoodMaterials', ''))
		self.body_json_object['kBIsPublish'] = int(cuisinebook.get('kBIsPublish', '0'))
		self.body_json_object['kBCreateTime'] = cuisinebook.get('kBCreateTime')
		self.body_json_object['kBKind'] = cuisinebook.get('kBKind', '')
		self.body_json_object['kBFollowMadeNums'] = cuisinebook.get('kBFollowMadeNums', '0')
		self.body_json_object['kBVisitNums'] = cuisinebook.get('kBVisitNums', '0')
		self.body_json_object['kBTopic'] = cuisinebook.get('kBTopic', '')
		self.body_json_object['kBSubKind'] = cuisinebook.get('kBSubKind', '')
		self.body_json_object['kBFrontCoverUrl'] = cuisinebook.get('kBFrontCoverUrl', '')
		self.body_json_object['kBStepNums'] = cuisinebook.get('kBStepNums', '0')
		self.body_json_object['kBVideoUrl'] = cuisinebook.get('kBVideoUrl', '')
		self.body_json_object['kBTags'] = cuisinebook.get('kBTags', '')
		self.body_json_object['kBTimeNeeded'] = cuisinebook.get('kBTimeNeeded', '')
		self.body_json_object['kBCookSteps'] = json.loads(cuisinebook.get('kBCookSteps', ''))
		self.body_json_object['kBNickName'] = cuisinebook.get('kBNickName', '')
		self.body_json_object['kBIconUrl'] = cuisinebook.get('kBIconUrl', '')
		
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return
	
class GetSomeCuisineBookHandler(RequestHandler):
	#get top cuisineBookNum record
	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kBCuisineBookNum = self.body_json_object.get('Num')
		if kBCuisineBookNum is None or kBCuisineBookNum < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'Num\'')
			return
		kBoffset = self.body_json_object.get('Offset')
		if kBoffset is None or kBoffset < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'Offset\'')
			return	
		cuisinebook = {}
		kBCookerId = self.body_json_object.get('CookerId')
		if kBCookerId is None:
			print 'cookerid none'
			cuisinebook = yield CuisineBookSQLHelper.get_somecuisinebook(kBoffset, kBCuisineBookNum)
		else:
			print 'cookerid yes'
			cuisinebook = yield CuisineBookSQLHelper.get_somecuisinebook_by_cookerid(kBCookerId, kBoffset, kBCuisineBookNum)
		
		if cuisinebook is None:
			self.exception_handle(config.get_cuisine_failed,'Get cuisine failed (MySQL.FecthProfile)')
			return
		self.body_json_object['cuisinebooks'] = [];
		del self.body_json_object['Offset']
		del self.body_json_object['Num']

		for cuisine in cuisinebook:
			#cuisine['kBCreateTime'] = int(time.mktime(time.strptime(str(cuisine['kBCreateTime']), '%Y-%m-%d %H:%M:%S')))
			if cuisine['kBFoodMaterials'] is not None:
				cuisine_ = cuisine['kBFoodMaterials']
				cuisine['kBFoodMaterials'] = json.loads(cuisine_)
			if cuisine['kBCookSteps'] is not None:
				cuisine_ = cuisine['kBCookSteps']
				cuisine['kBCookSteps'] = json.loads(cuisine_)
			self.body_json_object['cuisinebooks'].append(cuisine)
		
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return
	
class GetSomeCuisineBookByTimeHandler(RequestHandler):
	#get top cuisineBookNum record
	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kBCuisineBookNum = self.body_json_object.get('Num')
		if kBCuisineBookNum is None or kBCuisineBookNum < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'Num\'')
			return
		kBCreateTime = self.body_json_object.get('LimitTime')
		if kBCreateTime is None or kBCreateTime < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'LimitTime\'')
			return	
		cuisinebook = {}
		kBCookerId = self.body_json_object.get('CookerId')
		if kBCookerId is None:
			print 'no cookerid'
			cuisinebook = yield CuisineBookSQLHelper.get_somecuisinebook_by_time(kBCreateTime, kBCuisineBookNum)
		else:
			print 'have cookerid'
			cuisinebook = yield CuisineBookSQLHelper.get_somecuisinebook_by_cookerid_time(kBCookerId, kBCreateTime, kBCuisineBookNum)
		
		if cuisinebook is None:
			self.exception_handle(config.get_cuisine_failed,'Get cuisine failed (MySQL.FecthProfile)')
			return
		self.body_json_object['cuisinebooks'] = [];
		del self.body_json_object['LimitTime']
		del self.body_json_object['Num']

		for cuisine in cuisinebook:
			#cuisine['kBCreateTime'] = int(time.mktime(time.strptime(str(cuisine['kBCreateTime']), '%Y-%m-%d %H:%M:%S')))
			if cuisine['kBFoodMaterials'] is not None:
				cuisine_ = cuisine['kBFoodMaterials']
				cuisine['kBFoodMaterials'] = json.loads(cuisine_)
			if cuisine['kBCookSteps'] is not None:
				cuisine_ = cuisine['kBCookSteps']
				cuisine['kBCookSteps'] = json.loads(cuisine_)
			self.body_json_object['cuisinebooks'].append(cuisine)
		
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return
	
class UpdateProductHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kPProuctId = self.body_json_object.get('kPProuctId')
		if kPProuctId is None or len(kPProuctId) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kPProuctId\'')
			return
		#kPCookerId = self.body_json_object.get('kPCookerId')
		#if kPCookerId is None or len(kPCookerId) == 0:
		#	self.exception_handle(config.keyword_error, 'Missing argument \'kPCookerId\'')
		#	return
		#print 'kPCookerId:%s' % kPCookerId	
		kPDishName = self.body_json_object.get('kPDishName')
		if kPDishName is None or len(kPDishName) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kPDishName\'')
			return
		kPPhotos = self.body_json_object.get('kPPhotos')
		if kPPhotos is None or len(kPPhotos) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kPPhotos\'')
			return
		self.body_json_object['kPPhotos'] = json.dumps(kPPhotos, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		
		self.body_json_object['kPCreateTime'] = time.time()*1000
		#cur_ = yield ProductSQLHelper.check_product(kPProuctId)
		#if cur_ <> 0:
		#	self.exception_handle(config.product_exit,'kPProuctId is exit')
		#	return
		id_ = yield ProductSQLHelper.add_product(self.body_json_object)
		if id_ is None:
			self.exception_handle(config.add_product_failed,'The database operation failed (MySQL.Addcuisine)')
			return
		self.write(self.gen_result(0, 'add product succeed',self.body_json_object))
		return
	

class GetProductHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kPProuctId = self.body_json_object.get('kPProuctId')
		if kPProuctId is None or len(kPProuctId) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'kPProuctId\'')
			return
		
		product = yield ProductSQLHelper.get_product(kPProuctId)
		if product is None:
			self.exception_handle(config.get_product_failed,'Get product failed (MySQL.FecthProfile)')
			return

		self.body_json_object['kPCookerId'] = product.get('kPCookerId', '')
		self.body_json_object['kPDishName'] = product.get('kPDishName', '')
		self.body_json_object['kPFollowBookId'] = product.get('kPFollowBookId','')
		self.body_json_object['kPPhotoNums'] = product.get('kPPhotoNums', '0')
		self.body_json_object['kPFrontCoverUrl'] = product.get('kPFrontCoverUrl', '')
		self.body_json_object['kPTopic'] = product.get('kPTopic', '')
		self.body_json_object['kPDescription'] = product.get('kPDescription', '')
		self.body_json_object['kPKind'] = product.get('kPKind', '')
		self.body_json_object['kPSubKind'] = product.get('kPSubKind', '')
		self.body_json_object['kPIsPublished'] = product.get('kPIsPublished', '0')
		self.body_json_object['kPTags'] = product.get('kPTags', '')
		self.body_json_object['kPTips'] = product.get('kPTips', '')
		self.body_json_object['kPCreateTime'] = product.get('kPCreateTime', '')
		self.body_json_object['kPScore'] = product.get('kPScore', '')
		self.body_json_object['kPPhotos'] = json.loads(product.get('kPPhotos', ''))
		self.body_json_object['kPNickName'] = product.get('kPNickName', '')
		self.body_json_object['kPIconUrl'] = product.get('kPIconUrl', '')
		
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return
	
class GetSomeProductHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kPProuctNum = self.body_json_object.get('Num')
		if kPProuctNum is None or kPProuctNum < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'Num\'')
			return
		kPoffset = self.body_json_object.get('Offset')
		if kPoffset is None or kPoffset < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'Offset\'')
			return
		kPCookerId = self.body_json_object.get('CookerId')
		if kPCookerId is None:
			products = yield ProductSQLHelper.get_someproduct(kPoffset, kPProuctNum)
		else:
			products = yield ProductSQLHelper.get_someproduct_by_cookerid(kPCookerId, kPoffset, kPProuctNum)
		if products is None:
			self.exception_handle(config.get_product_failed,'Get products failed (MySQL.FecthProfile)')
			return
		del self.body_json_object['Offset']
		del self.body_json_object['Num']
		self.body_json_object['products'] = []
		for product in products:
			#product['kPCreateTime'] = int(time.mktime(time.strptime(str(product['kPCreateTime']), '%Y-%m-%d %H:%M:%S')))
			if product is not None:
				product['kPPhotos'] = json.loads(product['kPPhotos'])
			self.body_json_object['products'].append(product)
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return

class GetSomeProductByTimeHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		kPProuctNum = self.body_json_object.get('Num')
		if kPProuctNum is None or kPProuctNum < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'Num\'')
			return
		kPCreateTime = self.body_json_object.get('LimitTime')
		if kPCreateTime is None or kPCreateTime < 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'LimitTime\'')
			return
		kPCookerId = self.body_json_object.get('CookerId')
		if kPCookerId is None:
			products = yield ProductSQLHelper.get_someproduct_by_time(kPCreateTime, kPProuctNum)
		else:
			products = yield ProductSQLHelper.get_someproduct_by_cookerid_time(kPCookerId, kPCreateTime, kPProuctNum)
		if products is None:
			self.exception_handle(config.get_product_failed,'Get products failed (MySQL.FecthProfile)')
			return
		del self.body_json_object['LimitTime']
		del self.body_json_object['Num']
		self.body_json_object['products'] = []
		for product in products:
			#product['kPCreateTime'] = int(time.mktime(time.strptime(str(product['kPCreateTime']), '%Y-%m-%d %H:%M:%S')))
			if product is not None:
				product['kPPhotos'] = json.loads(product['kPPhotos'])
			self.body_json_object['products'].append(product)
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return

class UpdateCuisineImageHandler(RequestHandler):

	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		imagemd5 = self.body_json_object.get('imagemd5')
		if imagemd5 is None or len(imagemd5) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'imagemd5\'')
			return
		image_ = yield CuisineImageSQLHelper.check_cuisineimage(imagemd5)
		if image_ <> 0:
			self.write(self.gen_result(-28, 'image64 exit', self.body_json_object))
			return
		image64 = self.body_json_object.get('image64')
		if image64 is None or len(image64) == 0:
			self.write(self.gen_result(-29, 'Missing argument \'image64\'', self.body_json_object))
			return
		id_ = yield CuisineImageSQLHelper.add_cuisineimage(self.body_json_object)
		if id_ is None:
			self.exception_handle(config.add_image_failed,'The database operation failed (MySQL.Addcuisineimage)')
			return
		del self.body_json_object['image64']
		#imagemd5str = config.Hostip+"/api/user/getimage?imagemd5="+self.body_json_object.get('imagemd5')
		#self.body_json_object['imagemd5'] = imagemd5str
		self.write(self.gen_result(0, 'get cuisine succeed',self.body_json_object))
		return
	

class GetCuisineImageHandler(RequestHandler):
	
	@tornado.gen.coroutine
	@common.request_log('GET')
	def get(self):
		imagemd5 = None
		if self.request.arguments.has_key('imagemd5'):
			imagemd5 = self.get_argument('imagemd5')
			logger.debug('imagemd5: %s' % imagemd5)
		try:
			image = yield CuisineImageSQLHelper.get_cuisineimage(imagemd5)
			if image is None or len(image) == 0:
				self.exception_handle(config.get_image_failed,'Specific image not found')
				return
		except Exception as e:
			self.exception_handle(config.get_image_failed,'Specific image not found')
			return
		avatar = image.get('image64')
		avatart = base64.b64decode(str(avatar))
		self.set_header('Content-Type', 'image')
		#self.write("<img src='data:image/*;base64,"+avatar+"' alt='Red dot' />")
		self.write(avatart)
		
	@tornado.gen.coroutine
	@common.request_log('POST')
	@common.json_loads_body
	def post(self):
		if self.body_json_object is None:
			self.exception_handle(config.json_parameter_error, 
				'Request data format exception, %s' % self.request.uri)
			return
		cuisineBookId = self.body_json_object.get('cuisineBookId')
		if cuisineBookId is None or len(cuisineBookId) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'cuisineBookId\'')
			return
		iconname = self.body_json_object.get('iconname')
		if iconname is None or len(iconname) == 0:
			self.exception_handle(config.keyword_error, 'Missing argument \'iconname\'')
			return		
		cuisine = yield CuisineImageSQLHelper.get_cuisineimage(cuisineBookId, iconname)
		if cuisine is None:
			self.exception_handle(config.get_image_failed,'Get cuisine failed (MySQL.FecthProfile)')
			return

		self.body_json_object['iconid'] = cuisine.get('iconid','')
		self.body_json_object['cuisineBookId'] = cuisineBookId
		self.body_json_object['iconname'] = cuisine.get('iconname','')
		self.body_json_object['image64'] = cuisine.get('image64','')
		self.write(self.gen_result(0, 'get_success',self.body_json_object))
		return
