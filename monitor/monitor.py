#!/usr/bin/python

#
# Monitor.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
# 
# Inspired by: https://nl.oneguyoneblog.com/2016/08/09/p2000-ontvangen-decoderen-raspberry-pi/
# Follow up on a tutorial setting up the FLEX radio: https://raspberrytips.nl/p2000-meldingen-ontvangen/
#

import time
import sys
import subprocess
import os
import re
import fcntl
import requests
import json
from datetime import datetime
from dateutil import tz
from termcolor import colored

# Config File options
config_file = os.path.abspath(os.path.dirname(__file__)) + "/config/config.json"
config_file_default = os.path.abspath(os.path.dirname(__file__)) + "/config/config_default.json"

# Fallback to default if needed
if not os.path.exists(config_file) or not os.path.isfile(config_file):
	config_file = config_file_default

# Try reading the config file
try:
	with open(config_file) as json_data_file:
		settings = json.load(json_data_file)
except:
	print colored('Could not load in config file.', 'red')
	sys.exit()

# Variables
reading = False		# Are we reading a messagegroup?
groupidold = ""		# Last GroupID to compare to see if we entered a new message.
lastread = 0		# Time of last message reading.

# Storage for server connector (Only the ones we need to send)
timestamp = ''		# Timestamp of the received message
capcodes = []		# Stores capcodes temporarily.
message = ''		# The actual received message

# Regexes
regex_prio1 = "^A\s?1|\s?A\s?1|PRIO\s?1|^P\s?1"
regex_prio2 = "^A\s?2|\s?A\s?2|PRIO\s?2|^P\s?2"
regex_prio3 = "^B\s?1|^B\s?2|^B\s?3|PRIO\s?3|^P\s?3|PRIO\s?4|^P\s?4"

# Open a subprocess and listen to the radio
multimon_ng = subprocess.Popen(settings['radio']['command'], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)

# Make subprocess non-blocking so we can keep track of other stuff while nothing is happening
fcntl.fcntl(multimon_ng.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

# Initialization info
print 'Started listener with PID:',
print colored(multimon_ng.pid, 'cyan')

try:
	# We wanna run another cycle?
    while True:
		line = ''

		# If radio is NOT available
		if multimon_ng.poll() != None:
			print colored('Radio not connected or already in use.', 'red')
			break

		# Readline from radio
		try:
			line = multimon_ng.stdout.readline()

		# Nothing to read... Is this the end?
		except:
			# If we are reading a group and nothing seen for X time, assume ending
			if reading == True and time.time() - lastread > settings['radio']['triggertime']:
				if settings['common']['debug']:
					print colored('\nAtlaNET:', 'cyan'),

				# Send to server with a POST
				try:
					r = requests.post(settings['api']['endpoint'], data={
						'apikey': settings['api']['key'],
						'timestamp': timestamp, 
						'message': message, 
						'capcodes': ','.join(capcodes)
					})
				except:
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
				reading = False
				continue
		
		finally:
			# If it's sure to be a P2000 message
			if line.__contains__("ALN") and line.startswith('FLEX'):
				# Substring the needed parts (DIFFERENT FROM ORIGINAL)
				timestamp = line[6:25]
				groupid = line[37:43]
				capcode = line[45:54]
				message = line[60:]

				# We are entering a new group...
				reading = True
				lastread = time.time()

				# Check to see if we can detect a priority and assign color
				if re.search(regex_prio1, message, re.IGNORECASE):
					color = 'red'

				elif re.search(regex_prio2, message, re.IGNORECASE):
					color = 'yellow'

				elif re.search(regex_prio3, message, re.IGNORECASE):
					color = 'green'

				else:
					color = 'magenta'

				# If same groupcode, just append the capcode to the console
				# Also append capcode to list of capcodes for this group
				if groupid == groupidold:
					print colored(capcode, 'white'),
					capcodes.append(capcode)

				# We entered a new group, so display the info
				else:
					utc = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
					utc = utc.replace(tzinfo=tz.tzutc())
					local = utc.astimezone(tz.tzlocal())
					local = local.strftime("%d-%m-%Y %H:%M:%S")
					
					print ' '
					print colored(local,'blue', attrs=['bold']), colored(message, color,  attrs=['bold']),
					print '                  ',
					print colored(capcode, 'white'),

					# This is a new group, wipe capcode list, add this one and set groupid
					capcodes = [capcode]
					#capcodes.append(capcode)
					groupidold = groupid

# Keyboard Interrupt (Ctrl + C)
except KeyboardInterrupt:
	os.kill(multimon_ng.pid, 9)
	print colored('\nListener terminated by user.', 'red')