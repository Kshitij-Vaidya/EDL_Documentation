# Raspberry Pi 4

## Specifications

1. Model : Raspberry Pi 4 Model B 4GB RAM
2. External SD Card : 128GB SanDisk
3. Operating System : RasPiOS 
4. NoIR Camera V2

## Application In The Drone 

We used the Raspberry Pi on-board primarily to capture and relay the First Person View feed to the operater using the Radio Control on the ground station of the drone. We used the Raspberry NoIR Camera as our FPV Camera. To operate the Raspberry Pi, it is powered up and its Hotspot is turned on  (We configured it to be switched on at power up itself). After this, our ground station laptop is connected to the same network allowing us to SSH into the on board computer. The ground control station would require the `ffmeg` and `gstreamer` libraries which can be installed as follows :

1. `sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad`

2. `sudo apt install ffmpeg`

Once that is complete, we can run the following sequence of commands in the command window to start and transmit the camera feed.

1. Start the camera and configure its streaming parameters like dimensions of the feed and the framerate

`libcamera-vid -o - -t 0 -n --width 320 --height 200 --framerate 24 | cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' --sout-mux-caching=100 :demux=h264`

2. The following command is entered in a terminal window in the receiver laptop (not in the SSH window). This starts the reception of the video feed at the receiver.

`ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental http://10.42.0.1:8090 `

## Rotating the Camera Feed

In our drone assembly, we were constrained by the length of the ribbon wire of the camera and thus were forced to orient the camera in a rotated alignment. To counter this, we worked around a terminal command that rotates the incoming feed before relaying and storing. This can be done by modifying the `ffplay` command as follows.

`ffplay -fflags nobuffer -flags low_delay -framedrop -strict experimental -vf "transpose=1" http://10.42.0.1:8090`

The values taken by the transpose flag are interpretted as follows:


    transpose=1 → 90° clockwise

    transpose=2 → 90° counterclockwise

    transpose=0 → 90° clockwise and vertical flip

    transpose=3 → 90° counterclockwise and vertical flip

## Storing the Feed at the Receiver

The camera feed can be stored at the ground control station in the form of an `.mp4` file using the following terminal command 

`ffplay -fflags nobuffer -flags low_delay -framedrop http:/10.42.0.1:8090`  

The above command is the same as above used to start the camera feed. The command below is what is used to save the file at the ground station

`ffmpeg -fflags nobuffer -flags low_delay -probesize 32 -analyzeduration 0 -i http://10.42.0.1:8090 -vcodec libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p -f mp4 saved1.mp4`



