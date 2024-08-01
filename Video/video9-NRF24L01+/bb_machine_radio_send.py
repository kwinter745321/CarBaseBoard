# bb_machine_radio_send.py
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
import utime

# this code runs on board address "00002"
### Constants and PIN Definitions ###############
USER_BUTTON_PIN = 'PB10'
address = "00001"

### Setup #######################################
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
spi=pyb.SPI(2)
radio=NRF24L01(spi, cs=Pin("PA8"), ce=Pin("PB12"), payload_size=10)

### Radio Configuration #########################
radio.open_tx_pipe(address)
radio.stop_listening()

### main ########################################
done = False
print("Press User Button to send text.")
try:
    while not done:
        user_btn = user.value()
        if user_btn == 0:
            print("Sending text in the payload (10 chars).")
            mytime = ""
            myear,mmonth,mday,mhr,mmin,msec,mwd,myd = time.localtime()
            mydate = "{:4d}-{:02d}-{:02d}".format(myear,mmonth,mday)
            mytime = "{:02d}:{:02d}:{:02d}".format(mhr,mmin,msec)
            print("time:",mytime)
            radio.send_start("(" + mytime + ")")
            time.sleep(1)
        time.sleep(0.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    print("done")

