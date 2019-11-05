.. _refRPIcom:

Communication between Raspberry pi and MegaPi
*********************************************

This part explains you how etablish a simple comunication between Python (RPI) and Arduino C (Makeblock boards) using Pyserial
and how works this simple communication in order to setup new capabilities.

Basic working of the communication
==================================

First we will see how to adapt and run an example for RPI and Makeblock boards communication.

Requirement
-----------

* basic knowledge of Arduino
* nasic knowledge of Linux command (cd, ls, use of tab key for auto-completion)

Set-up the communication
------------------------

Arduino configuration
^^^^^^^^^^^^^^^^^^^^^

* Open *~/Documents/control_rover1.0/control_rover1.0.ino* in Arduino IDE. From ssh (see the :ref:`refSSH` topic), you can do ``arduino control_rover1.0.ino`` but it could be slow.
This is the Arduino code to process what Python part are sending.

* Depending on the type of board you're using, you need to modify the header file to match.

For example, if you're using a mCore. You should change ``#include <MeOrion.h>`` to ``#include <MeMCore.h>`` Corresponding boards and there header file are:

*Orion <> MeOrion.h ; BaseBoard <> MeBaseBoard.h ; mCore <> MeMCore.h ; Shield <> MeShield.h ; Auriga <> MeAuriga.h ; MegaPi <> MeMegaPi.h*

* for the moment, you just have to change the port and objects' name depending of your board (MeMegaPiDCMotor..). To find the good one, try motor example by clicking on File/Examples/makeblock-librairies-master
but keep the sames names (motor1...).

.. highlight:: arduino
   :linenothreshold: 5

.. code-block::
  :emphasize-lines: 2,7,8,9,10,11

  #include <SoftwareSerial.h>
  #include "MeMegaPiPro.h" //Insert here your makeblock boards.

  MeSmartServo mysmartservo(PORT5);   //UART2 is on port 5 //You can keep this even if you don't have the SmartServo

  //material declarations,
  MeMegaPiDCMotor motor1(PORT1B); //right front wheel
  MeMegaPiDCMotor motor2(PORT2B); // right back wheel
  MeMegaPiDCMotor motor3(PORT3B); // left front wheel
  MeMegaPiDCMotor motor4(PORT4B); // left back wheel
  MeRGBLed led(PORT_9); //You can keep this even if you don't have the module

* Connect your makeblock board at your Raspberry PI thanks to a USB-B cable and upload your code. The most harder is done ! If you have a problem don't hesitate to create a github issue (see :ref:`refSupport`)

launch Python-Arduino communication example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. On a terminal :
  the *control_example.py* uses sockets to send datas (providing by sensors,etc. i.e. by Arduino). Like this you can receive data in another PC (by changing ``sock.connect(('127.0.0.1', 8001))
``). For this example, we just show the values in another terminal. Write :

.. code-block::

   nc -l 8001

2. On another terminal :

* activate *comRPI* virtual environment (see :ref:`refPyenv`)

.. code-block::

  workon comRPI

PySerial is already installed on this virtual environment moreover if you want to create another venv you can ``pip install pyserial`` after activate your new venv.

Check on Arduino IDE that you have the good portname. You can see the "Serial Port" entry in the Arduino "Tools" menu
if it's not ``/dev/ttyUSB0``, edit control_example.py (using nano ou Gedit) and change the value of ``portname`` by the good one.

* Finaly write :

.. code-block::
  (comRPI) makeblock@makeblock-desktop: cd ~/Documents/RoverExamples/Python-Arduino-example
  (comRPI) makeblock@makeblock-desktop: python control_example.py

How to setup a new protocol of communication
============================================
