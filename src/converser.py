# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 00:10:16 2016

@author: Luc

Class handling all the user communication. 
Sends text input provided by the user to the watson chat api
and shows the response to the user.
"""


import json
from watson_developer_cloud import ConversationV1
from IPython import embed
import process_video
import pyttsx 
import cv2
#import speech_recognition as sr #doesnt work
import numpy as np
from Tkinter import *


"""
TTS (text-to-speech) settings
"""

font = cv2.FONT_HERSHEY_PLAIN
volume = 5
rate = 180

class Converser(object):
	
	def __init__(self, key_file = 'conv-api-key.json'):
		self.workspace_id = "98a57a51-e9d9-4252-b56d-5d6de63ef73b"
		with open(key_file, 'rb') as f:
			credentials = json.load(f)
			
		#Connect to the watson chatbot
		self.conversation = ConversationV1(username = str(credentials['username']) , password = str(credentials['password']), version = '2016-09-20')
		self.context = {}
		
		#More tts settings
		self.tts = pyttsx.init()
		self.tts.setProperty('rate', rate)
		self.tts.setProperty('value', volume)
		#self.create_main_screen()
		#self.recog = sr.Recognizer()
	
	def create_main_screen(self):
		"""
		Begin of nicer looking interface, not finished and not used
		"""
		self.blank_image = np.full((1280,1920, 3), 255, np.uint8)
		cv2.namedWindow("Background", cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty("Background", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		cv2.imshow("Background", self.blank_image)
		
	def sent_text(self, message = ""):
		"""
		Sent user query to watson and recieves response
		"""
		response = self.conversation.message(workspace_id = self.workspace_id, message_input = {'text' : message}, context = self.context)
		
		#print response
		return response

	def parse_response(self, response):
		"""
		Parse the json response from watson.
		"""
		self.context = response['context']
		text = response['output']['text']
		intents = response['intents'] #is a list, should filter
		if len(intents) > 0:
			intent = intents[0]['intent'] #get the intent of the message
		else:
			intent = ""
			
		return str(text[0]), intent

	def write_to_screen(self, text):
		"""
		Not used, not finished, part of the gui
		"""
		self.blank_image = np.full((1280,1920, 3), 255, np.uint8)
		cv2.putText(self.blank_image, text,(40,300), font, 8,(0,0,0),3,cv2.LINE_AA)
		cv2.imshow("Background", self.blank_image)
		cv2.waitKey(1)
		

	def get_user_speech_input(self):
		"""
		Speech recognition, doesn't work that well.
		"""
		with sr.Microphone() as source:
			print "You can speak!"
			audio = self.recog.listen(source, 5)
			
		#WIT_AI_KEY = "4KKA5EH6VFWPMWYZTSFHNJJZYCZHGTAQ"
		print "sending it"
		try:
			print "Google thinks: " + self.recog.recognize_google(audio)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			
			
	def get_user_text_input(self):
		"""
		Waits for text input from the user
		"""
		user_input = raw_input('You: ')
		return user_input
	
	def start(self):
		"""
		Start the main loop
		Asks a question, waits for input, and processes the input
		"""
		cv2.waitKey(1)
		text, _ = self.parse_response(self.sent_text())
		print text
		self.speak(text)
		while(True):
			user_input = self.get_user_text_input()
			response = self.sent_text(message = user_input)
			text, intent = self.parse_response(response)

			if response['output'].get('query') is not None:
				query = str(response['output']['query'])
				self.speak('Looking for ' + query) 
				self.speak('This might take a while')
				found, image = process_video.loop_through_frames(label = query)
				if found:
					print text
					self.speak(text)
					cv2.imshow("Here it is!", image)
					cv2.waitKey()
				else:
					self.speak("I am sorry, I could not find what you were looking for")
					
				return
			self.speak(text)
			#if intent == 'Lost':
			#	key = response['entities'] 
			#	print "I am looking for: " + key
			print text

			
	def speak(self, utterance):
		self.tts.say(utterance)
		#self.write_to_screen(utterance)
		self.tts.runAndWait()
	
		
	
		
if __name__ == "__main__":
	
	conv = Converser()
	#conv.get_user_speech_input()
	#conv.speak("The quick brown fox jumped over the lazy dog")
	#conv.sent_text()
	conv.start()
	#conv.sent_text(message = "I have lost something")
	