#!/usr/bin/python

#
# Twitter.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Twitter integration
#

import sys
from twitter import *

def sendTweet(settings, message):
	t = Twitter(auth=OAuth(
		settings['twitter']['user_key'],
		settings['twitter']['user_secret'],
		settings['twitter']['consumer_key'],
		settings['twitter']['consumer_secret']))
	try:
		status = t.statuses.update(status=message)
	except (Exception) as e:
		print e
		sys.exit()
	return status
