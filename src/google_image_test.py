# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 10:46:09 2016

@author: Luc

Handles all the communication with the Google Vision Cloud 
"""

import argparse
import base64
import json
import os

from IPython import embed
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

class Vision(object):

	def __init__(self):
		#Connects to the google vision api
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'My First Project-654a00650dac.json'
		self.credentials = GoogleCredentials.get_application_default()
		self.service = discovery.build('vision', 'v1', credentials=self.credentials)
	
	def classify(self, image):
	"""
	Sends an image to the Google Vision Cloud, and recieves the json response/classification
	"""
		#create request
		image_content = base64.b64encode(image.read())
		service_request = self.service.images().annotate(body={
			'requests' : [{
				'image' : {
					'content' : image_content.decode('UTF-8')
				},
				'features' : [{
					'type' : 'LABEL_DETECTION','maxResults' : 5}]
			}]
		})
		
		response = service_request.execute() 
		
		#label = str(response['responses'][0]['labelAnnotations'][0]['description'])
		#score = str(response['responses'][0]['labelAnnotations'][0]['score'])
		
		responses = response['responses'][0]['labelAnnotations']
		#print responses
		return responses
		
	def check_for_match(self, image, label):
		#Compares the image labels with the given target label.
		responses = self.classify(image)
		for prediction in responses:
			if str(prediction['description']) == label:
				return True, str(prediction['score'])

		return False, -1

if __name__ == "__main__" :
	vis = Vision()
	print vis.check_label("../frames/0/IMG_20161119_195704.jpg", "glasses")