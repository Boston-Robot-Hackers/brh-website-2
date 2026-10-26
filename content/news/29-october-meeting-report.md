---
date: 2026-10-26
excerpt: 'Arjun Viswanathan presented his Northeastern MS thesis on Husky-Beta, a legged-aerial
  robot that uses hierarchical reinforcement learning to decide when to walk and when
  to fly, and what it took to move the walking policy from simulation to hardware.'
highlight: true
image: images/news/boston-dynamics-spot.png
published_date: '2026-10-26'
title: 'October 15 Meeting Report: Reinforcement Learning for Multimodal Locomotion'
type: news
---

### Talk Overview

- **Reinforcement Learning for Multimodal Locomotion** — Arjun Viswanathan's MS thesis at Northeastern's Silicon Synapse Lab, presented by Arjun, who works on robot behavior at Boston Dynamics
- Husky-Beta is a legged-aerial platform for crossing rough terrain. The thesis addressed both learning to walk and choosing when to switch between walking and flight using hierarchical reinforcement learning.
- The talk covered the controller architecture, simulated terrain navigation, and the difficulties of transferring the walking policy to hardware.

### Husky-Beta: Robot Overview

- 18 DOF quadruped with propellers on knees, enabling walk/fly mode switching
- ~6 kg, built from carbon fiber and lightweight plastic for flight capability
- Actuators: Dynamixel servos (stronger at knee, weaker at hip joints)
- Onboard: Nvidia Jetson Orin, Cube Pilot flight controller with IMU, 22V LiPo (~15 min battery)
- Powered via voltage regulator; U2D2 bridges Orin to Dynamixels

### Control Architecture

- Walk controller: RL policy (PPO) with Raibert heuristic for footstep targets
  - Observes base state, joint positions, velocities, previous actions, contact schedule
  - Outputs joint position goals fed into a PD controller
- Flight controller: simple PD control on desired vs. actual acceleration
- Switching: originally motion mimic RL, simplified to direct joint-pose snapping for thesis scope
- High-level policy: hierarchical RL choosing walk/flight mode and velocity given terrain scans and goal pose

### Reinforcement Learning Approach (PPO)

- Actor-critic architecture: both networks update together
  - Actor outputs action distribution; critic outputs state value
- Rewards: velocity tracking, contact schedule, foot clearance, footstep target tracking
- Penalties: base height deviation, action jitter, undesired roll/pitch, high torque/power
  - Flight mode actively penalized to preserve battery; mode-switching penalized to prevent rapid toggling
- Critic gets privileged observations: true base position, time remaining to goal
  - Time budget prevents robot from stalling just short of goal to farm reward

### Raibert Heuristic

- Calculates foot placement from hip position, current velocity, desired velocity, and gait period
- Scales aggressiveness via user-tuned constant K
- Goal: keep robot within support polygon; speed up by stepping closer, slow down by stepping ahead
- No terrain awareness; designed for flat-ground hopping (Raibert, 1992)
- Used here as a thesis constraint; would have used pure RL otherwise

### Sim-to-Real Transfer and System Identification

- Base DC motor actuator model worked in sim but produced severe flailing on hardware
- Root cause: Dynamixel PWM-to-torque mapping is nonlinear, hard to model
- Ran sinusoidal SYSID (PACE method from ETH) to identify friction and armature parameters
  - Reduced error significantly but still off at higher frequencies
- Even after SYSID: foot position tracking remained poor; torque commands on hardware were ~half of simulation
- Leg compliance (unmodeled rigid-body assumption) also contributed to sim-to-real gap
- Verdict: Dynamixels poorly suited for RL force control; would switch to standard DC motors (e.g., Unitree Go2/G1) if starting over

### High-Level Policy Results and Edge Cases

- Terrain scans compressed via fully connected encoder (512 → 64 → 32) before feeding policy
  - Raw 200-500 point scans too redundant for network to extract useful features
- Edge case: robot defaulted to flight mode for entire traversal when flight penalty was too low
  - Fix: increase flight mode cost
- Edge case: robot oscillated near wall when obstacle threshold was too sensitive
  - Fix: reduce obstacle proximity threshold
- Successful behavior: robot learned to fly over walls and switch back to walk mode autonomously
  - Flight altitude above obstacles emerged without explicit reward; possibly energy-related

### Thesis Contributions and Limitations

- Contributions:
  - Footstep-tracking walk RL policy with domain randomization (friction, mass, disturbances)
  - Simple PD-based switching and flight controller
  - Terrain-aware hierarchical high-level policy
  - End-to-end sim-to-real infrastructure on Jetson Orin
- Known limitations:
  - No force control due to Dynamixel PWM nonlinearity
  - Rigid-body sim ignores leg compliance
  - High-level policy perception too narrow (misses alternate paths, dead ends)
  - No crossfade-based dynamic leg deployment for hardware flight transition
