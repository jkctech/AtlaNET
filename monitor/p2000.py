#!/usr/bin/python

# AtlaNET P2000 Receiver - By: JKCTech
# Inspired by: https://nl.oneguyoneblog.com/2016/08/09/p2000-ontvangen-decoderen-raspberry-pi/
#
# Changelog:
# 31-07-2019 -> Initial creation / adaptation of original

import time
import sys
import subprocess
import os
import re
import fcntl
from datetime import datetime
from dateutil import tz
from termcolor import colored

# Settings
command = "rtl_fm -f 169.65M -M fm -s 22050 | multimon-ng -q -a FLEX -t raw /dev/stdin" # Command to use for the radio
triggertime = 0.03 # After nothing read for time, assume messagroup has ended
#errfile = os.path.abspath(os.path.dirname(__file__)) + "/error.log"

# Variables
run = True			# Do we want to continue for another cycle? (Used to interrupt).
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

#with open(errfile,'a') as file:
#    file.write(('#' * 20) + '\n' + (time.strftime("%H:%M:%S %Y-%m-%d")) + '\n')

# Open a subprocess and listen to the radio
#multimon_ng = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=open(errfile,'a'), shell=True)
multimon_ng = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)

# Make subprocess non-blocking so we can keep track of other stuff while nothing is happening
fcntl.fcntl(multimon_ng.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

# Initialization info
print 'Started listener with PID:',
print colored(multimon_ng.pid, 'cyan')

try:
	# We wanna run another cycle?
    while run:
		line = ''

		# If radio is NOT available
		if multimon_ng.poll() != None:
			print colored('Radio not connected or already in use.', 'red')
			run = False
			continue

		# Readline from radio
		try:
			line = multimon_ng.stdout.readline()

		# Nothing to read...
		except:
			# If we are reading a group and nothing seen for X time, assume ending
			# And send information to server
			if reading == True and time.time() - lastread > triggertime:
				print colored('\nAtlaNET:', 'cyan'),
				print colored('Acknowledged.', 'green')
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

# KEyboard Interrupt (Ctrl + C)
except KeyboardInterrupt:
	os.kill(multimon_ng.pid, 9)
	print colored('\nListener terminated by user.', 'red')