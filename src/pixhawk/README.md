# Pixhawk Cube Orange+

## Hardware Specifications

Pixhawk Cube Orange+ is used as our flight controller unit. It is used primarily because of it's compatibility with a large range of autopilots, especially PX4. 

### Primary Sensors                     

Following lists some specs of our chosen flight controller:

1. Processor & Co-Processor
    - Main Processor: STM32H757ZI (32-bit ARM Cortex-M7) running at 400 MHz
    - Failsafe Co-Processor: STM32F103 (32-bit ARM Cortex-M3) operating at 24 MHz​

2. Sensors
    - Accelerometers: 3 redundant units (ICM42688p, ICM20948, ICM20649)
    - Gyroscopes: 3 redundant units (ICM42688p, ICM20948, ICM20649)
3. Magnetometer: 1 unit (ICM20948)
4. Barometers: 2 units (MS5611)​

### Additional Sensors

These sensors are connected via SPI and are housed in a temperature-controlled, vibration-isolated enclosure to ensure optimal performance.​
1. Power Management
    - Redundant Power Supply: Dual inputs with automatic failover
    - Servo Rail Voltage: Supports 3.3V and 5V (software-selectable)
    - Input Voltage Range: 4.1V to 5.7V

    - Rated Input Current: 2.5A

    - Rated Input/Output Power: 14W

2. USB Port Input: 4V to 5.7V, 250 mA​

3. I/O & Communication Ports
    - PWM/Servo Outputs: 14 total (8 from IO, 6 from FMU)

    - UART Ports: 5 total (1 high-power capable, 2 with hardware flow control)

    - CAN Bus Interfaces: 2 (1 with internal 3.3V transceiver, 1 on expansion connector)

    - R/C Inputs: Supports Spektrum DSM/DSM2/DSM-X® Satellite, Futaba S.BUS®, and PPM-SUM

    - RSSI Input: PWM or voltage

    - I2C Ports: 2

    - SPI Port: 1 (un-buffered, for short cables only)

    - Analog Inputs: 3 (3.3V and 6.6V)

    - USB Ports: Internal microUSB and external microUSB extension​

4. Additional Features
    - Failsafe Co-Processor: Ensures system reliability during critical operations

    - Integrated Backup System: Facilitates in-flight recovery and manual override, especially beneficial for fixed-wing applications

    - Redundant Power Supply Inputs: Automatic failover to maintain system stability

    - External Safety Switch: For manual intervention and safety

    - Multicolor LED Indicator: Provides visual status feedback

    - High-Power, Multi-Tone Piezo Audio Indicator: Audible alerts for system status

    - microSD Card Slot: Supports high-rate logging over extended periods​

## Reasons for Choosing PX4 Autopilot

We proceeded with the PX4 Autopilot over other autopilots for the following reasons:
- It's largely used by industries and hobbyists around the world, with a large community of developers, ensuring a consistently stable performance.

- The source code is fairly modular and is accompanied with a comprehensible documentation, which could have allowed us to integrate our custom controller code into the PX4 architecture seamlessly, had we chosen to do so.
- There is a wide range of tunable parameters that we could customize to ensure an optimal system performance.
- There exist multiple failsafes including low battery, telemetry loss and gps loss failsafes, ensuring that the drone returns safely to its takeoff position.
- It is compatible with a wide range of middlewares like ROS, allowing the user offboard applications like carrying out entire missions.
- It's compatibility with middlewares also allowed us to validate its performance on physics simulating platforms like Gazebo prior to performing hardware tests. 

## Review of PX4 Software Stack

The latest version of the PX4 autopilot was cloned from the following source: https://github.com/PX4/PX4-Autopilot

Initially, in order to explore possibilities of changes that we could make to the source code in order to integrate our controller, we thoroughly reviewd the PX4 stack and identified the relevant modules and uORB topics that needed to be modified for incorportating out scheme. The following lists these modules:

- `mc_pos_control`: This module of PX4 is responsible for implementing the position and velocity controllers and transforming the PID controlled accelerations by a rotation matrix to output the desired attitudes as quaternions. In addition, it computes the desired thrust in the body frame for the nominal case. Since the outer-loop control is independent of the configuration and the number of rotors of the aerial vehicle, we leave it unchanged for our implementation. The roll and pitch setpoints used by the default attitude controller are the same as the ones used for our custom control strategy.

- `mc_att_control`: This module implements the attitude control (the first part of the inner loop). The default controller subscribes to the attitude setpoints published by the mc_pos_control and performs non-linear quaternion-based attitude control to compute the rate setpoints. The function responsible for this computation is the `AttitudeControl::update()` function, defined in the `mc_att_control`/`AttitudeControl.cpp` file, which is called at every iteration of `mc_att_control::Run()`. For our custom implementation, we compute the actuator setpoints (normalized motor thrust values) in this module itself. We create the `AttitudeControl::custom_update()` function to publish actuator commands to the mixer module. This switching is controlled by the failure detector module. Moreover, rate setpoints are not published in the case of a motor failure, bypassing the default rate and control allocator modules.

