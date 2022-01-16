### Contents

[I/O Map](https://github.com/philLITERALLY/Pallet-Project#IO-Map)
* [Inputs](https://github.com/philLITERALLY/Pallet-Project#Inputs)
* [Outputs](https://github.com/philLITERALLY/Pallet-Project#Outputs)

[Running Mode](https://github.com/philLITERALLY/Pallet-Project#running-mode)
* [Process](https://github.com/philLITERALLY/Pallet-Project#process)
* [Outcome Chart](https://github.com/philLITERALLY/Pallet-Project#outcome-chart)

[SETUP Funcionality](https://github.com/philLITERALLY/Pallet-Project#setup-funcionality)

[Config Options](https://github.com/philLITERALLY/Pallet-Project#config-options)

# I/O Map

## Inputs

| Port | Description | Multi |
| -- | -- | -- |
| 0 | Go pulse from PLC (20ms) | White |
| 1 | ?? | Yellow |
| 2 | ?? | Orange |
| 3 | ?? | Red |
| 4 | ?? | Light Blue |
| 5 | ?? | Purple |
| 6 | ?? | Black |
| 7 | ?? | Grey |
| 8 | ?? | Pink |

## Outputs

| Port | Description | Multi |
| -- | -- | -- |
| 0 | Ready | White/Red |
| 1 | Good board | Yellow/Red |
| 2 | Flip | Green/Red |
| 3 | Reject | Red/Blue |
| 4 | ?? | Red/Brown |
| 5 | Fault | Red/Black |
| 6 | Not working | - |
| 7 | ?? | White |
| 8 | Running | Green |

# Running Mode

Whenever a user hits the `START` button we start the process listed below.

Whenever a user then hits `STOP` we reset all the AIO values.

## Process

1. Start running light (OUT8 ON)
2. Flag ready state (OUT0 ON)
3. Wait for pulse on IN0
4. Set OUT0 OFF
5. Read Camera 1
6. Read Camera 2
7. "Handle" Camera 1
8. "Handle" Camera 2
9. Test Side 1 for bark IF:
    - A or C above fail threshold
        1. Set BAD EDGE 1 flag
    - B above fail threshold
        1. Set REJECT flag
10. (FUTURE) Test SIDE 1 for form IF
    - FAIL
        1. Set REJECT flag
11. Test Side 2 for bark IF
    - A or C above fail threshold
        1. Set FLIP flag
    - B above fail threshold
        1. Set REJECT flag
12. (FUTURE) Test Side 2 for form IF
    - FAIL
        1. Set REJECT flag
13. Set OUT0 ON (Next Board)
14. IF:
    1. REJECT flag set
        - Clear flag
        - 100ms pulse OUT3 (Reject)
    2. BAD EDGE 1 and FLIP flag set
        - Clear flag
        - 100ms pulse OUT3 (Reject)
    3. Just FLIP flag set
        - Clear flag
        - 100ms pulse OUT2 (Flip)
    4. Neither flag set
        - 100ms pulse OUT1 (Good)
15. LOOP

## Outcome Chart

![Outcome Chart](/assets/Outcomes.png)

# SETUP Funcionality

When a user clicks SETUP they are brought to an adminstrative page. From here users can modify how we handle the images and perform the bark check. They can also perform isolated I/O actions using buttons.

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
| jam_delay | Delay on the first loop to make sure board clears (not in use) | :x: |
| [CAMERA] | Contains information that modifies the camera | |
| cam_width | Width of the camera image | :x: |
| cam_height | Height of the camera image | :x: |
| cam_exposure | Exposure of the camera image | :x: |
| frame_width | Width that contains plank | :x: |
| [BOARD SETTINGS] | Contains settings for the board/plank | |
| board_width | Width of the board i.e. 70, 96, 120 | :heavy_check_mark: |
| board_length | Length of the board (determines how many boxes to use) | :heavy_check_mark: |
| [REJECT SETTINGS] | Contains settings reject level | |
| reject_level | What percent of white is considered a reject | :heavy_check_mark: |
| edge_variance | How much better the first side has to be to flip it back again | :heavy_check_mark: |
| mid_size | What size the middle col is of total board | :heavy_check_mark: |
| [THRESH SETTINGS] | Contains settings for threshing of image | |
| cam_thresh | Thresh value applied to camera image | :heavy_check_mark: |
| [AIO] | Settings for AIO | |
| aio_wait | Length of time to "pulse" AIO (in seconds) | :x: |