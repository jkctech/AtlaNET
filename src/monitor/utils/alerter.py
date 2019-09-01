#!/usr/bin/python

#
# Alerter.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Controller determening if alerts should be fired and it's funciton to do so.
#

import os
import sys
import pyttsx3
import pygame
import time
import serial

def alert(settings, message, count = 2, volume = 1):
	ser = serial.Serial(settings['serial']['port'], settings['serial']['baudrate'])
	time.sleep(2)
	ser.write('+')
	for x in range(count):
		pygame.mixer.init()
		pygame.mixer.music.load(os.path.dirname(__file__) + "/../assets/siren.wav")
		pygame.mixer.music.set_volume(0.08 * volume)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
		time.sleep(0.5)
		engine = pyttsx3.init()
		engine.setProperty('voice', 'dutch')
		engine.setProperty('volume', 1 * volume)
		engine.setProperty('rate', 160)
		engine.say(message)
		engine.runAndWait()
		time.sleep(0.5)
	ser.write('-')

def hasTrigger(settings, capcodes, message):
	for capcode in capcodes:
		capcode = capcode[2:]
		if capcode in settings['triggers']['capcodes']:
			return True
	for word in settings['triggers']['words']:
		if message.lower().__contains__(str(word.lower())):
			return True
	return False