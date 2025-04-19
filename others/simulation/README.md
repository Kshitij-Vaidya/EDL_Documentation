Before performing hardware tests, we validated our approach on simulation.

## Software Requirements
- Gazebo Classic : https://docs.px4.io/main/en/sim_gazebo_classic/index.html
- ROS2 : https://docs.ros.org/en/humble/Installation.html
- MicroXRCE DDS : https://micro-xrce-dds.docs.eprosima.com/en/latest/agent.html
- Plotjuggler : https://index.ros.org/p/plotjuggler/
- Python : Version 3.10 or higher
- QGroundcontrol : https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html

## Gazebo Simulator
Gazebo Classic is a powerful, open-source 3D robotics simulator that integrates with ROS (Robot Operating System) and allows realistic testing of robots in complex environments. It provides physics simulation (via engines like ODE, Bullet), sensor simulation (e.g., cameras, IMUs, lidars), and supports plugins for custom behavior. For simulating our system, we used a default hexacopter model available in PX4's software stack, and varied its physical parameters according to our hardware specifications. Some of these values are:

### Inertial Parameters

| Component     | Dimensions            | Mass  | MoI (Ix)   | MoI (Iy)   | MoI (Iz)   |
|---------------|------------------------|--------|-------------|-------------|-------------|
| Chassis       | 0.67 x 0.67 x 0.15     | 0.997  | 0.039       | 0.039       | 0.075       |
| Camera        | 0.01 x 0.01 x 0.01     | 0.011  | 1.83e-7     | 1.83e-7     | 1.83e-7     |
| Landing Legs  | 0.01 x 0.03 (r x h)    | 0.1    | 7.54e-4     | 7.54e-4     | 7.45e-3     |
| Rotors        | 0.128 x 0.005 (r x h)  | 0.024  | 9.83e-5     | 9.83e-5     | 1.97e-4     |
| Nozzle        | 0.05 x 0.12 (r x h)    | 0.05   | 0.07        | 0.07        | 0.07        |

### Motor Parameters

| Parameters                             | Value        |
|----------------------------------------|--------------|
| Time Constant (s)                      | 0.0125       |
| Max Speed (rad/s)                      | 1240         |
| Max Speed (RPM)                        | 11840        |
| Motor Constant (N·s²/rad²)             | 8.038e-6     |
| Moment Constant (N·m·s²/rad²)          | 9.55e-3      |
| Rotor Drag Constant                    | 0.09637      |
| Rolling Moment Coefficient             | 1e-6         |

## Simulation Environment
- Simulator: Gazebo Classic
- Drone Model: Typhoon H480 (with custom parameters)
- Autopilot: PX4 v1.14
- Middleware: ROS2 with MicroXRCE bridge
- Operating System: Ubuntu 22.04

## Objective
- Take off the drone and maintain a constant altitude for 10s.
- To start spraying water in the specified direction.
- To ascend upwards by some distance while spraying water and
then stabilizing at its original altitude

## ROS2
We used ROS2 as the middleware for using the offboard mode on our simulated drone. A ROS2 node was run in the form of a python script after launching the drone. This node essentially utilized gazebo-ros topics for applying user-specified forces on the drone model. For bridging ROS2 with Mavlink (used by PX4 for communication), we used MicroXRCE-DDS.

## Water Spray Test
For simulating weight of the water column, reaction and recoil forces we applied forces in horizontal and vertical directions when the drone attained a stable altitude. The aforementioned script applied a constant vertical force simulating the weight of the onboard tank/ water column, and a user specified horizontal (with respect to drone frame) force on the drone.

## Running the Simulation
Expected configuration:
- All required softwares are installed
- Latest version of PX4 Autopilot repository is cloned and built
- A ROS2 workspace is setup with px4_msgs and px4_ros_com repositories cloned in the source directories
- The python file simulation.py is copied in the px4_ros_com folder
- MicroXRCE-DDS agent is cloned and built
- Parameters of the TyphoonH480 drone are modified as mentioned above

Run the following commands in separate terminals:

1. `./<path-to-QGC>/QGroundControl.AppImage`
2. `MicroXRCEAgent udp4 -p 8888`
3. `make /<path-to-PX4>/PX4-Autopilot/px4_sitl_default gazebo_typhoon_h480`
4. `ros2 run /<path-to-simulation.py>/simulation.py`

First takeoff the drone using QGC and let it stabilize. Then enter force values you want to simulate in the terminal running simulation.py. Finally, close all the terminals, extract the log file(.ulg) for the run for further analysis.

## Results and Analysis

Log files for the entire mission were analyzed and graphs were plotted using Plotjuggler. 

For force simulation, we computed the recoil thrust and an approximate value of the downward force using flow rate and mass of the tank/pipe and water pump that we used. We took the maximum value of these forces which were 10N in the horizontal and 11N in the Z direction.

From the position plots that we obtained, we inferred that the drone suffered an average perturbation of 0.3m in the horizontal direction and an average altitude drop of 0.2m once drone starts spraying water. Moreover, the drone settles at a pitch of around 20 degrees. Settling time for our run was around 5s. 