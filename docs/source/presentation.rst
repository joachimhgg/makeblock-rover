Tools & Softwares
*****************

In order to give you a ready-to-start RPI environment for Education, some packages has been installed to start without the needs to spend long time of installation.
To install more packages go to the `raspberry pi education website`_ or `snap store`_.



.. _raspberry pi education website: https://www.raspberrypi.org/education/
.. _snap store: https://snapcraft.io/store

Tools and packages installed
============================

* Ubuntu Mate 16.04
* Arduino with Makeblock librairies (open port access + choose Mega 2560 board)
* Python 2.7 and 3.5
* ROS Kinetic
* Ros-kinetic-rosserial-arduino
* Ros-kinetic-rosserial
* Ros-kinetic-usb-cam
* Ros-kinetic-web-video-server
* Gedit
* Git
* Scratch
* Open CV 3.1.1
* ...

.. _refSSH:

Working in SSH
==============

You can work on SSH from your linux PC. For that,

1. Open a terminal on RPI and write:
::
  Makeblock@makeblock:~$ hostname -I

It gives you the IP of your RPI.

2. open a terminal from your PC and write:
::
  yourPC@yourPC:~$ ssh makeblock@IPofraspberrypi

or to be able to open graphics interfaces (such as Arduino IDE)::

  yourPC@yourPC:~$ ssh -X makeblock@IPofraspberrypi

Realising projects in Arduino C
===============================

Arduino IDE is installed with Makeblock librairies. So, you can start by coding your first project using the IDE in Arduino C!
Each time you want to experiment a new Makeblock sensor, you should open an Arduino IDE and try the examples.

.. image:: /images/arduino_gedit_example.png

Realising projects in Python
============================

.. image:: /images/gedit.png

.. _refPyenv:

Configure a Python virtual environment
--------------------------------------

I recommend you to create a virtual environment for each python projects.
If you aren’t familiar with virtual environments, please take a moment look at `this article`_ on RealPython.

.. _this article: https://realpython.com/python-virtual-environments-a-primer/

You should use virtualenvwrapper as this package purposes simple commands to use virtual environment.
To create an virtual environment, open a terminal (CTRL+ALT+T) and launch::

  mkvirtualenv myproject -p python3

You can (and should) name your environment(s) whatever you’d like.

Then you can use workon, the workon command is part of the virtualenvwrapper package
and allows us to easily activate virtual environments.

::

  workon myproject

.. image:: /images/workon.png

and if you want to go out your environment::

  deactivate

Finaly you can install your project's packages and launch your .py file in this isolate emvironment::

  (myproject) makeblock@makeblock:~ $ pip install numpy
  (myproject) makeblock@makeblock:~ $  python myprojectExample.py


**Notes :**

* environments are created in ~/.virtualenvs
* if you want to remove an environment you can write ``rmvirtualenv ENVNAME``
* check other commands on the `virtualenwrapper documentation`_

.. _virtualenwrapper documentation: https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html

Interfacing between Python and Makeblock boards
-----------------------------------------------

Please see :ref:`refRPIcom` .

Realising projects in ROS
=========================

ROS Kinetic installed on the OS. If you want to develop projects using ROS, please check the :ref:`refExample` .
