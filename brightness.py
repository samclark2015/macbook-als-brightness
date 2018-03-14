#!/usr/bin/python3

import asyncio
import re
import time
import math

### Start Config
poll_time=0.5 # Time between updates, in seconds
poll_count=10 # Number of polls used to calculate average

max_als=4095

min_keyb = 0
max_keyb = int(open('/sys/class/leds/smc::kbd_backlight/max_brightness').readline().strip())

min_screen = 70
max_screen = int(open('/sys/class/backlight/intel_backlight/max_brightness').readline().strip())

### End Config

avg_als=[]
last_avg=0.0

def get_keyb():
    f = open('/sys/class/leds/smc::kbd_backlight/brightness')
    return int(f.readline().strip())

def get_screen():
    f = open('/sys/class/backlight/intel_backlight/brightness')
    return int(f.readline().strip())

def get_als():
    f = open('/sys/bus/acpi/devices/ACPI0008:00/iio:device0/in_illuminance_raw')
    s = f.readline().strip()
    return int(s)

def set_keyb(val):
    f = open('/sys/class/leds/smc::kbd_backlight/brightness', 'w')
    f.write(str(val))

def set_screen(val):
    f = open('/sys/class/backlight/intel_backlight/brightness', 'w')
    f.write(str(val))

def fade_screen(old, new):
    for i in range(old, new, 1 if old < new else -1):
        set_screen(i)
        time.sleep(0.007)

def fade_keyb(old, new):
    #print(old, new)
    for i in range(old, new, 1 if old < new else -1):
        set_keyb(i)
        time.sleep(0.007)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def handle_diff(val):
    screen_delta = val * max_screen
    screen_val = math.ceil(get_screen() + screen_delta)
    if min_screen < screen_val < max_screen :
        fade_screen(get_screen(), screen_val)

    keyb_delta = val * max_keyb
    keyb_val = math.ceil(get_keyb() - keyb_delta)
    if min_keyb < keyb_val < max_keyb:
        fade_keyb(get_keyb(), keyb_val)

async def loop_fun(loop):
    global last_avg
    while True:
        log_val = math.log(1+get_als())/math.log(1+max_als)
        avg_als.append(log_val * max_als)
        if len(avg_als) > poll_count:
            avg_als.pop(0)
        if len(avg_als) > 0:
            avg = sum(avg_als)/len(avg_als)
            perc = (avg - last_avg) / max_als
            #val = translate(avg, 0, max_als, 0, max_screen)
            #print("Avg val: {}; Percent {}%".format(avg, perc * 100))
            handle_diff(perc)
            last_avg = avg

        await asyncio.sleep(poll_time)

loop = asyncio.get_event_loop()
loop.run_until_complete(loop_fun(loop))
loop.close()
