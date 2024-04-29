# cbb_test_buttons.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin
import time

### PIN Definitions ###############
USER_BUTTON_PIN = 'PB10'

### Setup #########################
key = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

### Loop ##########################

print("Definitions and Drivers are setup.")
done = False
print("Press User Button to start.")
try: 
    while not done:
        key_btn = key.value()
        print("key_btn:",key_btn)
        if key_btn == 0:
            key_btn = 1
        time.sleep(0.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    print("done")