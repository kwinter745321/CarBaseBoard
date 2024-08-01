# bb_machine_radio_receive.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
import sys
import ustruct as struct
import utime
import pyb
from machine import Pin, SPI, SoftSPI
from nrf24l01 import NRF24L01
from micropython import const
import time

# this code runs on board address "00001"
### Constants and PIN Definitions ###############
USER_BUTTON_PIN = 'PB10'
address = "00001"
text = ""

### Setup #########################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
spi=pyb.SPI(2)
radio=NRF24L01(spi, cs=Pin("PA8"), ce=Pin("PB12"), payload_size=10)

### Radio Configuration ###################
radio.open_rx_pipe(0, address)
radio.start_listening()

### main ##########################
done = False
print("Press User Button to EXIT.")
try:
    print("Waiting for transmission...")
    while not done:
        user_btn = user.value()
        #print("user_btn:",user_btn)
        if user_btn == 0:
            done=True
        if radio.any():
            text = ""
            while radio.any():
                text = radio.recv()
                print("received:",text)
        time.sleep(0.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    print("done")

