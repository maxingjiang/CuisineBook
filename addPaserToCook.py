
#!/usr/bin/python
#-*- coding : utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8');
sys.path.append("..")
import threading
import logging
import sys
import traceback
import json, base64, urllib, hashlib, time
import collections
from collections import OrderedDict
import re
from cuisinebook import *
from cuisinebook.db_cuisine import CuisineBookSQLHelper
from cuisinebook.db_cuisine import CuisineImageSQLHelper

class DateEncoder(json.JSONEncoder):
        def default(self, obj):
                if isinstance(obj, datetime):
                        return obj.__str__()
                elif isinstance(obj, decimal.Decimal):
                        return str(obj)
                else:
                        return json.JSONEncoder.default(self, obj)

class insertCrawlDataToCook():

	def run(self, kbcookid):
		#kBCookBookId = '051872ca-0b71-11e6-a0a7-0242ac110002'
		kBCookBookId = kbcookid
		book = CuisineBookSQLHelper()
		pasercook = book.get_cuisinebook_from_paser(kBCookBookId)
		if pasercook is None:
			print 'get cuisine empty'
			return
		#cookjson = json.dumps(pasercook, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		cuisine = {};
		cuisine['kBCookBookId'] = pasercook[0]
		cuisine['kBDishName'] = pasercook[2]
		cuisine['kBTimeNeeded'] = pasercook[3]
		cuisine['kBStepNums'] = pasercook[5]
		cuisine['kBTips'] = pasercook[6]
		cuisine['kBCookSteps'] = []
		cuisine['kBFoodMaterials'] = pasercook[8]
		cuisine['kBCreateTime'] = time.time()*1000
		
		print('========insert============')
		print 'kBCookBookId:%s ' % cuisine['kBCookBookId']
		print 'kBDishName:%s ' % cuisine['kBDishName']
		print 'kBTimeNeeded:%s ' % cuisine['kBTimeNeeded']
		print 'kBStepNums:%s ' % cuisine['kBStepNums']
		print 'kBTips:%s ' % cuisine['kBTips']
		print 'kBCookSteps:%s ' % pasercook[7]
		print 'kBFoodMaterials:%s ' % cuisine['kBFoodMaterials']
		print 'kBCreateTime:%d ' % cuisine['kBCreateTime']
		#cuisineBookId = book.add_cuisinebook_paser_to_cuisinebook(cuisine)

		print('========insert steps image============')
		imagehelper = CuisineImageSQLHelper()
		imagepaser = imagehelper.get_cuisineimage_from_paser(kBCookBookId)
		if imagepaser is None:
			print 'get image empty===='
			return
		
		data = json.loads(pasercook[7]);
		for image in imagepaser:
			KBSteps = {}
			KBSteps['kPhotoSerialNum'] = image[2]
			KBSteps['kPhotoUrl'] = image[3]
			KBSteps['kPhotoDescription'] = data[str(image[2])]
			cuisine['kBCookSteps'].append(KBSteps)
			cuisine['kBFrontCoverUrl'] = image[3]
			#print json.dumps(KBSteps, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
			imagemd5 = image[3]
			image64 = image[4]
			imagehelper.add_image_paser_to_cuisinebook(imagemd5, image64)
		cuisine['kBCookSteps'] = json.dumps(cuisine['kBCookSteps'], sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		print cuisine['kBCookSteps']
		cuisineBookId = book.add_cuisinebook_paser_to_cuisinebook(cuisine)
		

if __name__ == "__main__":
	paser = insertCrawlDataToCook();
	kbcook = CuisineBookSQLHelper()
	f = open("douguo.txt", "r")
	lines = f.readlines()
	for line in lines:
		linesrc = line.replace('\n','').replace('\t','').strip()
		kbcookid = kbcook.get_kBCookId_from_paser(linesrc+'%')
		print 'id=====:%s' % kbcookid
		if kbcookid is not None:
			paser.run(kbcookid)
