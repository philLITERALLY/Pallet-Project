### Contents

[Running Mode](https://github.com/philLITERALLY/Pallet-Project#running-mode)
* [Process](https://github.com/philLITERALLY/Pallet-Project#process)
[SETUP Funcionality](https://github.com/philLITERALLY/Pallet-Project#setup-funcionality)
* [SINGLE Button](https://github.com/philLITERALLY/Pallet-Project#single-button)
* [ROTATE Button](https://github.com/philLITERALLY/Pallet-Project#rotate-button)
[Config Options](https://github.com/philLITERALLY/Pallet-Project#config-options)


# Running Mode

Whenever a user hits the `START` button we start the process listed below.

Whenever a user then hits `STOP` we reset all the AIO values (apart from rotate).

## Process

1. Delay (start_delay)
2. Running Light On (OUT8 ON)
3. Set up for image:
    1. Turn Board Stops On (OUT0 ON)
    2. Get current R+L (IN0 + IN1)
    3. If R or L ON wait for board to leave (IN0 + IN1 OFF)
    4. Wait for R+L On (IN0 + IN1 ON)
    5. Turn Clamp On (OUT1 ON)
    6. Sleep for 0.05 secs
    7. Check if Clamps are open (IN7 + IN8 ON) if they are then FAULT:
        1. Turn Fault On (OUT5 ON)
        2. Highlight FAULT in UI
        3. While user hasn't accepted fault:
            1. Pulse light (OUT6 ON)
            2. Sleep for 0.5 secs
    8. Turn Lift On (OUT2 ON)
    9. Wait for Lift On (IN3 ON)
    10. Turn Board Stops Off (OUT0 OFF)
4. Delay (wait_grab)
5. Read Camera 1
6. Read Camera 2
7. "Handle" Frame 1 (Get bark count and image)
8. "Handle" Frame 2 (Get bark count and image)
9. Figure out Side 1 Bark Count (Cam1 count + Cam2 count divided by two)
10. Update UI
11. Delay (after_grab)
12. Get current CCW and CW (IN4 + IN5)
13. Sleep for 0.2 secs
14. Toggle Rotate State (OUT3 Switch)
15. Wait for CCW and CW to change (IN4 + IN5)
16. Delay (wait_grab)
17. Read Camera 1
18. Read Camera 2
19. "Handle" Frame 1 (Get bark count and image)
20. "Handle" Frame 2 (Get bark count and image)
21. Figure out Side 2 Bark Count (Cam1 count + Cam2 count divided by two)
22. Update UI
23. Delay (after_grab)
24. If either side is over "REJECT" (defined in UI) then it's a reject
25. If Plank isn't a reject and less bark of Side 1:
    1. Get current CCW and CW (IN4 + IN5)
    2. Sleep for 0.2 secs
    3. Toggle Rotate State (OUT3 Switch)
    4. Wait for CCW and CW to change (IN4 + IN5)
26. Drop Plank:
    1. Turn Lift Off (OUT2 OFF)
    2. Wait for Lift Down (IN2 ON)
    3. Turn Clamp Off (OUT1 OFF)
    4. Wait Clamp Open (IN6 ON)
27. If Reject:
    1. Turn Reject On (OUT4 ON)
    2. Sleep for 0.2 secs
    3. Turn Reject Off (OUT4 OFF)
    4. Update Stats for UI
28. If Not Reject:
    1. Turn Good Board On (OUT7 ON)
    2. Sleep for 0.2 secs
    3. Turn Good Board Off (OUT7 OFF)
    4. Update Stats for UI


# SETUP Funcionality

When a user clicks SETUP they are brought to an adminstrative page. From here users can modify how we handle the images and perform the bark check. They can also perform isolated I/O actions using buttons.

## SINGLE Button

When first pushed the SINGLE Button runs the "Set up for image" function and marks the button as active.

On it's second push it runs the "Drop Plank" function and deactivates the button.

First push (Set up for image):
1. Turn Board Stops On (OUT0 ON)
2. Get current R+L (IN0 + IN1)
3. If R or L ON wait for board to leave (IN0 + IN1 OFF)
4. Wait for R+L On (IN0 + IN1 ON)
5. Turn Clamp On (OUT1 ON)
6. Sleep for 0.05 secs
7. Check if Clamps are open (IN7 + IN8 ON) if they are then FAULT:
    1. Turn Fault On (OUT5 ON)
    2. While user hasn't accepted fault:
        1. Pulse light (OUT6 ON)
        2. Sleep for 0.5 secs
8. Turn Lift On (OUT2 ON)
9. Wait for Lift On (IN3 ON)
10. Turn Board Stops Off (OUT0 OFF)

Second push (Drop Plank):
1. Turn Lift Off (OUT2 OFF)
2. Wait for Lift Down (IN2 ON)
3. Turn Clamp Off (OUT1 OFF)
4. Wait Clamp Open (IN6 ON)

## ROTATE Button

The ROTATE Button simply toggles the rotate state (OUT3).

# Config Options

There is a `config.ini` file which holds configurable variables that modify the process.

**NOTE:** When you edit these values you need to restart the application to take effect

The values in `config.ini` are described below:

| Name | Description | Modified By UI? |
| ------------- | ------------- | ------------- |
| [DELAY] | This section handles any delays (in seconds) | |
| start_delay | Runs at the start of every loop before the board stops go on | :x: |
| wait_grab | Runs just before each image grab | :x: |
| after_grab | Runs after each image grab | :x: |
| [CAMERA] | Contains information that modifies the camera | |
| cam_width | Width of the camera image | :x: |
| cam_height | Height of the camera image | :x: |
| cam_exposure | Exposure of the camera image | :x: |
| frame_width | Width that contains plank | :x: |
| [BOARD SETTINGS] | Contains settings for the board/plank | |
| board_width | Width of the board i.e. 70, 96, 120 | :heavy_check_mark: |
| board_length | Length of the board (determines how many boxes to use) | :heavy_check_mark: |
| cam1_box_count | Amount of boxes for camera 1 | :heavy_check_mark: |
| cam2_box_count | Amount of boxes for camera 2 | :heavy_check_mark: |
| [REJECT SETTINGS] | Contains settings reject level | |
| reject_level | What percent of bark is considered a reject | :heavy_check_mark: |
| [TRANSFORM SETTINGS] | Contains settings for plane transformation | |
| cam1_trans_left | Position to determine plane adjust | :heavy_check_mark: |
| cam1_trans_right | Position to determine plane adjust | :heavy_check_mark: |
| cam2_trans_left | Position to determine plane adjust | :heavy_check_mark: |
| cam2_trans_right | Position to determine plane adjust | :heavy_check_mark: |
| [THRESH SETTINGS] | Contains settings for threshing of image | |
| cam1_thresh | Thresh value applied to cam1 image | :heavy_check_mark: |
| cam2_thresh | Thresh value applied to cam2 image | :heavy_check_mark: |
| [BOX POSITIONING] | Contains values for box positions | |
| side`{X}`_vert | Vertical positioning of side `X` boxes | :heavy_check_mark: |
| side`{1}`\_cam`{2}`\_box`{3}`\_`{4}` | Determines horizontal position of box | :heavy_check_mark: |
| [AIO] | Settings for AIO | |
| aio_wait | Length of time to "pulse" AIO (in seconds) | :x: |