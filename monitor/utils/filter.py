#!/usr/bin/python

#
# Filter.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
# 
# Functions to filter and process all incoming alerts as far as we can,
# before sending them to the server.
#

import re

# Return the priority of the alert
def getPrio(msg):
	# Tests
	if re.search("((^|\s)(test(oproep)?|proefalarm)|The quick brown fox jumps)", msg, re.IGNORECASE):
		return 5

	# A prio's [1 - 4]
	for i in range(1,5):
		if re.search("(^A\s?%d|P(RIO)?\s?%d)" % (i,i), msg, re.IGNORECASE):
			return i

	# B prio's [1 - 3]
	for i in range(1,4):
		if re.search("(^|\s)B\s?%d" % (i), msg, re.IGNORECASE):
			return i + 9

	return 0

# Is this a revoke message?
def isRevoke(msg):
	return bool(re.search("intrekken", msg, re.IGNORECASE))

# TRY to find out the dicipline of the call
#def getDicipline(capcodes, msg):

'''
print "Prio\tRevoke\tMessage"

with open('../testdata/flex_clean.txt','r') as f:
	for x in f.readlines():
		print "%d\t%d\t%s" % (getPrio(x), int(isRevoke(x)), x),
'''