#!/usr/bin/python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#  HW_Thread.py
#  Classes for communication with asynchronous hardware
#  written by Jonathan Foote jtf@rotormind.com 3/2013
#  Updated for Python 3.6 by Jonathan Foote  3/2019
#  Modified for Makeblock by Joachim Honegger
#  j.honegger@makeblock.com 10/2019
#
# -----------------------------------------------------------------------------
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as  as published 
# by the Free Software Foundation http://www.gnu.org/licenses/gpl-2.0.html
# This program is distributed WITHOUT ANY WARRANTY use at your own risk blah blah
from __future__ import print_function

import time
import sys
import threading



class GetHWPoller(threading.Thread):
  """ thread to repeatedly poll hardware
  sleeptime: time to sleep between pollfunc calls
  pollfunc: function to repeatedly call to poll hardware"""

  def __init__(self,sleeptime,pollfunc):

    self.sleeptime = sleeptime
    self.pollfunc = pollfunc
    threading.Thread.__init__(self)
    self.runflag = threading.Event()  # clear this to pause thread
    self.runflag.clear()
    # response is a byte string, not a string
    self.response = b''

  def run(self):
    self.runflag.set()
    self.worker()

  def worker(self):
    while(1):
      if self.runflag.is_set():
        self.pollfunc()
        time.sleep(self.sleeptime)
      else:
        time.sleep(0.01)

  def pause(self):
    self.runflag.clear()

  def resume(self):
    self.runflag.set()

  def running(self):
    return(self.runflag.is_set())


class HW_Interface(object):
  """Class to interface with asynchrounous serial hardware.
  Repeatedly polls hardware, unless we are sending a command
  "ser" is a serial port class from the serial module """

  def __init__(self,ser,sleeptime):
    self.ser = ser
    self.sleeptime = float(sleeptime)
    self.worker = GetHWPoller(self.sleeptime,self.poll_HW)
    self.worker.setDaemon(True)
    self.response = None # last response retrieved by polling
    self.worker.start()
    self.callback = None
    self.verbose = True # for debugging

  def register_callback(self,proc):
    """Call this function when the hardware sends us serial data"""
    self.callback = proc
    #self.callback("test!")

  def kill(self):
    self.worker.kill()


  def write_HW(self,command):
    """ Send a command to the hardware"""
    self.ser.write(command)
    self.ser.flush()


  def poll_HW(self):
    """Called repeatedly by thread. Check for interlock, if OK read HW
    Stores response in self.response, returns a status code, "OK" if so"""

    response = self.ser.read(1)
    if response is not None:
      if len(response) > 0: # did something write to us?
        response = response.strip() #get rid of newline, whitespace
        if len(response) > 0: # if an actual character
          if self.verbose:
            self.response = response
          if self.callback:
            #a valid response so convert to string and call back
            self.callback(self.response.decode("utf-8"))
        return "OK"
    return "None" # got no response