- `mc_rate_controller`: This module performs PID control on the angular body rates to compute the commanded thrust and torques. For our implementation, we have bypassed this module since all of our inner loop computations are being performed in the attitude control module itself.

- `control_allocator`: Thrust and torque setpoints are pre-multiplied by the control effectiveness matrix to calculate the normalized motor thrusts. Since our attitude controller module, in its custom mode of implementation, publishes actuator setpoints as well, a potential collision of setpoints is prevented by a conditional statement controlled by the failure detector module.

Since the tests we performed on simulation depicted that the drone remained reasonably stable despite the recoil forces it experienced from the water spraying mechanism using the default cascaded PID flight controller, we didn't feel the need to explore other advanced controllers and subsequently make changes to the source code.

## Pixhawk Flight Modes

### Pixhawk Flight Modes Explained

Pixhawk supports various flight modes, each suited for different flying styles and purposes. Below is a detailed explanation of commonly used modes:

---

#### 1. **Manual Mode**

- **Description**: 
  - Pilot has **full control** of the aircraft.
  - No stabilization or assistance from the flight controller.

---

#### 2. **Stabilized Mode**

- **Description**:
  - The flight controller automatically **levels the aircraft** when sticks are centered.
  - Pilot controls throttle and direction manually.

---

#### 3. **Altitude Mode**

- **Description**:
  - The aircraft **maintains a consistent altitude** using barometer data.
  - Pilot controls roll, pitch, and yaw.

---

#### 4. **Hold Mode**

- **Description**:
  - Aircraft holds **current GPS position and altitude**.
  - Re-centering sticks will bring the aircraft to a stop and hover.

---

#### 5. **Acro Mode**

- **Description**:
  - Pilot controls **rotation rate**, not angle.
  - Aircraft does **not auto-level**.

---

#### 6. **Mission Mode**

- **Description**:
  - Executes a **predefined autonomous mission** using waypoints.
  - No manual input required during the mission.

---

#### 7. **Position Mode**

- **Description**:  
  - **Full position and altitude stabilization**
  - Uses **GPS and altitude sensors** to control the vehicle’s position and height.

---

> **Note**: Always ensure good **GPS lock** before using GPS-dependent modes like **Hold**, **Position** and **Mission**. Use **Manual or Stabilized** when testing indoors or in GPS-denied areas.



## Modifications to Base Software Stack Parameters


The only changes in the PX4 Autopilot were a result of changes made to the defult parameters. Here is an exhaustive list of all the parameters we changed:

1. Airframe parameters:
    - CA_AIRFRAME: Multirotor
    - MAV_TYPE: Hexarotor
2. Motor assignments:
    - PWM_MAIN_FUNC1: Motor 5
    - PWM_MAIN_FUNC2: Motor 1
    - PWM_MAIN_FUNC3: Motor 4
    - PWM_MAIN_FUNC6: Motor 6
    - PWM_MAIN_FUNC7: Motor 2
    - PWM_MAIN_FUNC8: Motor 3
3. RC setup:
    - RC_MAP_PITCH: Channel 2
    - RC_MAP_ROLL: Channel 3
    - RC_MAP_THROTTLE: Channel 1
    - RC_MAP_YAW: Channel 4
    - RC_MAP_AUX1: Channel 10
    - RC_MAP_ARM_SW: Channel 9
    - RC_MAP_FLTMODE: Channel 5
    - RC_MAP_KILL_SW: Channel 6
    - COM_FLTMODE1: Position
    - COM_FLTMODE4: Manual
    - COM_FLTMODE6: Hold
4. Disabling redundant failsafes:
    - COM_ARM_HFLT_CHK: Disabled
    - COM_ARM_SDCARD: Disabled
5. Changing min and max of pump pwms:
    - PWM_AUX_MIN1: 0
    - PWM_AUX_MAX1: 2000
6. Battery:
    - BAT1_N_CELLS: 4S Battery
    - BAT1_V_CHARGED: 4.20 V
    - BAT1_V_EMPTY: 0.0V
7. GPS:
    - GPS_1_CONFIG: GPS 2


## Peripherals Used

PX4 Autopilot uses the Mavlink protocol to communicate with various onboard and offboard peripherals. The onoboard peripherals consist of the built in sensors within the flight controller listed before, while the offboard peripherals include:
1. **GPS Module**: GPS 2 Port : Cirocomm Active GPS Antenna
2. **Motor Driver Pwm Input**: AUX1 Port : L298N Motor Driver
3. **6 30A ESCs**: MAIN 1-3 and 6-8 Ports : SimonK 30A Electronic Speed Controller
4. **Telemetry module**: TELEM1 Port : HolyBro SiK Telemetry Module
5. **RC receiver**: RC-IN Port : RadioMaster TX16S
6. **Power connection**: POWER1 Port : Bonka 4S LiPo Battery





