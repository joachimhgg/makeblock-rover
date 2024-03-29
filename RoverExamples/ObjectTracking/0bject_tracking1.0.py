#!/usr/bin/python
'''
Object detection and tracking with OpenCV
    ==> Turning the ME_RGB_LED module on detection and
    ==> Printing object position Coordinates 

    Based on original tracking object code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/

Developed by Joachim Honegger - Makeblock j.honegger@makeblock.com 10/19 
'''

from __future__ import print_function
from imutils.video import VideoStream
import imutils
import time
import cv2
import HW_Thread_py36 as HWT
import serial
import sys
import time
import socket


#INSTRUCTION :
#open a terminal and launch nc -l 8001 to listen the socket and show the values.
#open another terminal and launch python control_example.py

panServo = 1
tiltServo = 2

#position servos 
def positionServo (servo, angle):
	hw.write_HW("S," + str(servo) + "," + str(angle) + ",100.")
	print("[INFO] Positioning Makeblock servo at {0} to {1} degrees\n".format(servo, angle))

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 220):
        panAngle += 3
        if panAngle > 180:
            panAngle = 180
        positionServo (panServo, panAngle)
 
    if (x > 280):
        panAngle -= 3
        if panAngle < -180:
            panAngle = 180
        positionServo (panServo, panAngle)

    if (y < 160):
        tiltAngle -= 3
        if tiltAngle < 0:
            tiltAngle = 0
        positionServo(tiltServo, tiltAngle)
 
    if (y > 210):
        tiltAngle += 3
        if tiltAngle > 100:
            tiltAngle = 10
        positionServo (tiltServo, tiltAngle)

        
def my_callback(response):
    global value
    """example callback function to use with HW_interface class.
     Called when the target sends a byte, just print it out"""
    if response != '.':
     #the value has to be something like 40,50. to have ListValue[0] = 40  and ListValue[1]=50
	    value = value + response
    else :
        ListValue = value.split(',')
        inform = "("
        for val in ListValue:
            inform += val + ";"
        inform += ")\n"   
        sock.send(inform)
        
        value = ""
    	#print(response)


  # Need to set the portname for your Arduino serial port:
  # see "Serial Port" entry in the Arduino "Tools" menu
portname = "/dev/ttyUSB0"
portbaud = "115200"
ser = serial.Serial(portname,portbaud,timeout=0, write_timeout=0)
# timeout=0 means "non-blocking," ser.read() will always return, but
# may return a null string. 
print("opened port " + portname + " at " + str(portbaud) +  " baud")

sys.stdout.flush() 
hw = HWT.HW_Interface(ser,0.1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8001))
value=""

#when class gets data from the Arduino, it will call the my_callback function
hw.register_callback(my_callback)
print("Python Serial communication for MegaPi Pro connected")
        
# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
vs = VideoStream(0).start()
time.sleep(2.0)

# define the lower and upper boundaries of the object
# to be tracked in the HSV color space
colorLower = (16, 100, 100)
colorUpper = (36, 255, 255)

# Start with LED 1
hw.write_HW("L,1,50,50,50.")
ledOn = False

# Initialize angle servos at 90-90 position
global panAngle
panAngle = 80
global tiltAngle
tiltAngle =20

# positioning Pan/Tilt servos at initial position
time.sleep(0.05)
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

# loop over the frames from the video stream
while True:
	# grab the next frame from the video stream, Invert 180o, resize the
	# frame, and convert it to the HSV color space
	frame = vs.read()
	frame = imutils.resize(frame, width=1000)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the object color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			# position Servo at center of circle
			mapServoPosition(int(x), int(y))
			
			# if the led is not already on, turn the LED on
			if not ledOn:
				ledOn = True
				print(ledOn)
				time.sleep(0.1)
                                hw.write_HW("L,1,64,0,0.")

	# if the ball is not detected, turn the LED off
	elif ledOn:
		ledOn = False
		print(ledOn)
		time.sleep(0.1)
		hw.write_HW("L,1,0,0,0.")
		

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	
	# if [ESC] key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
            break

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
positionServo(panServo, -50)
positionServo(tiltServo, 20)
cv2.destroyAllWindows()
vs.stop()


