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
from utils.logger import *

def sendTweet(settings, message, user = "AtlaNET_P2000"):
	twuser = settings['twitter'][user]
	status = False
	t = Twitter(auth=OAuth(
		twuser['user_key'],
		twuser['user_secret'],
		twuser['consumer_key'],
		twuser['consumer_secret']))
	try:
		status = t.statuses.update(status=message)
	except (Exception) as e:
		print e
		logError(settings, e)
	return status
