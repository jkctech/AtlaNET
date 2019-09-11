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

import requests
from datetime import datetime
from termcolor import colored

# Own utils
from utils.alerter import *
from utils.resolver import *
from utils.twitter_utils import *

# Emoji Icons
light = u'\U0001f6A8'.encode('utf-8')
caduceus = u'\U00002695'.encode('utf-8')
heli = u'\U0001f681'.encode('utf-8')
ambu = u'\U0001f691'.encode('utf-8')
brw = u'\U0001F692'.encode('utf-8')
pol = u'\U0001F693'.encode('utf-8')
boat = u'\U0001F6E5'.encode('utf-8')
pager = u'\U0001F4DF'.encode('utf-8')

red = u'\U0001F534'.encode('utf-8')

specials = {
	# Heli's
	"0120901" : red + " #TraumaHeli #LFL01 #LifeLiner1 " + heli,
	"1420059" : red + " #TraumaHeli #LFL02 #LifeLiner2 " + heli,
	"0923993" : red + " #TraumaHeli #LFL03 #LifeLiner3 " + heli,
	"0320591" : red + " #Waddenheli #Medic01 " + heli,
	"0320592" : red + " #Waddenheli #Medic01 " + heli,
	"1220009" : red + " #Traumateam #MMT " + ambu,

	# Sigma
	"0220828" : red + " #SIGMA " + caduceus,
	"0402110" : red + " #SIGMA " + caduceus
}

def process(settings, msgobject):
	capinfo = msgobject['capinfo']
	capcodes = msgobject['capcodes']
	message = msgobject['message']
	timestamp = msgobject['timestamp']

	# Send to server
	if settings['common']['debug']:
		print colored('AtlaNET:', 'cyan'),

	# Send to server with a POST
	try:
		r = requests.post(settings['api']['endpoint'] + "post/insert", data={
			'apikey': settings['api']['key'],
			'timestamp': timestamp, 
			'message': message, 
			'capcodes': ','.join(capcodes)
		})
	except (Exception) as e:
		logError(settings, "Could not reach endpoint: " + e)
		if settings['common']['debug']:
			print colored('FAILED!', 'red'),
			print colored('Could not reach endpoint.', 'magenta')
	else:
		if settings['common']['debug']:
			if r.status_code == 200:
				print colored(r.reason, 'green'),
				print colored(r.text, 'cyan')
			else:
				print colored(r.status_code, 'red'),
				print colored(r.reason, 'magenta')

	if settings['common']['debug']:
		print ''

	# Special alerts for twitter system
	for cap in capcodes:
		if cap in specials:
			sendTweet(settings, specials[cap] + " " + message)
			break

	# Check for keywords and capcodes on local alarm
	trigger = hasTrigger(settings, capcodes, message)
	if trigger:
		# Send high prio tweets to private Twitter
		disc = getDiscipline(settings, capinfo)
		did = disc['id']

		ok = [2,3,5,6,7,8]
		if did in ok:
			if did == 2: icon = pol
			elif did == 3: icon = brw
			elif did == 5: icon = heli
			elif did == 6 or did == 7 or did == 8: icon = boat
			else: icon = pager

			msg = "{0} #{1} #{2} {3} {4}".format(
				red, 
				trigger.replace(" ", ""), 
				disc['name'].replace(" ", ""),
				icon,
				message
			)
			sendTweet(settings, msg, user="JKCTech")

		# Volume control on schedule
		vol = 1
		now = datetime.now()
		if now.hour >= 22 or now.hour <= 8:
			vol = 0.35
		# Send alert
		alert(settings, message, volume=vol)
