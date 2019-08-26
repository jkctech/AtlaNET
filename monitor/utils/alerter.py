import os
import pyttsx3
import pygame
import time

def alert(message, count = 2, volume = 1):
	for x in range(count):
		pygame.mixer.init()
		pygame.mixer.music.load(os.path.dirname(__file__) + "/../assets/siren.wav")
		pygame.mixer.music.set_volume(0.08 * volume)
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