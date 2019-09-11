#!/usr/bin/python

#
# Logger.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Controls the saving of messages to the logfiles.
#

import os
from datetime import date, datetime
from time import strftime

# Save a message to a raw file
def saveraw(message, settings):
	if settings['common']['saveraw']:
		filename = "raw.txt"
		if settings['common']['rawdatefiles']:
			today = date.today()
			filename = today.strftime("%Y-%m-%d.txt")
		path = os.path.dirname(__file__) + settings['common']['rawpath']
		if not os.path.exists(path):
			os.makedirs(path)
		if not os.path.isfile(path + filename):
			with open(path + filename, 'w'): pass
		with open(os.path.abspath(path + filename), 'a') as file:
			file.write(message)

# Save a message to a UNIQUE raw file
def saverawunique(message, settings):
	if settings['common']['saverawunique']:
		filename = "raw.txt"
		if settings['common']['uniquedatefiles']:
			today = date.today()
			filename = today.strftime("%Y-%m-%d.txt")
		path = os.path.dirname(__file__) + settings['common']['uniquepath']
		if not os.path.exists(path):
			os.makedirs(path)
		if not os.path.isfile(path + filename):
			with open(path + filename, 'w'): pass
		with open(os.path.abspath(path + filename), 'a') as file:
			file.write(message)
		
def logError(settings, message):
		filename = "errors.txt"
		time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		path = os.path.dirname(__file__) + settings['common']['errorpath']
		if not os.path.exists(path):
			os.makedirs(path)
		if not os.path.isfile(path + filename):
			with open(path + filename, 'w'): pass
		with open(os.path.abspath(path + filename), 'a') as file:
			file.write("[{0}] {1}".format(time, message))
