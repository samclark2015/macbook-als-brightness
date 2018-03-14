# MacBook Brightness Controller
### An ambient light sensor controller for MacBooks running Linux
Developed & tested on a 2013 rMBP running OpenSUSE Tumbleweed.

### Installation
Includes a script to install the Python script & associated `systemd` service

    $ ./install.sh

### Configuration
Inside of the `brightness.py` file, there is a marked section containing configurable variables. 
    poll_time:	number of seconds between polls of the ALS
    poll_count: number of samples used to calculate average
    
    max_als: 	maximum value of the ALS sensor
    
    min_keyb:	minimum value program can set for keyboard
    max_keyb	maximum value program can set for keyboard

    min_screen:	minimum value program can set for screen
    max_screen:	maximum value program can set for screen
