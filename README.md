# Gesture-Based Coffee Delivery System

## Problem
In a coworking environment, users may need a fast and frictionless way to request coffee without interacting with a mobile application, a terminal, or approaching the coffee machine. The solution must support a hands-free request method (via a predefined gesture), automatically initiate coffee preparation, dispatch a delivery robot to the user, and return the robot to its base after completion.

## Solution
The proposed system consists of four core components operating as an integrated pipeline:

1. **Camera** — captures and streams video to the server  
2. **Server** — performs gesture recognition, triggers coffee preparation, computes routes, and issues robot control commands  
3. **Coffee Machine** — prepares/pours coffee upon receiving a server signal  
4. **Robot** — executes delivery and return actions according to the server commands


## Technical systems complex
This diagram provides a high-level view of the physical components and their connectivity.

<img src="readme_imgs/KTS.jpg" alt="Hardware/Network Architecture (KTS)">

## Use-Case diagram
This diagram outlines the supported functions for each component: Camera / Server / Coffee Machine / Robot.

<img src="readme_imgs/use-case-schema.png" alt="Use-Case Diagram">

## Diagram of precedent sequences
The following steps represent the nominal operational workflow:

1. Camera → Server: stream video  
2. Server: recognize the predefined gesture  
3. Server → Coffee Machine: send a “pour coffee” command  
4. Server: compute a route to the user  
5. Server → Robot: send a “start delivery” command  
6. Robot: perform motion actions (move/turn)  
7. Server: detect robot arrival  
8. Server: compute a return route to the base  
9. Server → Robot: send a “start return” command  
10. Robot: perform motion actions (move/turn)

<img src="readme_imgs/sequence-schema.png" alt="Sequence Diagram">

## Conceptual model
This diagram captures the key entities and relationships: the camera streams video to the server; the server issues control commands to the robot and the coffee machine.

<img src="readme_imgs/concept-model.png" alt="Conceptual Model">

## Class Diagram

<img src="readme_imgs/uml.png" alt="Class Diagram">