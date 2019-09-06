#!/usr/bin/python

#
# Processor.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Processes every alert and determines what we should do.
# Idealy you create your custom workflow here if you want to.
#

from datetime import datetime
from utils.alerter import *
from utils.twitter_utils import *

# Emoji Icons
light = u'\U0001f6A8'
heli = u'\U0001f681'
ambu = u'\U0001f691'
caduceus = u'\U00002695'

purple = u'\U0001F7E3'
green = u'\U0001F7E2'
yellow = u'\U0001F7E1'
red = u'\U0001F534'

specials = {
	# Heli's
	"0120901" : purple + " #Traumateam #lfl01 #LifeLiner1 " + heli,
	"1420059" : purple + " #Traumateam #lfl02 #LifeLiner2 " + heli,
	"0923993" : purple + " #Traumateam #lfl03 #LifeLiner3 " + heli,
	"0320591" : green + " #Traumateam #medic01 #Waddenheli " + heli,
	"0320592" : green + " #Traumateam #medic02 #Waddenheli " + heli,
	"1220009" : yellow + " #Traumateam #MMT " + ambu,

	# Sigma
	"0220828" : red + " #SIGMA " + caduceus,
	"0402110" : red + " #SIGMA " + caduceus
}

def process(settings, capcodes, message):
	# Special alerts for twitter system
	for cap in capcodes:
		if cap in specials:
			sendTweet(settings, specials[cap] + " " + message)
			break

	# Check for keywords and capcodes on local alarm
	if hasTrigger(settings, capcodes, message):
		# Volume control on schedule
		vol = 1
		now = datetime.now()
		if now.hour >= 22 or now.hour <= 8:
			vol = 0.3
		# Send alert
		alert(settings, message, volume=vol)
