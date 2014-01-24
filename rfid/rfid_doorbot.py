import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

port = "/dev/ttyAMA0"
rfid_en = 12	#Pin number

rfid = serial.Serial(port, 2400, timeout=0.5)
GPIO.setup(rfid_en,GPIO.OUT)
GPIO.output(rfid_en,GPIO.LOW)

while True:
	acceptedKeys = open('/home/pi/rfid/keys.txt','r').read().splitlines()
	key = rfid.read(12).strip()
	if len(key) != 0 and (key in acceptedKeys):
		doorfile = open('/home/pi/door.txt','r+')
		doorfile.write('1')
		doorfile.close()
