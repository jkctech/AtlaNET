# Primitive Logger for debugging purposes.

import os
import time
import sys
import subprocess
import fcntl
import re
from termcolor import colored
from datetime import datetime
from dateutil import tz

groupidold = ""

mmt = ['0120901', '0320591', '0320592', '0620901', '0923993', '1220009', '1420059']

print '\033c',

multimon_ng = subprocess.Popen("rtl_fm -f 169.65M -M fm -s 22050 | multimon-ng -a FLEX -t raw /dev/stdin", stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)
#multimon_ng = subprocess.Popen("rtl_fm -f 169.65M -M fm -s 22050 -p 83 -g 30 | multimon-ng -a FLEX -t raw /dev/stdin", stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)
fcntl.fcntl(multimon_ng.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

try:
    while True:
		time.sleep(0.0001) # Add a sleep so we don't burn our CPU (oops)
		line = ''

		# Check accessibility of the radio
		if multimon_ng.poll() != None:
			print colored('Radio terminated by external control.', 'red')
			break

		# Readline from radio
		try:
			line = multimon_ng.stdout.readline()
			if line.__contains__("ALN"):
				timestamp = line[6:25]
				groupid = line[37:43]
				capcode = line[47:54]
				message = line[60:]

				#print "MSG: " + message
				#print "CAP: " + capcode
				#print "TIM: " + timestamp
				#print "GID: " + groupid

				if capcode in mmt:
					print colored("TRAUMATEAM", 'red')

				if groupid == groupidold:
					print colored(capcode, 'white'),

				else:
					utc = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
					utc = utc.replace(tzinfo=tz.tzutc())
					local = utc.astimezone(tz.tzlocal())
					local = local.strftime("%d-%m-%Y %H:%M:%S")
					
					print '\n'
					print colored(local,'blue', attrs=['bold']), colored(message, 'magenta',  attrs=['bold']),
					print '                  ',
					print colored(capcode, 'white'),

					groupidold = groupid
		
		# Nothing to read...
		except:
			pass

# Keyboard Interrupt (Ctrl + C)
except KeyboardInterrupt:
	print colored('\nTerminated by user.', 'red')