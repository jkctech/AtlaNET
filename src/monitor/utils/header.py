from termcolor import colored
from datetime import datetime

def printheader():
	today = datetime.now()

	print '\033c' + '=' * 40,
	print colored("""
     _   _   _       _   _ _____ _____ 
    / \ | |_| | __ _| \ | | ____|_   _|
   / _ \| __| |/ _` |  \| |  _|   | |
  / ___ \ |_| | (_| | |\  | |___  | |
 /_/   \_\__|_|\__,_|_| \_|_____| |_|
	""", 'cyan')
	print '=' * 40
	print "Current system time:",
	print colored(today.strftime("%Y-%m-%d %H:%M:%S"), 'red')