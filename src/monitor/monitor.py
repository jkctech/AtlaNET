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

import os
import time
import sys
import subprocess
import re
import fcntl
import requests
import mysql.connector
from datetime import datetime, date
from dateutil import tz
from termcolor import colored

# Import our own stuff <3
from utils.settings import *
from utils.header import *
from utils.logger import *
from utils.alerter import *
from utils.filter import *
from utils.resolver import *

# Disable pygame's "hello" message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Print header design
printheader()

# Get settings from files
settings = getSettings()

# Add triggers to settings
settings = setTriggers(settings)

# Connect to database
con = None
if settings['mysql']['enabled']:
	print 'Database Connection:',
	try:
		con = mysql.connector.connect(
			host=settings['mysql']['host'],
			user=settings['mysql']['username'],
			passwd=settings['mysql']['password'],
			database=settings['mysql']['database']
		)
		print colored('SUCCESS', 'green')
	except Exception as e:
		print colored('ERROR', 'red')
		print colored(e, 'red')
		exit()

# Variables
reading = False		# Are we reading a messagegroup?
groupidold = ""		# Last GroupID to compare to see if we entered a new message.
lastread = 0		# Time of last message reading.

# Storage for server connector (Only the ones we need to send)
timestamp = ''		# Timestamp of the received message
capcodes = []		# Stores capcodes temporarily.
message = ''		# The actual received message
prio = 0			# Priority of alert

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
		# Add a sleep so we don't burn our CPU (oops)
		time.sleep(0.001)

		line = ''

		# If radio is NOT accessible
		if multimon_ng.poll() != None:
			print colored('Cannot claim radio thread. (Already in use?)', 'red')
			break

		# Readline from radio
		try:
			line = multimon_ng.stdout.readline()

		# Nothing to read... Is this the end?
		except:
			# If we are reading a group and nothing seen for X time, assume ending
			if reading == True and time.time() - lastread > settings['radio']['triggertime']:
				# Save raw if wanted
				saverawunique(message, settings)

				# Request capcode info from AtlaNET
				capinfo = getCapInfo(settings, capcodes)
				printCapInfo(capinfo, capcodes)

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

				if settings['common']['debug']:
					print ''

				reading = False
				
				# Check if we want to play an alert
				if hasTrigger(settings, capcodes, message):
					alert(settings, message)
				continue
		
		finally:
			# Start of a new P2000 message
			if line.__contains__("ALN") and line.startswith('FLEX'):
				# Save raw if wanted
				saveraw(line, settings)

				# Substring the needed parts and set globals
				timestamp = line[6:25]
				groupid = line[37:43]
				capcode = line[47:54]
				message = line[60:]
				prio = getPrio(message)

				# We are entering a new group...
				reading = True
				lastread = time.time()

				# Define color for monitor
				if prio is 1:
					color = 'red'
				elif prio is 2:
					color = 'yellow'
				elif prio is 3 or prio is 10:
					color = 'green'
				elif prio is 4 or prio is 11:
					color = 'cyan'
				else:
					color = 'white'

				# If same groupcode, just append the capcode to the console
				# Also append capcode to list of capcodes for this group
				if groupid == groupidold:
					capcodes.append(capcode)

				# We entered a new group, so display the info
				else:
					utc = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
					utc = utc.replace(tzinfo=tz.tzutc())
					local = utc.astimezone(tz.tzlocal())
					local = local.strftime("%d-%m-%Y %H:%M:%S")

					print "\n", colored(local,'blue', attrs=['bold']), colored(message, color,  attrs=['bold'])

					# This is a new group, wipe capcode list, add this one and set groupid
					capcodes = [capcode]
					#capcodes.append(capcode)
					groupidold = groupid

# Keyboard Interrupt (Ctrl + C)
except KeyboardInterrupt:
	print colored('\nTerminated by user.', 'red')

# Catch crashes
except (Exception) as e:
	alert(settings, "Monitor crash!", 1)
	print colored('\nException:', 'red')
	print e

# Cleanup
finally:
	multimon_ng.kill()
	if con:
		con.close()