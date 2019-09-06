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

def getCapInfo(settings, capcodes):
	try:
		r = requests.get(settings['api']['endpoint'] + "get/capinfo", params={
			'apikey': settings['api']['key'],
			'capcodes': ','.join(capcodes)
		})
	except (Exception) as e:
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
		if capcode in capinfo:
			if capinfo[capcode]['discipline']:
				infos.append(disciplineToString(settings, capinfo[capcode]['discipline'])['name'])
			if capinfo[capcode]['plaats']:
				infos.append(str(capinfo[capcode]['plaats']))
			if capinfo[capcode]['description']:
				infos.append(str(capinfo[capcode]['description']))
		if len(infos) == 0:
			infos.append("Onbekend")
		print " | ".join(infos)

def disciplineToString(settings, discipline):
	return settings['lists']['disciplines'][str(discipline)]
	pass