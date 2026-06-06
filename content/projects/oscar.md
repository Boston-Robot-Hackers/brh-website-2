---
title: Oscar
date: 2000-01-01
status: Retired
image: images/projects/oscar.jpg
text: Tabletop robot
lead: Alan Kilian
members: 1
excerpt: I wanted a tiny robot for my office desktop
---

### Software
Software Development Environment/Methods: I wrote the original code in Motorola Assembly, and then used the Imagecraft icc11 'C' compiler to rewrite the code. It all fits into about 500 bytes, although it is quite a simple robot right now.

<img src="../images/projects/oscar.jpg" alt="Sample image" style="float: left; margin: 25px 25px 25px 25px; border-radius: 8px; height: 250px;">

### Hardware
* Controller: Motorola MC68HC11E2
* Two downward looking IR to detect the edge of the table.
* Two mechanical switch 'Whisker' bump switches. The IR sensors are mounted to the end of the bump switch arms. 
* Four CdS cells mounted around the dome for ambient light detection. 
* Battery Voltage detection.
* Actuators: Two four-phase 45-degree stepper motor/gearbox driving the wheels.
* Height, width, length: 4 Inches diameter, 4 Inches tall
* Weight: A couple of pounds.
* Power source: Nicad 12-volt
* Speed: Slow. About 1 Inch per second or less.


### Construction history: 

I was at the local electronic surplus shop, and they had these GREAT colored plastic domes that I just had to make a Robot out of. I left that dome on my desk for over two years while I slowly added other components to the pile that would fit the dome. 

<img src="../images/projects/oscar1.jpg" alt="Sample image" style="float: right; margin: 25px 25px 25px 25px; border-radius: 8px; height: 250px;">

I found two Litton stepper motors with a 45 degree-per-step motor attached to a gear reduction box that made almost one step-per-degree at the output shaft. The motors EXACTLY fit back-to-back under the dome. I then used a hacksaw to chop off both ends of a Miniboard so that I could fit it under the dome also. I removed the serial connectors at one end, and the Motor LEDs and connectors from the other end. Then I bought a Sherline Lathe and Mill so that I could mill up some aluminum parts to hold the motors, and some aluminum rims with setscrews so that I could mount some model airplane wheels. I had a tiny robot!!!

#### Operational description: 

Oscar is supposed to modulate the downward looking IR detectors to see if there is a table under it, and avoid falling off. I would also like it to find a charging station, and recharge. I can charge the Nicads from an external charging jack, and I can also switch the Nicads out of the circuit and power the robot from the external supply in case the Nicads are completely dead. He currently draws "Spirograph" like designs by dragging colored markers around while driving on a sheet of paper. It's a very simple program like this to draw a square:
```
while (1) {
    forward(100);
    clockwise(90);
    forward(100);
    clockwise(90);
    forward(100);
    clockwise(90);
    forward(100);
    clockwise(90);
}
```
Of course the details are in the functions forward() and clockwise().