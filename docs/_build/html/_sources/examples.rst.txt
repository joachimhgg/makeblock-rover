.. _refExample:

Examples
********

Description
===========

Somes examples have been done to help you to start with Raspberry Pi, Ubuntu, OpenCV, ROS and Kinect360 with Makeblock boards.

CameraTesting
-------------

[Image]

Python-Arduino-example
----------------------

ObjectLedDetection
------------------

[Image]

ObjectTracking
--------------

Kinect360_projects
------------------

[Image]

ROS examples
------------

[Image]
[Image]


First try
=========

To launch the examples, follow this method :

press CTRL+ALT+T to open a terminal, press enter to launch a command.

The different example send the information/state of the robot by sockets. So before to launch an example you have to launch a terminal to listen the port by writing :

TERMINAL 1 :

.. code-block:: console

  nc -l 8001

or for the Mouvement_tkinter_gui example :

.. code-block:: console

  nc -l 8002

then press CTRL+ALT+T to open another terminal
TERMINAL 2 :
write (use tab for autocompletion):

.. code-block:: console

  cd Documents/RoverExamples/
  ls

Like this you can see all the example coded for the Rover.
Continue by writing :

.. code-block:: console

    source ~/.profile
    workon cv
    cd Mouvement_tkinter_gui
    python Mouvement_tkinter_gui.py

Each time you close the program, you have to listen the port again (nc -l 8001).

You can see and edit the code by using gedit (as example):

.. code-block:: console

  (cv) makeblock@makeblock-deskop:~/Documents/RoverExamples/ObjectLedDetection$ gedit Object_LED_detection_coordonates.py
