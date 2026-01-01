---
title: "Meeting announcement for January 8 2026 - URDF and Vibe Coding"
date: 2025-12-14
image: "images/leo-1.png"
excerpt: Speakers for March, April and June 2026
highlight: true
type: news
---
## Our Next Meeting

* When: January 8 2026 at 7:00 to 9:00pm
* Where: [Artisans Asylum](https://www.artisansasylum.com) (96 Holton Street, Boston, MA 02135))
* Register: [Register](https://brh.eventbrite.com)

**We hope that you will join us for our next meeting.**

## Agenda

* 7:00 Mingle, network, show and tell
* 7:30 Lightning Talks
    * Please send me ideas
* 7:45 Featured Speaker: Pito Salas, URDF and Vibe Coding 
* 8:30 Q&A and Open Discussion
* 9:00 End of formal meeting

## URDF and Vibe Coding

URDF is the Unified Robot Description Format — it's an XML based format used in ROS (and other places) to describe a robot's physical structure, including its links, joints, visual geometry, collision properties, and inertial parameters. The data in a URDF file is used if various scenarios, including simulation, rendering it in RVIZ and elsewhere, doing coordinate transformations and more. 

The problem with it is that URDF (and XML) is not especially user friendly - good for computers and bad for people. URDF files can go hundreds of inscrutable lines and are overwhelming and tricky to write and maintain.

After introducing URDF and explaining what I think are the key concepts and non-obvious aspects of it I will show two ways that I have used to deal with the complexity. One is using AI (that is LLMs, that is vibe coding, that is Claude.ai) to read, write, correct and check URDF. It’s pretty magical.

The second is kind of a research project that I undertook to design and validate a couple of possible ways to more directly address the complexity. I will show some ideas for a DSL (domain specific language) version of URDF, and what is good and bad about it. And I will show a Python library I created to generate valid URDF, and again what is good and bad about it.

