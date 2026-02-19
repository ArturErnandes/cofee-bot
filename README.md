# Gesture-Based Coffee Delivery System

## Problem Statement
In a coworking environment, users may need a fast and frictionless way to request coffee without interacting with a mobile application, a terminal, or approaching the coffee machine. The solution must support a hands-free request method (via a predefined gesture), automatically initiate coffee preparation, dispatch a delivery robot to the user, and return the robot to its base after completion.

---

## Proposed Solution
The proposed system consists of four core components operating as an integrated pipeline:

1. **Camera** — captures and streams video to the server  
2. **Server** — performs gesture recognition, triggers coffee preparation, computes routes, and issues robot control commands  
3. **Coffee Machine** — prepares/pours coffee upon receiving a server signal  
4. **Robot** — executes delivery and return actions according to the server commands

---

## Implementation

### 1) Hardware/Network Architecture (KTS)
This diagram provides a high-level view of the physical components and their connectivity.

![Hardware/Network Architecture (KTS)](readme_imgs/KTS.jpg)

---

### 2) Use-Case Diagram (Component Responsibilities)
This diagram outlines the supported functions for each component: Camera / Server / Coffee Machine / Robot.

![Use-Case Diagram](readme_imgs/use-case-schema.png)

---

### 3) Sequence Diagram (End-to-End Workflow)
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

![Sequence Diagram](readme_imgs/sequence-schema.png)

---

### 4) Conceptual Model (UML Class Diagram)
This diagram captures the key entities and relationships: the camera streams video to the server; the server issues control commands to the robot and the coffee machine.

![Conceptual Model](readme_imgs/concept-model.png)

---

## System Components (Summary)
- **Camera**: record video; stream video to the server  
- **Server**: gesture recognition; coffee-machine signaling; route planning; robot start/return commands; arrival tracking  
- **Coffee Machine**: pour coffee  
- **Robot**: move forward/backward; turn right/left  

---

## Minimum Requirements
- A camera capable of providing a stable video stream (IP/USB)
- A server capable of real-time video processing and gesture recognition
- A controllable coffee machine interface (API/controller)
- A controllable robot interface (API/controller)

---