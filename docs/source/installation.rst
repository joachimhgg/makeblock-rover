Installation
************

To install the environment on your Raspberry Pi, it's really simple.

Requirement
===========

* a computer with an SD slot or equivalent.
* **Raspberry Pi 2 or higher** (the ISO has been testing with Raspberry Pi 3B+)
* **Makeblock board** based on Arduino (Orion, BaseBoard, mCore, Shield, Auriga, MegaPi)
* **8 Gb SD card minimum** (but at least 16 GB is recommanded)
* basic knowledge of Arduino

Installation steps
==================

1. Download the `ISO file`_ in the github project.
  .. _ISO file: https://github.com/joachimhgg/makeblock-rover
2. Download `Balena Etcher`_ for Linux, Windows or macOS, a easy tool to flash ISO image on SD card.
  .. _Balena Etcher: https://www.balena.io/etcher/
3. Open Balena Etcher software, select the ISO image downloaded, select your SD card and flash !
4. Insert the SD card into the RPI
5. connect your keyboard, mouse and hdmi screen to your RPI and connect the power cable.
6. Set-up your wifi (or ethernet) connection.
7. Open a terminal and launch::
  makeblock@makeblock:~$ sudo apt-get update
  makeblock@makeblock:~$ sudo apt-get upgrade

**Note:  The root password of the environnment is "mb".**

8. You can now start to develop robotics projects !
