#! /usr/bin/env python

#This script is run at boot using /etc/rc.local
#It polls a file to see if there is someone waiting
#to get into the room. The file is: /var/www/door.txt
#A 1 denotes an unanswered door command, at which point
#the Pi will open the door and reset the file to 0.


import RPi.GPIO as GPIO
import time
import json

motordig = 16	#Motor digital pin (directional)
motorpwm = 18	#Motor PWM pin (power/speed)
openLED  = 12	#LED for when door is opening
closeLED = 10	#LED for when door is closing

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


########## FUNCTION DECLARATIONS ##########

# loadTimings():
# Loads motor timing settings from
# /home/pi/opendoor_timing.txt
#
# Returns a list containing the number
# of seconds the motor should run to open
# the door, pause, and then close the door
# in that order.
def loadTimings():
        path = '/home/pi/opendoor_timing.txt'
        jsonfile = open(path,'r')
        timing = json.load(jsonfile)
        return [float(timing['open']), float(timing['pause']), float(timing['close'])]


# openDoor():
# This function interacts with
# the Raspberry Pi's GPIO to
# send the proper signal to the motor
# controller with the right timing
def openDoor():
	#Get timings from settings file
	oTime, pTime, cTime = loadTimings()
	
	#Open door
	GPIO.output(closeLED,GPIO.LOW)	#LEDs
	GPIO.output(openLED,GPIO.HIGH)
	
	GPIO.output(motordig,GPIO.LOW)	#Motor
	p.ChangeDutyCycle(50)
	
	time.sleep(oTime)
	
	p.ChangeDutyCycle(0)
	
	
	#Pause while open
	GPIO.output(closeLED,GPIO.LOW)	#LEDs
	GPIO.output(openLED,GPIO.LOW)
	
	time.sleep(pTime)
	
	
	#Close
	GPIO.output(closeLED,GPIO.HIGH)	#LEDs
	GPIO.output(openLED,GPIO.LOW)
	
	GPIO.output(motordig,GPIO.HIGH)	#Motor
	p.ChangeDutyCycle(50)

	time.sleep(cTime)
	
	
	#Rest
	GPIO.output(closeLED,GPIO.LOW)	#LEDs
	GPIO.output(openLED,GPIO.LOW)

	GPIO.output(motordig,GPIO.LOW)	#Motor
	p.ChangeDutyCycle(0)


########## MAIN LOOP ##########

try:
	#Check flag file repeatedly
	while 1:
		doorfile = open('/var/www/door.txt','r+')
		doorcmd  = doorfile.read(2)
		
		#If flagged,
		#unflag and open door	
		if(doorcmd == '1'):
			doorfile.seek(0)
			doorfile.write('0')
			openDoor()

		doorfile.close()

except KeyboardInterrupt:
	pass

#Upon exiting script:
p.stop()
GPIO.cleanup()
doorfile.close()
