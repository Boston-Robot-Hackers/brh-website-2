---
title: Dome ROBOT
date: 2025-08-01
status: initial testing
image: images/projects/dome.png
text: Dome!
lead: Pito Salas
members: 1
github: https://github.com/campusrover/dome
excerpt: A small simple differential drive robot built from scratch with no external help. Built with ROS2 and Linorobot2
---
A small simple differential drive robot. This is a third generation of robots that I built at Brandeis. What's different is that I had no help, I built it all with my own two hands (more or less). 

### Software

[ROS2 Jazzy](https://docs.ros.org/en/jazzy/index.html). I am using the Linorobot2 package of code and instructions which I highly recommend. There is a [fork of Linorobot2](https://github.com/hippo5329/linorobot2) that supports ESP32. On top of that is [my own code and configuration](https://github.com/campusrover/dome).

### Hardware

As mentioned it is a simple differential drive robot. For compute there is a Raspberry Pi 4B+ which is connected by USB to an ESP32 processor. The processor is on the Waveshare General Driver For Robots which is a handy development board that has a bunch of features. The ones I use are the ESP32, IMU, Power management and Motor Controllers.

<img src="../images/projects/dome.png" alt="Sample image" style="float: left; margin: 20px 20px 20px 0; border-radius: 8px; height: 250px;">

Viewed from above, there are two circular plates made from clear acrylic. One interesting idea I am playing with is that there is a grid of holes on 25mm centers across the whole circular plate. Anything mounted on the robot gets a 3d-printed adapter which has 25mm center holes as well as accurate holes or other brackets depending on the device. This applies to the raspberry Pi, the WaveShare board, the Lidar, but also the battery holder, the little control panel and more.

<img src="../images/projects/caster.jpeg" alt="Another sample image" style="float: right; margin: 0 0 20px 20px; border-radius: 12px; height: 250px">

I went nuts with 3d Printing. I couldn't find a caster just the right side so I made this one. It is all 3d printed, and has two ball bearings. It works beautifully, at least so far, indoors. And the really nice thing is that if I need to change its height a little (which I do) I can just 3d Print a new part.