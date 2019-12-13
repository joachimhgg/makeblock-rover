#!/usr/bin/python

import HW_Thread_py36 as HWT
import serial
import sys
import time
import socket

#INSTRUCTION :
#open a terminal and launch nc -l 8001 to listen the socket and show the values.
#open another terminal and launch python control_example.py

def my_callback(response):
    global value
    """example callback function to use with HW_interface class.
     Called when the target sends a byte, just print it out"""
    if response != '.':
     #the value has to be something like 40,50. to have ListValue[0] = 40  and ListValue[1] =50
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
print("Python Serial communication for MegaPi Pro")

while(1):
    sys.stdout.flush()
    cmd = raw_input('--> ')
    sys.stdout.flush()
    hw.write_HW(cmd)



