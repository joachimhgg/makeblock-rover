#!/usr/bin/python
# coding=utf-8
# This code is an example using Tkinter to control the mouvement of the rover 
#INSTRUCTION :
#open a terminal and launch nc -l 8001 to listen the socket and show the values.
#open another terminal and launch Mouvement_tkinter_guy.py

from Tkinter import *
import tkMessageBox
import HW_Thread_py36 as HWT
import serial
import sys
import time
import socket

def Action(mvt):
	hw.write_HW("M," + mvt + ",50.")
	time.sleep(0.1)
	print(mvt)
def Stop(event):
	hw.write_HW("M,.")
	time.sleep(0.1)
	print("Stop")

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
sock.connect(('127.0.0.1', 8002))
value=""

#when class gets data from the Arduino, it will call the my_callback function
hw.register_callback(my_callback)
print("Python Serial communication for MegaPi Pro connected")


#######################TKINTER#######################

window = Tk()
window.title("Makeblock example for Tkinter and rover mouvement")
window.geometry('350x200')

tkMessageBox.showinfo('Makeblock welcome','This example shows how you can control the robot using Tkinter Gui !')

lbl = Label(window, text="Rover control")
lbl.grid(column=0, row=0)

btnF = Button(window, text="🡅")#, command=lambda:Action('F') )
btnF.bind('<ButtonRelease>', Stop)
btnF.bind('<ButtonPress-1>', lambda event:Action('F'))
btnF.grid(column=1, row=2)

btnB = Button(window, text="🡇")
btnB.bind('<ButtonRelease>', Stop)
btnB.bind('<ButtonPress-1>', lambda event:Action('B'))
btnB.grid(column=1, row=3)

btnR = Button(window, text="🡆")
btnR.bind('<ButtonRelease>', Stop)
btnR.bind('<ButtonPress-1>', lambda event:Action('R'))
btnR.grid(column=2, row=3)

btnL = Button(window, text="🡄")
btnL.bind('<ButtonRelease>', Stop)
btnL.bind('<ButtonPress-1>', lambda event:Action('L'))
btnL.grid(column=0, row=3)

window.mainloop()



