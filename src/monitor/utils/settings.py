#!/usr/bin/python

#
# Settings.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
#
# Read settings from file.
#

import os
import sys
import json
import requests
from termcolor import colored

def getSettings():
	# Config File options
	config_file = os.path.abspath(os.path.dirname(__file__)) + "/../config/config.json"
	config_file_default = os.path.abspath(os.path.dirname(__file__)) + "/../config/config_default.json"

	# Fallback to default if needed
	if not os.path.exists(config_file) or not os.path.isfile(config_file):
		config_file = config_file_default

	# Try reading the config file
	try:
		with open(config_file) as json_data_file:
			return json.load(json_data_file)
	except (Exception) as e:
		print colored('Could not load in config file:', 'red')
		print colored(e, 'red')
		sys.exit()

def setTriggers(settings):
	path_capcodes = os.path.abspath(os.path.dirname(__file__)) + "/../config/triggers/capcodes.txt"
	tr_capcodes = open(path_capcodes, "r").read().splitlines()
	path_words = os.path.abspath(os.path.dirname(__file__)) + "/../config/triggers/words.txt"
	tr_words = open(path_words, "r").read().splitlines()
	settings['triggers'] = dict()
	settings['triggers']['capcodes'] = tr_capcodes
	settings['triggers']['words'] = tr_words
	return settings

def getDisciplines(settings):
	try:
		r = requests.get(settings['api']['endpoint'] + "get/disciplines", params={
			'apikey': settings['api']['key']
		})
	except (Exception) as e:
		print colored('Could not download discipline list.', 'red')
		print e
		sys.exit()
	if r.status_code is not 200:
		print colored('Could not read discipline list.', 'red')
		print str(r.status_code) + ": " + r.reason
		sys.exit()
	try:
		result = json.loads(r.text)
	except:
		print colored('Could not load JSON discipline list.', 'red')
		sys.exit()
	return result

def getRegios(settings):
	try:
		r = requests.get(settings['api']['endpoint'] + "get/regios", params={
			'apikey': settings['api']['key']
		})
	except (Exception) as e:
		print colored('Could not download regio list.', 'red')
		print e
		sys.exit()
	if r.status_code is not 200:
		print colored('Could not read regio list.', 'red')
		print str(r.status_code) + ": " + r.reason
		sys.exit()
	try:
		result = json.loads(r.text)
	except:
		print colored('Could not load JSON regio list.', 'red')
		sys.exit()
	return result


def refreshServerLists(settings):
	settings['lists'] = dict()
	settings['lists']['disciplines'] = getDisciplines(settings)['result']
	settings['lists']['regios'] = getRegios(settings)['result']