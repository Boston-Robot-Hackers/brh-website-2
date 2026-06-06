---
title: Trippy
date: 2000-01-01
status: Retired
image: images/projects/trippy.jpg
text: Trippy Holonomic robot
lead: Alan Kilian
members: 1
excerpt: A holonomic robot based on the Killough platform used for my Mechatronics BS degree from the U of Minnesota.
---
<img src="../images/projects/trippy.jpg" alt="Sample image" style="float: right; margin: 25px 25px 25px 25px; border-radius: 8px; height: 450px;">

### Software

Micrium micro C/OS-II RTOS in C.

### Hardware

* Purpose: I saw a Lego robot like this and I wanted one also.
* Controller: Mini Robo Mind from Robominds Motorola MC68332 processor.
I am using the PIC-SERVO PID motion controllers from J R Kerr for doing the motion control of the three motors.

* Software Development Environment/Methods: I have a forward kinematic simulator based on some equations that the local Math guy came up with so I can enter in the speeds of the three motors, and see how the platform would move.

* I can compile C programs using GCC on a RedHat Linux box and download to the FLASH on the MRM.
I am using the motorobots library also.
* Sensors: Rate gyro from hobby airplane. Dinsmore 1525 analog compass, Gyration MG100 rate gyro.
* Actuators: Three holonomic wheel platform.
* Height, width, length: About 10 Inches diameter and 10 Inches tall
* Weight: Several pounds.
* Power source: Two Makita NiCd 9.6 Volt packs with 5 Volt regulator.
* Speed: Pretty slow. Maybe 0.5 Feet-per-second?
* Construction history: See: Trippy progress page at: http://bobodyne.com/web-docs/robots/Trippy/index.html

