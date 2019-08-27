#!/usr/bin/python

#
# Speak.py
#
# AtlaNET P2000 Receiver - By: JKCTech
# https://github.com/jkctech/AtlaNET
# 
# Speak the alerts out loud and play a siren sound
#

import time
import pyttsx3
import pygame

def alert(message, count = 2, volume = 1):
	for x in range(count):
		pygame.mixer.init()
		pygame.mixer.music.load("../monitor/assets/siren.wav")
		pygame.mixer.music.set_volume(0.07 * volume)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue
		time.sleep(0.5)
		engine = pyttsx3.init()
		engine.setProperty('voice', 'dutch')
		engine.setProperty('volume', 1 * volume)
		engine.setProperty('rate', 150)
		engine.say(message)
		engine.runAndWait()
		time.sleep(0.5)

#alert('Ambulance. 15:18. DEN HELDER. HUISDUINERWEG. B1 10117 Rit 162029 NW 4 NOORD Interne Geneeskunde.')
alert('Traumateam. 22 uur 24. DEN HELDER. HOOGSTRAAT. A1 Regio 10.', volume=0.8)
#alert('Brandweer. 17 uur 21. DEN HELDER. JOUBERTSTRAAT. P 1 BNH-01 (Middelbrand) Brand Woning.', volume=1)
#alert('Kustwacht. 15 uur 40. DEN HELDER. Prio 1, Surfer in problemen / vermist.', volume=1)
#alert('A2. 10189. Rit. 163120. VWS. Kooypunt. Schrijnwerkersweg. Den. Helder', volume=1)
#alert('Politie. 11 uur 56. DEN HELDER. EYSERHOF. Steekpartij.', volume=1)