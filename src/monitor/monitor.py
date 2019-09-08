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
from termcolor import colored

# Import our own stuff <3
from utils.radio import *
from utils.settings import *
from utils.header import *
from utils.logger import *
from utils.alerter import *
from utils.filter import *
from utils.resolver import *
from utils.twitter_utils import *
from utils.processor import *

# Print header design
printheader()

# Get settings from files
settings = getSettings()

# Add triggers to settings
settings = setTriggers(settings)

# Download info from server
refreshServerLists(settings)

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
queue = []
lastread = 0

# Open a subprocess and listen to the radio
multimon_ng = subprocess.Popen(settings['radio']['command'], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)

# Make subprocess non-blocking so we can keep track of other stuff while nothing is happening
fcntl.fcntl(multimon_ng.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

# Check if we can access radio
time.sleep(0.5)
if multimon_ng.poll() != None:
	print colored('Cannot claim radio thread, attempting override...', 'magenta')
	killRadio()
	time.sleep(1)
	multimon_ng = subprocess.Popen(settings['radio']['command'], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)
	fcntl.fcntl(multimon_ng.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
	if multimon_ng.poll() != None:
		print colored('Could not force override, terminating...', 'red')
		sys.exit()
	else:
		print colored('Reclaimed radio, proceeding...', 'green')

# Initialization info
print 'Started listener with PID:',
print colored(multimon_ng.pid, 'cyan')
print colored("Watching...", 'cyan')

try:
	# We wanna run another cycle?
    while True:
		time.sleep(0.001) # Add a sleep so we don't burn our CPU (oops)
		line = '' # Store the received line

		# Check accessibility of the radio
		if multimon_ng.poll() != None:
			print colored('Radio terminated by external control.', 'red')
			break

		# Readline from radio
		try:
			line = multimon_ng.stdout.readline()
			saveraw(line, settings)
			if line.__contains__("ALN") and line.startswith('FLEX'):
				queue.append(line)
				lastread = time.time()
		
		# Nothing to read...
		except:
			pass

		# Process queued messages after triggertime
		if time.time() - lastread > settings['radio']['triggertime'] and len(queue) > 0:
			last_msg = ""
			last_line = ""
			capcodes = []

			cnt = 1
			queue.append('X' * 64)
			for line in queue:
				# Substring the needed parts and set globals
				capcode = line[47:54]
				message = line[60:]

				# If first or same msg, append capcode
				if message == last_msg or cnt == 1:
					last_msg = message
					last_line = line
					capcodes.append(capcode)
				
				# If different msg or last queue item, push out alert
				if message != last_msg:
					# Save raw if wanted
					saverawunique(last_msg, settings)

					capinfo = getCapInfo(settings, capcodes)
					prio = getPrio(last_msg)

					printMessage(last_line, prio)
					printCapInfo(settings, capinfo, capcodes)

					msgobject = {
						"timestamp": last_line[6:25],
						"message": last_msg,
						"capcodes": capcodes,
						"capinfo": capinfo,
						"prio": prio
					}

					process(settings, msgobject)

					# Set for next
					last_msg = message
					last_line = line
					capcodes = [capcode]
				cnt += 1
			queue = []

# Keyboard Interrupt (Ctrl + C)
except KeyboardInterrupt:
	print colored('\nTerminated by user.', 'red')

# Catch crashes
except (Exception) as e:
	alert(settings, "Monitor crash")
	print colored('\nException:', 'red')
	print e

# Cleanup
finally:
	killRadio()
	if con:
		con.close()