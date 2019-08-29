import sys
import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

time.sleep(2)
ser.write('+')
time.sleep(5)
ser.write('-')