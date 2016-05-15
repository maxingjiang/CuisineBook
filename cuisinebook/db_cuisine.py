#!/usr/bin/python

import sys, os, uuid
import logging
import tornado.gen
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('..')
import common
import config
logger = logging.getLogger('cuisineweb')

class CuisineBookSQLHelper:

        def add_cuisinebook_console(self,cuisinebook,cuisineUrl):
		cuisineBookId = str(uuid.uuid1())
                dishName = cuisinebook.get('dishname')
                needTime = cuisinebook.get('needtime')
                difficulty = cuisinebook.get('difficulty')
                stepsNum = cuisinebook.get('stepsnum')
                tips = cuisinebook.get('tipsteps')
                CookStep = cuisinebook.get('cookstep')
                FoodMaterial = cuisinebook.get('foodmaterial')
                ImageSteps = cuisinebook.get('imagesteps')

                sql_statement = ('insert INTO `CuisineBook` '
                                '(`cuisineBookId`, `cuisineUrl`, `dishName`, `needTime`, `difficulty`, `stepsNum`, `tips`, `CookStep`, `FoodMaterial`, `ImageSteps`)'
                                ' VALUES '
                                '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
		
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisine_crawl',port=3306)
		if conn is None:
			print('Unknown connection conn')
			return None
		cur=conn.cursor()
		if cur is None:
			print('Unknown connection cur')
			return None
		conn.set_character_set('utf8')
		cur.execute('SET NAMES utf8;')
		cur.execute('SET CHARACTER SET utf8;')
		cur.execute('SET character_set_connection=utf8;')
		try:
			rc = cur.execute(sql_statement, (cuisineBookId, cuisineUrl, dishName, needTime, difficulty, stepsNum, tips,  CookStep, FoodMaterial, ImageSteps))
			conn.commit()
			cur.close()
			conn.close()
			if rc is None or rc <> 1:
				print('insert cuisine error')
				return None
			else:
				return cuisineBookId
		except Exception, e:
			print(e)
			return None
	
    
	def get_cuisinebook_from_paser(self, kBCookBookId):

        	sql_statement = ("SELECT * from `CuisineBook` WHERE `cuisineBookId` = '%s'" % kBCookBookId)
        
       		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisine_crawl',port=3306)
        	if conn is None:
            		print('Unknown connection conn')
            		return None
        	cur=conn.cursor()
        	if cur is None:
            		print('Unknown connection cur')
            		return None
        	conn.set_character_set('utf8')
        	cur.execute('SET NAMES utf8;')
        	cur.execute('SET CHARACTER SET utf8;')
        	cur.execute('SET character_set_connection=utf8;')
        	try:
            		rc = cur.execute(sql_statement)
            		conn.commit()
            		data = cur.fetchone()
            		cur.close()
            		conn.close()
            		if data is None or len(data) == 0:
                		print('get cuisine empty')
                		return None
            		else:
                		return data
        	except Exception, e:
            		print(e)
            		return None

        def get_kBCookId_from_paser(self, cuisineUrl):

                sql_statement = ("select cuisineBookId from CuisineBook where cuisineUrl like '%s'" % cuisineUrl)

                conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisine_crawl',port=3306)
                if conn is None:
                        print('Unknown connection conn')
                        return None
                cur=conn.cursor()
                if cur is None:
                        print('Unknown connection cur')
                        return None
                conn.set_character_set('utf8')
                cur.execute('SET NAMES utf8;')
                cur.execute('SET CHARACTER SET utf8;')
                cur.execute('SET character_set_connection=utf8;')
                try:
                        rc = cur.execute(sql_statement)
                        conn.commit()
                        data = cur.fetchone()
                        cur.close()
                        conn.close()
                        if data is None or len(data) == 0:
                                print('get cuisineid empty')
                                return None
                        else:
                                return data
                except Exception, e:
                        print(e)
                        return None
 
    	def add_cuisinebook_paser_to_cuisinebook(self,cuisinebook):
                kBCookBookId = str(uuid.uuid1())
		kBCookerId = ''
                kBDishName = cuisinebook.get('kBDishName')
                kBTimeNeeded = cuisinebook.get('kBTimeNeeded')
                kBStepNums = cuisinebook.get('kBStepNums')
                kBTips = cuisinebook.get('kBTips')
                kBCookSteps = cuisinebook.get('kBCookSteps')
                kBFoodMaterials = cuisinebook.get('kBFoodMaterials')
		kBFrontCoverUrl = cuisinebook.get('kBFrontCoverUrl')
                kBCreateTime = cuisinebook.get('kBCreateTime')

                sql_statement = ('insert INTO `kBCookBook` '
                                '(`kBCookBookId`, `kBCookerId`, `kBDishName`, `kBTimeNeeded`, `kBStepNums`, `kBTips`, `kBCookSteps`, `kBFoodMaterials`, `kBFrontCoverUrl`, `kBCreateTime`)'
                                ' VALUES '
                                '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        
        	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisinebook',port=3306)
        	if conn is None:
            		print('Unknown connection conn')
            		return None
        	cur=conn.cursor()
        	if cur is None:
            		print('Unknown connection cur')
            		return None
        	conn.set_character_set('utf8')
        	cur.execute('SET NAMES utf8;')
        	cur.execute('SET CHARACTER SET utf8;')
        	cur.execute('SET character_set_connection=utf8;')
        	try:
            		rc = cur.execute(sql_statement, (kBCookBookId, kBCookerId, kBDishName, kBTimeNeeded, kBStepNums, kBTips,  kBCookSteps, kBFoodMaterials, kBFrontCoverUrl, kBCreateTime))
            		conn.commit()
            		cur.close()
            		conn.close()
            		if rc is None or rc <> 1:
                		print('insert cuisine error')
                		return None
            		else:
                		return kBCookBookId
        	except Exception, e:
            		print(e)
            		return None
        
    
	@classmethod
	@tornado.gen.coroutine
	def add_cuisinebook(self,cuisinebook):
		cuisineBookId = cuisinebook.get('cuisineBookId')
		dishName = cuisinebook.get('dishname')
		needTime = cuisinebook.get('needtime')
		difficulty = cuisinebook.get('difficulty')
		stepsNum = cuisinebook.get('stepnum')
		#stepsNum = 3
		logger.info(dishName)
		tips = cuisinebook.get('TipsSteps')
		CookStep = cuisinebook.get('FoodSteps')
		FoodMaterial = cuisinebook.get('FoodMaterial')
		
		sql_statement = ('REPLACE INTO `CuisineBook` '
				'(`cuisineBookId`, `dishName`, `needTime`, `difficulty`, `stepsNum`, `tips`, `CookStep`, `FoodMaterial`)'
				' VALUES '
				'(%s, %s, %s, %s, %s, %s, %s, %s)')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		try:
			yield pool.execute(sql_statement, (cuisineBookId , dishName, needTime, difficulty, stepsNum, tips,  CookStep, FoodMaterial))	
			raise tornado.gen.Return(cuisineBookId)
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		
	@classmethod
	@tornado.gen.coroutine
	def add_cuisinebook_all(self,cuisinebook):
		kBCookBookId = cuisinebook.get('kBCookBookId', str(uuid.uuid1()))
		kBCookerId = cuisinebook.get('kBCookerId', '')
		kBDishName = cuisinebook.get('kBDishName', '')
		kBFavorNums = cuisinebook.get('kBFavorNums', 0)
		kBDescription = cuisinebook.get('kBDescription', '')
		kBTips = cuisinebook.get('kBTips', '')
		kBFoodMaterials = cuisinebook.get('kBFoodMaterials', '')
		kBIsPublish = cuisinebook.get('kBIsPublish', False)
		kBCreateTime = cuisinebook.get('kBCreateTime', '0')
		kBKind = cuisinebook.get('kBKind', '')
		kBFollowMadeNums = cuisinebook.get('kBFollowMadeNums', '')
		kBVisitNums = cuisinebook.get('kBVisitNums', '')
		kBTopic = cuisinebook.get('kBTopic', '')
		kBSubKind = cuisinebook.get('kBSubKind', '')
		kBFrontCoverUrl = cuisinebook.get('kBFrontCoverUrl', '')
		kBStepNums = cuisinebook.get('kBStepNums', '')
		kBVideoUrl = cuisinebook.get('kBVideoUrl', '')
		kBTags = cuisinebook.get('kBTags', '')
		logger.info(kBDishName)
		kBTimeNeeded = cuisinebook.get('kBTimeNeeded', '')
		kBCookSteps = cuisinebook.get('kBCookSteps', '')
		kBNickName = cuisinebook.get('kBNickName', '')
		kBIconUrl = cuisinebook.get('kBIconUrl', '')
        
		sql_statement = ('REPLACE INTO `kBCookBook` '
                '(`kBCookBookId`, `kBCookerId`, `kBDishName`, `kBFavorNums`, `kBDescription`, `kBTips`, `kBFoodMaterials`,'
                '`kBIsPublish`, `kBKind`, `kBFollowMadeNums`, `kBVisitNums`, `kBTopic`, `kBSubKind`, '
                '`kBFrontCoverUrl`, `kBStepNums`, `kBVideoUrl`, `kBTags`, `kBTimeNeeded`, `kBCookSteps`, `kBNickName`, `kBIconUrl`, `kBCreateTime`)'
                ' VALUES '
                '(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		try:
			cur = yield pool.execute(sql_statement, (kBCookBookId, kBCookerId, kBDishName, kBFavorNums, kBDescription, kBTips, kBFoodMaterials, 
                                               kBIsPublish, kBKind, kBFollowMadeNums, kBVisitNums, kBTopic, kBSubKind, 
                                               kBFrontCoverUrl, kBStepNums, kBVideoUrl, kBTags, kBTimeNeeded, kBCookSteps, kBNickName, kBIconUrl, kBCreateTime))    
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(kBCookBookId)

	@classmethod
	@tornado.gen.coroutine
	def get_cuisinebook(self,cuisineBookId):
		sql_statement = ('SELECT * from `kBCookBook` WHERE `kBCookBookId` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (cuisineBookId))
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('cuisine not found')
		cuisine = cur.fetchone()
		raise tornado.gen.Return(cuisine)

	@classmethod
	@tornado.gen.coroutine
	def get_somecuisinebook(self, kBoffset, cuisineBookNum):
		sql_statement = ('SELECT * from `kBCookBook` ORDER BY kBCreateTime DESC LIMIT %d,%d' % (kBoffset, cuisineBookNum))
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement)
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('cuisine not found')
		cuisine = cur.fetchall()
		raise tornado.gen.Return(cuisine)

        @classmethod
        @tornado.gen.coroutine
        def get_somecuisinebook_by_cookerid(self, kBCookerId, kBoffset, cuisineBookNum):
                sql_statement = ("SELECT * from `kBCookBook` where `kBCookerId` = '%s' ORDER BY kBCreateTime DESC LIMIT %d,%d" % (kBCookerId, kBoffset, cuisineBookNum))
                pool = common.get_mysql_pool()
		print 'find by cookerid'
                if pool is None:
                        logger.error('Unknown connection pool')
                cur = None
                try:
                        cur = yield pool.execute(sql_statement)
                except Exception, e:
                        logger.error(e)
                if cur is None:
                        raise tornado.gen.Return(None)
                if cur.rowcount == 0:
                        logger.error('cuisine not found')
                cuisine = cur.fetchall()
                raise tornado.gen.Return(cuisine)

	@classmethod
	@tornado.gen.coroutine
	def get_somecuisinebook_by_time(self, kBCreateTime, cuisineBookNum):
        	sql_statement = ('SELECT * from `kBCookBook` where `kBCreateTime` < %d ORDER BY kBCreateTime DESC LIMIT %d' % (kBCreateTime, cuisineBookNum))
        	pool = common.get_mysql_pool()
        	if pool is None:
            		logger.error('Unknown connection pool')
        	cur = None
        	try:
            		cur = yield pool.execute(sql_statement)
        	except Exception, e:
            		logger.error(e)
        	if cur is None:
            		raise tornado.gen.Return(None)
        	if cur.rowcount == 0:
            		logger.error('cuisine not found')
        	cuisine = cur.fetchall()
        	raise tornado.gen.Return(cuisine)

	@classmethod
	@tornado.gen.coroutine
    	def get_somecuisinebook_by_cookerid_time(self, kBCookerId, kBCreateTime, cuisineBookNum):
                sql_statement = ("SELECT * from `kBCookBook` where `kBCookerId` = '%s' and  `kBCreateTime` < %d ORDER BY kBCreateTime DESC LIMIT %d" 
		% (kBCookerId, kBCreateTime, cuisineBookNum))
                pool = common.get_mysql_pool()
                if pool is None:
                        logger.error('Unknown connection pool')
                cur = None
                try:
                        cur = yield pool.execute(sql_statement)
                except Exception, e:
                        logger.error(e)
                if cur is None:
                        raise tornado.gen.Return(None)
                if cur.rowcount == 0:
                        logger.error('cuisine not found')
                cuisine = cur.fetchall()
                raise tornado.gen.Return(cuisine)

	@classmethod
	@tornado.gen.coroutine
	def check_cuisinebook(self,cuisineBookId):
		sql_statement = ('SELECT * from `kBCookBook` WHERE `kBCookBookId` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (cuisineBookId))
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)
	
class ProductSQLHelper:

	@classmethod
	@tornado.gen.coroutine
	def add_product(self,product):
		kPProuctId = product.get('kPProuctId', str(uuid.uuid1()))
		kPCookerId = product.get('kPCookerId', '')
		kPDishName = product.get('kPDishName', '')
		kPFollowBookId = product.get('kPFollowBookId','')
		kPPhotoNums = product.get('kPPhotoNums', '')
		kPFrontCoverUrl = product.get('kPFrontCoverUrl', '')
		kPTopic = product.get('kPTopic', '')
		kPDescription = product.get('kPDescription', '')
		kPKind = product.get('kPKind', '')
		kPSubKind = product.get('kPSubKind', '')
		kPIsPublished = product.get('kPIsPublished', '0')
		kPTags = product.get('kPTags', '')
		kPTips = product.get('kPTips', '')
		kPCreateTime = product.get('kPCreateTime', '0')
		kPScore = product.get('kPScore', '')
		kPPhotos = product.get('kPPhotos', '')
		kPNickName = product.get('kPNickName', '')
		kPIconUrl = product.get('kPIconUrl', '')

		sql_statement = ('REPLACE INTO `Prouct` '
		'(`kPProuctId`, `kPCookerId`, `kPDishName`, `kPFollowBookId`, `kPPhotoNums`, `kPFrontCoverUrl`, `kPTopic`, `kPDescription`, '
		'`kPKind`, `kPSubKind`, `kPIsPublished`, `kPTags`, `kPTips`, '
		'`kPScore`, `kPPhotos`, `kPNickName`, `kPIconUrl`,  `kPCreateTime`)'
		' VALUES '
		'(%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s,%s, %s, %s, %s, %s,%s, %s)')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		try:
			yield pool.execute(sql_statement, (kPProuctId, kPCookerId, kPDishName, kPFollowBookId, kPPhotoNums, kPFrontCoverUrl, kPTopic, kPDescription,
                                               kPKind, kPSubKind, kPIsPublished, kPTags, kPTips,  
                                               kPScore, kPPhotos, kPNickName, kPIconUrl, kPCreateTime))    
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(kPProuctId)
        
	@classmethod
	@tornado.gen.coroutine
	def get_product(self,productId):
		sql_statement = ('SELECT * from `Prouct` WHERE `kPProuctId` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (productId))
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('product not found')
		cuisine = cur.fetchone()
		raise tornado.gen.Return(cuisine)
        
	@classmethod
	@tornado.gen.coroutine
	def get_someproduct(self, kPoffset, someproduct):
		sql_statement = ('SELECT * from `Prouct` ORDER BY kPCreateTime DESC LIMIT %d,%d' % (kPoffset, someproduct))
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement)
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('product not found')
		cuisine = cur.fetchall()
		raise tornado.gen.Return(cuisine)

        @classmethod
        @tornado.gen.coroutine
        def get_someproduct_by_cookerid(self, kPCookerId, kPoffset, someproduct):
                sql_statement = ("SELECT * from `Prouct` where `kPCookerId` = '%s' ORDER BY kPCreateTime DESC LIMIT %d,%d" % (kPCookerId, kPoffset, someproduct))
                pool = common.get_mysql_pool()
                if pool is None:
                        logger.error('Unknown connection pool')
                cur = None
                try:
                        cur = yield pool.execute(sql_statement)
                except Exception, e:
                        logger.error(e)
                if cur is None:
                        raise tornado.gen.Return(None)
                if cur.rowcount == 0:
                        logger.error('product not found')
                cuisine = cur.fetchall()
                raise tornado.gen.Return(cuisine)
            
	@classmethod
	@tornado.gen.coroutine
    	def get_someproduct_by_time(self, kPCreateTime, someproduct):
        	sql_statement = ('SELECT * from `Prouct` where `kPCreateTime` < %d ORDER BY kPCreateTime DESC LIMIT %d' % (kPCreateTime, someproduct))
       	 	pool = common.get_mysql_pool()
        	if pool is None:
            		logger.error('Unknown connection pool')
        	cur = None
        	try:
            		cur = yield pool.execute(sql_statement)
        	except Exception, e:
            		logger.error(e)
        	if cur is None:
            		raise tornado.gen.Return(None)
        	if cur.rowcount == 0:
            		logger.error('product not found')
        	cuisine = cur.fetchall()
        	raise tornado.gen.Return(cuisine)

    	@classmethod
    	@tornado.gen.coroutine
    	def get_someproduct_by_cookerid_time(self, kPCookerId, kPCreateTime, someproduct):
                sql_statement = ("SELECT * from `Prouct` where `kPCookerId` = '%s' and `kPCreateTime` < %d ORDER BY kPCreateTime DESC LIMIT %d,%d" 
		% (kPCookerId, kPCreateTime, someproduct))
                pool = common.get_mysql_pool()
                if pool is None:
                        logger.error('Unknown connection pool')
                cur = None
                try:
                        cur = yield pool.execute(sql_statement)
                except Exception, e:
                        logger.error(e)
                if cur is None:
                        raise tornado.gen.Return(None)
                if cur.rowcount == 0:
                        logger.error('product not found')
                cuisine = cur.fetchall()
                raise tornado.gen.Return(cuisine)
            
	@classmethod
	@tornado.gen.coroutine
	def check_product(self,productId):
		sql_statement = ('SELECT * from `Prouct` WHERE `kPProuctId` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (productId))
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount) 

class CuisineImageSQLHelper:
	
	@classmethod
	@tornado.gen.coroutine
	def add_cuisineimage(self,cuisineimage):
		iconid = cuisineimage.get('iconid', str(uuid.uuid1()))
		imagemd5 = cuisineimage.get('imagemd5')
		print 'iconid:%s ' % iconid
		image64 = cuisineimage.get('image64')
		
		sql_statement = ('REPLACE INTO `icon` '
				'(`iconid`, `imagemd5`, `image64`)'
				' VALUES '
				'(%s, %s, %s)')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			raise tornado.gen.Return(None)
		try:
			yield pool.execute(sql_statement, (iconid, imagemd5, image64))	
		except Exception, e:
			logger.error(e)
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(iconid)

	def add_cuisineimage_console(self, cuisineid, stepsnum, imagemd5, image64):
		iconid = str(uuid.uuid1())
		print 'iconid:%s ' % iconid

		sql_statement = ('insert INTO `icon` '
                        '(`iconid`, `cuisineid`, `stepsnum`, `imagemd5`, `image64`)'
                        ' VALUES '
                        '(%s, %s, %s, %s, %s)')
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisine_crawl',port=3306)
		if conn is None:
			print('Unknown connection conn')
			return
		cur=conn.cursor()
		if cur is None:
			print('Unknown connection cur')
			return
		conn.set_character_set('utf8')
		cur.execute('SET NAMES utf8;')
		cur.execute('SET CHARACTER SET utf8;')
		cur.execute('SET character_set_connection=utf8;')
		try:
			rc = cur.execute(sql_statement, (iconid, cuisineid, stepsnum, imagemd5, image64))
			conn.commit()
			cur.close()
			conn.close()
			if rc is None:
				print('insert image error')
				return
		except Exception, e:
			print(e)
			return

    	def get_cuisineimage_from_paser(self, cuisineid):

        	sql_statement = ("SELECT * from `icon` WHERE `cuisineid` = '%s'" % cuisineid)
        	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisine_crawl',port=3306)
        	if conn is None:
            		print('Unknown connection conn')
            		return
        	cur=conn.cursor()
        	if cur is None:
            		print('Unknown connection cur')
            		return
        	conn.set_character_set('utf8')
        	cur.execute('SET NAMES utf8;')
        	cur.execute('SET CHARACTER SET utf8;')
        	cur.execute('SET character_set_connection=utf8;')
        	try:
            		rc = cur.execute(sql_statement)
            		conn.commit()
            		data = cur.fetchall()
            		cur.close()
            		conn.close()
            		if data is None or len(data) == 0:
                		print('get cuisine empty')
                		return None
            		else:
                		return data
        	except Exception, e:
            		print(e)
            		return
        
    	def add_image_paser_to_cuisinebook(self, imagemd5, image64):
        	iconid = str(uuid.uuid1())
        	print 'iconid:%s ' % iconid

        	sql_statement = ('insert INTO `icon` '
                        '(`iconid`, `imagemd5`, `image64`)'
                        ' VALUES '
                        '(%s, %s, %s)')
        	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='cuisinebook',port=3306)
        	if conn is None:
            		print('Unknown connection conn')
            		return
        	cur=conn.cursor()
        	if cur is None:
            		print('Unknown connection cur')
            		return
        	conn.set_character_set('utf8')
        	cur.execute('SET NAMES utf8;')
        	cur.execute('SET CHARACTER SET utf8;')
        	cur.execute('SET character_set_connection=utf8;')
        	try:
            		rc = cur.execute(sql_statement, (iconid, imagemd5, image64))
            		conn.commit()
            		cur.close()
            		conn.close()
            		if rc is None:
                		print('insert image error')
                		return
        	except Exception, e:
            		print(e)
            		return

	@classmethod
	@tornado.gen.coroutine
	def get_cuisineimage(self, imagemd5):
		sql_statement = ('SELECT `image64` from `icon` WHERE`imagemd5` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
		cur = None
		try:
			cur = yield pool.execute(sql_statement, (imagemd5))
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		if cur.rowcount == 0:
			logger.error('imagemd5 not found')
		cuisine = cur.fetchone()
		raise tornado.gen.Return(cuisine)
	
	@classmethod
	@tornado.gen.coroutine
	def check_cuisineimage(self, imagemd5):
		sql_statement = ('SELECT `image64` from `icon` WHERE`imagemd5` = %s')
		pool = common.get_mysql_pool()
		if pool is None:
			logger.error('Unknown connection pool')
			cur = None
		try:
			cur = yield pool.execute(sql_statement, (imagemd5))
		except Exception, e:
			logger.error(e)
		if cur is None:
			raise tornado.gen.Return(None)
		raise tornado.gen.Return(cur.rowcount)
