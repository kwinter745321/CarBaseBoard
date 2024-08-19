# bb_machine_test_i2c.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from machine import Pin, I2C
import time

I2C_PORT = 'I2C1'
I2C_SCL_PIN = 'PB6'
I2C_SDA_PIN = 'PB7'
I2C_FREQ = 400000

i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
print("*",i2c)

print('Scanning I2C bus...')
devices = i2c.scan() 
print('Scan finished.')
device_count = len(devices)

if device_count == 0:
    print('No I2C device found.')
else:
    print('I2C devices found:',device_count)
    print("| Decimal Address | Hex Address |")
    print("| --------------- | ----------- |")
    for device in devices:
        xdevice = str(hex(device))
        print("| %15s " % device,end="")
        print("| %9s " % xdevice," |")
            

print("done")
