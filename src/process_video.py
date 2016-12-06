# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:43:38 2016

@author: Luc
"""

from watson import Watson
from google_image_test import Vision
import numpy as np
import cv2
import time
from tqdm import tqdm
import os
from IPython import embed

cap = cv2.VideoCapture('../vids/vid3.mp4')
font = cv2.FONT_HERSHEY_PLAIN

def process_video():
	n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	n_captures = 10
	print n_frames
	
	i = 0
	while i < n_frames:
		print i
		ret, frame = cap.read()
		if ret:#acturally retrieved an image
			i+=1
			#cv2.imshow('frame', frame)
			if (i%(n_frames/n_captures) == 0):	
				
				cv2.imwrite('../frames/frame{}.png'.format(i/n_captures), frame, [cv2.IMWRITE_PNG_COMPRESSION, 1])
				
	print "n_frames{}".format(i)
	cap.release()
	cv2.destroyAllWindows()

	
def loop_through_frames(folder = "../frames/3", label = "glasses"):
	#watson = Watson()
	vision = Vision()
	frames = os.listdir(folder)
	for frame in tqdm(frames):
		if frame.split('.')[-1] == 'jpg':
			with open(folder + '/' + frame, 'rb') as image:
				result, confidence = vision.check_for_match(image, label)
				if result: 
					cvImage = cv2.imread(folder + '/' + frame)
					r = 500.0 / cvImage.shape[1]
					dim = (500, int(cvImage.shape[0] * r))
					cvImage = cv2.resize(cvImage, dim)
					cv2.putText(cvImage, label.format(confidence),(10,20), font, 1,(0,0,255),1,cv2.LINE_AA)
					cv2.putText(cvImage,'Confidence of: {}'.format(confidence),(10,40), font, 1,(0,0,255),1,cv2.LINE_AA)

					return True, cvImage
	return False, None

def test_folder(folder = '../frames/0'):
	watson = Watson()
	frames = os.listdir(folder)
	for frame in tqdm(frames):
		if frame.split('.')[-1] == 'jpg':
			with open(folder + '/' + frame, 'rb') as image:
				result= watson.classify(image)
				#print result
				if result: 
					cvImage = cv2.imread(folder + '/' + frame)
					r = 500.0 / cvImage.shape[1]
					dim = (500, int(cvImage.shape[0] * r))
					cvImage = cv2.resize(cvImage, dim)
					cv2.imshow("image", cvImage)
					cv2.waitKey()
					
if __name__ == "__main__":
	test_folder()


	

	