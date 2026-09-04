---
title: "September 3 Meeting Report: Powering Robots"
date: 2026-09-04
image: "images/news/battery.png"
excerpt: "Alan Kilian spoke about power systems for robots: batteries, circuitry, motor controllers, processors, and graceful shutdown. Learn about voltage selection, battery chemistry, BMS, and EMI."
highlight: false
slides_pdf: "meeting-reports/22/slides.pdf"
type: news
---

## Meeting Summary

Alan Kilian, with decades of experience in software and hardware, shared practical insights on powering robots. The talk covered everything from battery selection through sensor integration and graceful shutdown.

**[Download Slides (PDF)](../meeting-reports/22/slides.pdf)** — Full slide deck with detailed references and sensor resources mentioned during the talk.

## Power Systems and Battery Selection

- Match battery voltage to the highest-load component to avoid unnecessary regulation
- Run high-power loads (motors, servos) unregulated directly off the battery
- More efficient to step voltage down than up; avoid boost converters where possible
- Higher voltage = lower current = thinner wires, smaller connectors, less loss
- Safe voltage ranges:
  - Up to 24V: safe to handle
  - 48V: potentially lethal under certain conditions
  - Recommended range for hobby/club robots: 12–24V

## Battery Chemistry and Cell Types

- Two main types for robotics: lithium ion (cylindrical cells) and lithium polymer (pouch cells)
  - **LiPo**: lighter, higher discharge rate, preferred for drones and weight-critical builds
  - **Li-ion**: more robust, slower self-discharge, better for stationary or long-idle robots
  - **Lithium iron phosphate (LiFePO4)**: safest, heavier, best for high-capacity or inhabited applications
- Old "memory effect" advice (discharge to 0% before charging) applies only to NiCd, not lithium
- Do not charge lithium cells below freezing: can damage cells
  - Smart batteries can self-heat before accepting charge

## Battery Management Systems (BMS)

- Required whenever cells are wired in series
  - Balances individual cell voltages during charge and discharge
  - Prevents overcharge, over-discharge, and overheating
- BMS can be built into the battery pack or split into the charger (common in quadcopters to save weight)
  - For most ground robots: buy a pack with integrated BMS
- Configurable parameters on better units: min/max voltage, charge rate, discharge rate, temperature limits
- Cell count notation: 2S, 3S, 4S (number of cells in series)
- Low-voltage detector (~$2) can trigger a graceful OS shutdown before the battery dies

## DC-DC Conversion

- Use a separate converter for each voltage rail needed (e.g., 3.3V, 5V, 12V)
  - Adjustable buck converters available for ~$5; set with a trim pot, lock with nail polish
- Three converter types:
  - **Buck**: steps voltage down
  - **Boost**: steps voltage up
  - **Buck-boost**: handles both (less efficient, more expensive)
- Can chain converters (e.g., 48V → 12V → 5V) to avoid costly wide-ratio converters
- Enable pins on converters allow individual rail shutdown for power saving or debugging
- Add fuses; useful for bench debugging and protecting against shorts

## Motors and Motor Controllers

- **Brushed DC**: simple, cheap, two wires, generates electrical noise; fine for most hobby use
- **Brushless DC (BLDC)**: three wires, higher power density, quieter, more complex driver
  - Identified by: three wires, or spinning outer case (outrunner)
- **Stepper motors**: four or six wires, square body, 200–400 steps/rev
  - Good for precise positioning without encoders; used in locomotion and arms
  - Step-and-direction interface simplifies software control
  - Dedicated stepper controllers (~$5–$15) handle acceleration profiles
- **Hobby servos**: three wires, PWM signal, 90–160° range, great mechanical mounting options
- **Smart servos** (e.g., Dynamixels): digital packet control, torque feedback, continuous rotation capable
- **Linear actuators**: brushed/brushless/stepper with lead screw; not back-drivable (good for clamping)
- **Transverse flux motors**: emerging direct-drive option, eliminates gearbox, better haptic feedback
- **Encoders** on any motor type give position feedback without full servo complexity

## Processors, Sensors, and Shutdown Practices

- Processor options by capability:
  - **Microcontrollers** (Arduino, ESP32): no OS, instant power-on/off, cheap
  - **Hybrid boards**: new Arduino with dual cores (one Arduino, one Linux) at similar cost to buying separately
  - **Raspberry Pi**: Wi-Fi, BLE, USB, more RAM; requires graceful shutdown
  - **Nvidia Jetson**: onboard GPU for AI/CV workloads; $400–$500, high power draw
  - **Mini PC / laptop**: full Linux or Windows, velcro-mount option, easy to monitor live
  - **Beaglebone**: has dedicated real-time co-processors on-die, good for time-sensitive tasks

### Graceful Shutdown is Critical

- Hard power cuts corrupt filesystems; can take weeks to manifest and diagnose
- Fanuc-style three-state (on / pause / off) useful for arm robots: pause stops motion, retains position
- Kill switches may be legally mandated in some regulated environments

### Sensor and EMI Considerations

- Sensor selection: match interface (Ethernet, I2C, PWM) to what the processor actually supports
- EMI is a real problem in scratch-built robots
  - PWM, ultrasonic sensors, Bluetooth, USB 3.0 can all interfere with each other
  - USB 3.0 is a known Wi-Fi/BT killer if unshielded
  - Buying tested kits avoids many mysterious noise issues
- Programming small microcontrollers: C/C++ or MicroPython via JTAG, serial port, or DFU (drag-and-drop flash)

## Key Takeaways

- **Design for efficiency**: match voltage rails to load, step down rather than up
- **Battery management matters**: proper BMS, correct chemistry, and protection circuits prevent damage and danger
- **Motor choice drives system complexity**: match motor type to your positioning needs and power budget
- **Graceful shutdown prevents corruption**: critical for any system with a filesystem
- **EMI is real**: careful layout and shielding save debugging time

## Thanks

Thanks to Alan for a comprehensive and practical talk that covered both theory and real-world considerations. Special thanks to all attendees for questions and discussion.
