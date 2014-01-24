doorbot
=======
Raspberry Pi-powered dorm room door unlocker
Video: http://youtu.be/aq7At8ip24I

Doorbot is a project thought up and executed by two roommates at Tufts University: Riley Wood and Win Halelamien.
The basic idea is that unlocking your door with a key is time consuming and frustrating when you forget your key.
Doorbot allows you to open your door from any Internet-equipped device.

Doorbot is a project that combines a few different disciplines.
The first is the mechanical design: what kind of apparatus is needed to open the door in the first place?
We settled on a motor that reels in a string which is connected to a vicegrip clamped on the doorknob shaft.
As the motor reels in the string, the vice grip is pulled to the side, turning the knob and opening the door from the inside.
In this way, our door can always remain locked from the outside (so we will never accidentally leave it unlocked)
and Doorbot will let us in from inside the room when we ask it to.

The next task is to design the circuit to interface the Raspberry Pi with the motor.
This was done with a simple motor driver IC, specifically the TA8428KOS-ND from Toshiba.
A 9V power supply was used to supply power to the motors, and pins from the Raspberry Pi
controlled the power the motor driver supplied to the motor.
LEDs were also attached to other pins on the Pi to be used as indicators for when
Doorbot is reeling in versus when it is releasing the string.

The last challenge was the software for Doorbot. Doorbot's main functionality was written
in Python using the RPi library. This script checks if there is an unanswered request
for the door to be opened, and opens the door (i.e. runs the motor) if so, and then clears
that request. A request is denoted by a specific file, door.txt, containing a 1, and if there
is no pending request, it will read 0. The Python script repeatedly checks this file.
The use of a file as a flag allows for a very simply interface for triggering Doorbot. Any
application can modify that file (IOW write a 1 to the file) and Doorbot will see the change
and open the door in response. In this way, a lot of things can be used as input.

Currently, there are two methods of opening the door. The first to be implemented 
was a web server running on the Pi that hosts a PHP script that will modify the door.txt file
when the proper password is given via GET. The second is an RFID reader (specifically the
Parallax RFID Card Reader). A second Python script is continuously run on the Pi which waits
for a message from the RFID reader via serial. If the message contains a key listed in the keys.txt
file, the Doorbot flag will be triggered (i.e. door.txt will be written to).