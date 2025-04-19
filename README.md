[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/NJLWAR4a)

![Docs Added](https://github.com/edl-iitb/edl-25-project-submission-edl25_mon13/actions/workflows/classroom.yml/badge.svg)

<!-- DON'T MODIFY ANYTHING ABOVE -->

<!-- Modify from here -->
# EDL 2025 Project Submission Repository

## Project Overview

### Project Name: P08 - Wall/Glass Pane Cleaning Drone
### Team Number: MON-13
### Team Members:
| Name            | Roll No  |
|-----------------|----------|
| Aagam Shah      | 22B1201  |
| Adit Srivastava | 22B1269  |
| Jainam Ravani   | 22B1242  |
| Jay Mehta       | 22B1281  |
| Kshitij Vaidya  | 22B1829  | 

<!-- ### Problem Statement and Solution: -->

## Problem Statement 
1. Build an aerodynamically stable drone for cleaning high-rise building windows.  
2. Ensure it can withstand windy conditions and recoil from high-pressure water spraying.  
3. Carry sufficient water to clean multiple windows.  
4. Operate safely in both manual and autonomous modes.  

## Proposed Solution

Our system consisted of a water spraying mechanism integrated with a baseline drone model. The spraying mechanism comprises of an onboard pump capable of ejecting water at 3L/min, which when coupled with our chosen nozzle suffices to clean dust and grime from glass surfaces, and a water tank that can either store enough water for the mission or utilize a continual water supply from a ground pump.

### Hardware Design Choices

In order to sustain the additional payload, we used an S550 hexacopter frame; the specs of various components including the BLDC motors and propellers were decided so as to achieve stable hover at 50% throttle. Pixhawk Cube flight controller equipped with PX4 Autopilot was used for regulating motor speeds to achieve a controlled flight. Various flight modes of the PX4 Autopilot were used to achieve manual as well as semi-autonomous navigation. Manual operation consisted of navigating the drone using roll, pitch, yaw and throttle setpoints from a Radio Controller; whereas the autonomous mode consisted of navigating to prespecified waypoints set by the user on the Ground Control Station (QGroundControl).

### QGroundControl Software

QGC proved to be instrumental not only for communication with the drone during flight but also for calibrating sensors, motor ESCs and updating flight parameters. For establishing connection with the Ground Control Station, we used a radio telemetry module. The state estimates of the drone required for autonomous navigation were determined using an external GPS module and onboard sensors on the flight controller. For remotely operating the spraying mechanism, an RC channel was assigned to regulate the voltage of the onboard pump.

An optimal choice of various PID gains for the flight controller ensured that our drone remained stable during flight, and maintained its position even in the presence of external disturbances like wind and recoil force of the spray. For aiding manual navigation, FPV control was added by using a Raspberry Pi and an onboard RPi-camera for transmitting continuous video streams to the ground control station. Further, all electrical components were insulated using a silicone spray and were mechanically protected by 3D-printed envelopes.

### Safety Measures

To ensure safety of the drone, surrounding structures, and the operating personnel, various failsafes were enabled including GPS signal loss failsafe, low battery failsafe, and radio signal loss failsafe. These failsafes ensured that in any of the aforementioned conditions, the drone returns safely to its launching site. In addition to this, a pipeline was established to allow users to upload custom missions or specify a set of waypoints, enabling cleaning of an entire structure with a single key press.

## Project Deliverables

1. A Hexacopter Drone with an onboard Pixhawk Cube, Telemetry Module, GPS Module and Radio Receiver 
2. A Complete Water Spraying Mechanism with a Water Tank, Water Pump and a Spraying Pipe with a Nozzle for Effective Water Spraying
3. Complete Software Stack for operating the Drone using Radio Control as well as for autonomous takeoff and hover in various operating modes like Position and Hold.  

## Navigating the Repository

```plaintext
/
├── src/
│   ├── Controller 1
|   ...
├── 3d_models/
│   ├── Component 1
│   ...
├── pcb/
│   ├── others/
├── reports/
├── others/
├── bom.xlsx
└── README.md
```

The repository includes all the essentials needed to understand and replicate this project in its current state. We have also highlighted our learnings, the mistakes we have made and the solutions and workarounds that we have found. 

1. The `src` folder includes the details of our Pixhawk, Raspberry Pi and the Radio Control that we have used. Their respective `README.md` files include instructions of using them and what changes we made to their default configurations before operating them.
2. The `3d_models` directory has all our CAD Models with their renders and the images of final fabricated components. We also include our insights about each of these components and design choices(if any) that went into finalising said components.
3. While we did not design and fabricate a PCB, the `pcb` directory includes a single directory `others` that has the designs and implementations and schematics of our in-house Power Distribution Board and the BEC Circuit that we have installed on our current prototype.
4. `reports` includes all our checkpoint presentations. This directory serves as a progress tracker for our project which indicates the levels of completion of our drone at various stages of the semester.
5. We include our simulation results and images of our assembly in parts and as a whole in the `others` directory. 
6. The `bom.xlsx` is our complete Bill Of Materials where we provide the list of components that have been procured for the project. We have also provided links and references for purchase from official and authentic sources.    

## Learnings and Key Takeways

1. Developed an understanding on aerial robotics (specifically quadcopters and hexacopters) from a mechanical point of view. This was crucial in making the choice between a quadcopter and hexacopter for out final drone. We eventually settled on the latter because of its increased payload capacities.
2. Working with the Pixhawk Cube as our Primary Flight Controller. This was a unique challenge as despite the Pixhawk being an off-the-shelf state of the art controller, we ran into multiple techincal and compatibility issues that needed to be resolved. We also needed to re-configure the boot sequence of the Pixhawk to ensure that our ESC Calibration and power up was synchronised
3. Electronic Speed Controllers must be thoroughly tested before installation on the drone. We faced severe troubles with the calibration of our ESCs partly because of the faults in the ESCs themselves and partly because of their improper calibration with the flight controller
4. Power Distribution Boards are extremely crucial in robotics applications. Our on-frame PDB was not uniformly powering the ESCs causing them to shut down unexpectedly. This also cost us one of our ESCs as it shut down during testing and we were unable to get it working again. To resolve this issue, we developed and made our own PDB using single sided copper clads and multi-stranded PVC wire.  
5. Experimented with different methods of operating the drone including Radio Control, using the QGroundController and operating the actuators from a laptop communicating with the drone using a Telemetry Module. These were especially useful for continuous testing and dry testing the components before performing the flight tests
6. Beyond the technical learnings, this project also helped us improve our time management and team skills. Coordinating with other members to ensure that the project keeps moving forward and our progress is not halted. We also learned that tasks should not be trivialized or underestimated. We made this mistake with our assembly and calibration but ran into a large number of errors because of both our mistakes and the malfunctions of our components. 


## Road Ahead

In the semester long project, we were able to develop a proof of concept prototype for the window cleaning drone but there are several areas of improvement that we have identified which would make this project even better:

1. Our current payload capacity is around 2kg which includes a 0.5L water tank. This is not sufficient for sustained cleaning purposes and we need to increase the total water carrying capacity of the drone. This can be done in 2 ways : increasing the water tank capacity or using a ground stationed water pump to supply water to the drone. Both these methods can be experimented with, each has their advantages and disadvantages which must be weighed carefully.
2. We can use motors with an inceased KV Rating. This increases the total thrust that is provided by the motors and thus increases the payload capacity of the drone. While this comes at the cost of a decreased battery life, the analysis of the decision must be done by weighing all options such as exploring the possiblility of using a larger battery
3. The whole drone system can be scaled by in size. While the weight of the drone frame does increase, this can be offset by using larger batteries and more powerful motors. This also facilitates a larger water tank which can be installed on-board. (In the current marker agricultural and irrigation drones which work on similar principles have payloads of upto 10-16L of fluid)
4. Implement a user-friendly Graphical User Interface Application that can be used to input the coordinates of the windows as waypoints with approximate window sizes. An on-board computer converts these into a mission which can be run by the drone to clean the windows at the waypoints in succession. 
5. We can modify and explore robust controllers which provide additional stability to the drone and improve the performance of the drone in windy conditions and handle the recoil and other forces by the water mechanism in a better manner 

