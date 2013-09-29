#! /usr/bin/env python

#This script is run at boot using /etc/rc.local
#It polls a file to see if there is someone waiting
#to get into the room. The file is: /var/www/door.txt
#A 1 denotes an unanswered door command, at which point
#the Pi will open the door and reset the file to 0.


import RPi.GPIO as GPIO
import time

motordig = 16
motorpwm = 18
openLED  = 12
closeLED = 10

#Setup GPIO and pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorpwm,GPIO.OUT)
GPIO.setup(motordig,GPIO.OUT)
GPIO.setup(openLED,GPIO.OUT)
GPIO.setup(closeLED,GPIO.OUT)

#Zero everything to start
p = GPIO.PWM(motorpwm,100)
p.start(0)
GPIO.output(motordig,GPIO.LOW)
GPIO.output(openLED,GPIO.LOW)
GPIO.output(closeLED,GPIO.LOW)

def openDoor():
	#Open door
	GPIO.output(closeLED,GPIO.LOW)
	GPIO.output(openLED,GPIO.HIGH)
	GPIO.output(motordig,GPIO.LOW)
	p.ChangeDutyCycle(50)
	time.sleep(4.5)
	p.ChangeDutyCycle(0)
	
	#Hold open
	GPIO.output(closeLED,GPIO.LOW)
	GPIO.output(openLED,GPIO.LOW)
	time.sleep(10)
	
	#Close
	GPIO.output(closeLED,GPIO.HIGH)
	GPIO.output(openLED,GPIO.LOW)
	p.ChangeDutyCycle(50)
	GPIO.output(motordig,GPIO.HIGH)
	time.sleep(8.5)
	
	#Rest
	GPIO.output(closeLED,GPIO.LOW)
	GPIO.output(openLED,GPIO.LOW)
	p.ChangeDutyCycle(0)
	GPIO.output(motordig,GPIO.LOW)

def writeLog():
	logFile = open('/home/pi/opendoor.log','a')
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	logFile.write(timestamp + " Opened door\n")
	logFile.close()

#Main loop
try:
	while 1:
		doorfile = open('/var/www/door.txt','r+')
		doorcmd  = doorfile.read(2)
		#print doorcmd
		if(doorcmd == '1'):
			doorfile.seek(0)
			doorfile.write('0')
			openDoor()
			writeLog()
except KeyboardInterrupt:
	pass
p.stop()
GPIO.cleanup()
doorfile.close()
