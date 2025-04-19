# Radio Controller : RadioMaster TX16S

The RadioMaster TX16S is a versatile 16-channel 2.4 GHz radio transmitter. The TX16S is compatible with OpenTX and EdgeTX firmware, offering extensive customization options. It includes USB-C charging, dual USB-C ports, external SD card support, and two UART expansion ports for future upgrades. The transmitter is powered by two 18650 Li-ion batteries or a 2S LiPo battery, providing long-lasting performance. 

We used the following Radio Model on the transmitter to map the channels to our desired outputs.

1. Channel 1 : THR 100% : Throttle
2. Channel 2 : ELE 50% : Pitch
3. Channel 3 : AIL 50% : Roll
4. Channel 4 : RUD 100% : Yaw
5. Channel 5 : SE : Controls Flight Modes
6. Channel 6 : SF : Kill Switch
7. Channel 9 : SG : Arm/Disarm the Drone
8. Channel 10 : S1 : Knob for Controlling the Motor

The percentages in the first 4 parameters control the sensitivity of the knob. These channel numbers must also reflect in the QGroundControl software which determines the channels used by the Pixhawk. If something is changed in the Radio Control, the same change must be done on the Pixhawk and vice versa.  