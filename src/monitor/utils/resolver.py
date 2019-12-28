#!/usr/bin/python

#
# Resolver.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Connects to the endpoint in attemtp to resolve capcodes and locations
#

import requests
import json
from termcolor import colored
from datetime import datetime
from dateutil import tz
from utils.logger import *

def getCapInfo(settings, capcodes):
	try:
		r = requests.get(settings['api']['endpoint'] + "get/capinfo", params={
			'apikey': settings['api']['key'],
			'capcodes': ','.join(capcodes)
		})
	except (Exception) as e:
		logError(settings, "Cap resolve error: " + str(e))
		print colored('Capcode Database:', 'cyan'), colored('FAILED!', 'red'),
		print colored('Could not reach endpoint.', 'magenta')
		print colored(e, 'white')
		return
	if r.status_code is not 200:
		print colored(r.status_code, 'red')
		print colored(r.text, 'white'),
	try:
		capinfo = json.loads(r.text)['result']
	except:
		return []
	return capinfo

def printCapInfo(settings, capinfo, capcodes):
	for capcode in capcodes:
		print '                   ',
		print colored(capcode, 'red') + ":",
		infos = []
		if capinfo:
			if capcode in capinfo:
				if capinfo[capcode]['discipline']:
					infos.append(enumToDiscipline(settings, capinfo[capcode]['discipline'])['name'])
				if capinfo[capcode]['plaats']:
					infos.append(str(capinfo[capcode]['plaats']).encode('utf-8'))
				if capinfo[capcode]['description']:
					infos.append(str(capinfo[capcode]['description']).encode('utf-8'))
			if len(infos) == 0:
				infos.append("Onbekend")
			print str(" | ".join(infos))
		else:
			print ""

def printMessage(line, prio):
	timestamp = line[6:25]
	message = line[60:]

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

	utc = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
	utc = utc.replace(tzinfo=tz.tzutc())
	local = utc.astimezone(tz.tzlocal())
	local = local.strftime("%d-%m-%Y %H:%M:%S")
	
	print "\n", colored(local,'blue', attrs=['bold']), colored(message, color,  attrs=['bold'])


def enumToDiscipline(settings, discipline):
	return settings['lists']['disciplines'][str(discipline)]
	pass

def getDiscipline(settings, capinfo):
	result = []
	order = [10, 9, 5, 6, 7, 8, 13, 12, 3, 2, 4, 11, 14, 1]
	if capinfo:
		for cap in capinfo:
			if capinfo[cap]['discipline']:
				result.append(capinfo[cap]['discipline'])
		for i in order:
			if i in result:
				return enumToDiscipline(settings, i)
	
