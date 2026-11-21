---
title: What you will need
summary: In this section we enumerate what is required to be part of this program. It mentions the robot itself, the software and the hardware
order: 1
---

### Makers Pet - Required

To be a full participant in the Build-a-ROSBot program you are required to have a ["Arduino/ROS2 Self-Driving Robot 120mm Build Pack"](Arduino/ROS2 Self-Driving Robot 120mm Build Pack). As you see there are multiple configurations. You need to get the one with the LIDAR. You can decide which set up for the battery to get.

### ROS2 "Computer"

There are several ways to go here and each is a little different. As background, ROS2 is a "distributed operating system". Sort of. It's not really an Operating System in the traditional sense of the word. But it is distributed.

It is typical that your ROS2 "application" will have interconnected components running on multiple computers. In the case of Makers Pet, there will be a little bit of ROS2 on the robot itself and a lot more of it on your computer. There's no way around it given the hardware and the way ROS2 works.

There are several options here. No matter what option you pick, the computer needs to be relatively new, and have at least 8 but preferably 16 Gig of memory. At at least 32 but preferably 50Gig of free disk space. The low ends of these ranges will work but will be slow. 

Here are the possible scenaraios:

1. Linux Computer: a laptop or other computer running Ubuntu 24.04. I do not think any of us will have this set up but it is the default ideal. We are sure this will work.

2. MacOS running a VMWare VM, with Ubuntu 24.04 installed. That works excellent as well

3. Windows or Mac running [Pixi for Robotics](https://pixi.prefix.dev/latest/robotics/)/ We have tried it and it seems to work. It does need more validation.

4. Windows running ROS om WSL. This is supposed to work but none of us has tested it.


### ROS2 development Environment

To be a full participant in the Build-a-ROSbot program, you need a development environment running ["ROS2 Jazzy"](https://docs.ros.org/en/jazzy/index.html). "Jazzy" is the version "number". It is fairly recent but not the latest. Still that is what we will use because that is what the Makers Pet requires. Don't worry, ypu will probably not be able to tell the difference.


