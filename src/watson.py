# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:16:02 2016

@author: Luc
"""

import json
import StringIO
from PIL import Image
from IPython import embed


from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition

class Watson(object):
	
	def __init__(self, key_file = 'api-key.txt'):
		with open(key_file, 'rb') as f:
			api_key = f.readline()
			self.visual_recognition = VisualRecognition("2016-05-20", api_key = api_key)
			print(json.dumps(self.visual_recognition.list_classifiers(), indent=2))
			embed()
		
	def classify(self, image):
		result = self.visual_recognition.classify(image)
		with open('response.json', 'wb') as outfile:
			json.dump(result, outfile)
		
		return result
			
	def load_json_file(self, json_file = "response.json"):
		
		with open(json_file, 'rb') as f:
			data = json.load(f)
			
		return data
	
	def check_for_match(self, data, label):
		predictions = data['images'][0]['classifiers'][0]['classes']
		for predict in predictions:
			if predict['class'] == label:
				return True, predict['score']
		
		return False, -1
		
	def check_for_match(self, image, label):
		json_response = self.classify(image)
		return self.check_label(json_response, label)
		

if __name__ == "__main__":
	watson = Watson()
	#with open("../frames/0/IMG_20161119_195704.jpg", 'rb') as image:
	#	watson.find_match(image)
	watson.load_json_file()
	

