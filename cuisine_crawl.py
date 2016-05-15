
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
import json, base64, urllib, hashlib
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

class cuisinejson:

	def __init__(self,data):
		self.data = data;
		self.dishname = ''
		self.difficulty = ''
		self.needtime = ''
		self.stepnum = 0
		self.FoodMaterial = collections.OrderedDict()
		self.FoodSteps = collections.OrderedDict()
		self.TipsSteps = []
		self.ImageSteps = collections.OrderedDict()

	def replaceunicode(self,strcode):
		strcode = strcode.replace('：','').replace('。','').replace('\t','').strip();
		return strcode;

	def get_md5_value(self, url):
		myMd5 = hashlib.md5()
		myMd5.update(url)
		myMd5_Digest = myMd5.hexdigest()
		return myMd5_Digest

	def get_decode(self, url):
		data = urllib.urlopen(url).read()
		image_base64 = base64.b64encode(data)
		return image_base64

	#def Parsingjson(self, data, dishname, difficulty, needtime, stepnum, material, FoodMaterial, FoodSteps, TipsSteps, ImageStepsNum):
	def Parsingjson(self):
		value = json.loads(self.data, object_pairs_hook=OrderedDict)
		rootlist = value.keys()
		index = 0
		#print 'len(rootlist):%d' % len(rootlist)
		while(index < len(rootlist)):
		#for rootkey in rootlist:
			#print '(key,value):(%s:%s)' %(rootlist[index],value[rootlist[index]])
			if self.replaceunicode(rootlist[index]) == u'难度':
				print '难度:%s' % value[rootlist[index]]
				self.difficulty = self.replaceunicode(value[rootlist[index]])
			elif self.replaceunicode(rootlist[index]) == u'时间':
				print ('时间:%s' % value[rootlist[index]])
				self.needtime = self.replaceunicode(value[rootlist[index]])
			elif index == 2:
				print('主料=========>')
				while(index < len(rootlist)):
					if self.replaceunicode(rootlist[index]) != 'strs':
						if len(self.replaceunicode(rootlist[index])) != 0:
							print '%s:%s' % (rootlist[index], value[rootlist[index]])
							self.FoodMaterial[rootlist[index]] = value[rootlist[index]]
						else:
							pass
						index += 1;
					else:
						index -= 1;
						break
			elif self.replaceunicode(rootlist[index]) == 'strs':
				print('步骤============>')
				foodsteps_index = value[rootlist[index]]
				foodsteps_num = 0
				while(foodsteps_num < len(value[rootlist[index]])):
					if foodsteps_index[foodsteps_num].find(u'的做法步骤') <> -1:
						self.dishname = foodsteps_index[foodsteps_num].rstrip(u'的做法步骤')
						print('菜谱名称:%s' % self.dishname)
						foodsteps_num += 1;
					steps_str = self.replaceunicode(foodsteps_index[foodsteps_num])
					m = re.match(r'^[1-9][0-9]*.$', steps_str)
                                        if m is not None:
						self.stepnum += 1
						step_i = self.replaceunicode(foodsteps_index[foodsteps_num]).replace('.','')
						step_i_value = self.replaceunicode(foodsteps_index[foodsteps_num + 1])
						print('%s:%s' % (step_i, step_i_value))
						self.FoodSteps[step_i] = step_i_value
						foodsteps_num += 2
					elif steps_str == u'小贴士':
						print('小贴士============>')
						foodsteps_num += 1
						while(foodsteps_num < len(value[rootlist[index]])):
							TipsStep = self.replaceunicode(foodsteps_index[foodsteps_num]);
							if len(TipsStep) != 0:
								print TipsStep
								self.TipsSteps.append(TipsStep);
							else:
								pass
							foodsteps_num += 1
					else:
						foodsteps_num += 1
			elif self.replaceunicode(rootlist[index]).find(u'做法图解') <> -1:
				imagekey = rootlist[index]
				imagekey = imagekey[imagekey.index(u'做法图解')+4:].strip()
				print ('%s:%s' % (imagekey, value[rootlist[index]]))
				self.ImageSteps[imagekey] = value[rootlist[index]]
			index += 1


class insertCrawlData():

	def run(self, data, cuisineUrl):
		#print data
		json1 = cuisinejson(data);
		json1.Parsingjson()

		#print '================'+json1.difficulty
		cuisine = {};
		cuisine['dishname'] = json1.dishname
		cuisine['needtime'] = json1.needtime
		cuisine['difficulty'] = json1.difficulty
		cuisine['tipsteps'] = json.dumps(json1.TipsSteps, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		cuisine['cookstep'] = json.dumps(json1.FoodSteps, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		cuisine['stepsnum'] = json1.stepnum
		cuisine['foodmaterial'] = json.dumps(json1.FoodMaterial, sort_keys=False, ensure_ascii = False, cls=DateEncoder)
		cuisine['imagesteps'] = json.dumps(json1.ImageSteps, sort_keys=False, ensure_ascii = False, cls=DateEncoder)

		print('========insert============')
		book = CuisineBookSQLHelper()
		print 'dishname:%s ' % cuisine['dishname']
		print 'needTime:%s ' % cuisine['needtime']
		print 'difficulty:%s ' % cuisine['difficulty']
		print 'tips:%s ' % cuisine['tipsteps']
		print 'CookStep:%s ' % cuisine['cookstep']
		print 'stepsNum:%s ' % cuisine['stepsnum']
		print 'FoodMaterial:%s ' % cuisine['foodmaterial']
		print 'ImageSteps:%s ' % cuisine['imagesteps']

		cuisineBookId = book.add_cuisinebook_console(cuisine, cuisineUrl)
		print 'cuisineBookId:%s ' % cuisineBookId;
		print 'cuisineUrl:%s ' % cuisineUrl;

		print('========insert steps image============')
		imagelist = json1.ImageSteps.keys()
		imagehelper = CuisineImageSQLHelper()
		imagenum = 0
		for image in imagelist:
			image64 = json1.get_decode(json1.ImageSteps[image])
			imagemd5 = json1.get_md5_value(image64)
			imagehelper.add_cuisineimage_console(cuisineBookId, image, imagemd5, image64)
			print ('%s:%s' % (image, json1.ImageSteps[image]))

if __name__ == "__main__":
	f = open("a.txt")
	t = f.read();
	cuisineUrl = 'http://www.douguo.com/cookbook/1355539.html'
	cuisinecrawl = insertCrawlData()
	cuisinecrawl.run(t, cuisineUrl)
