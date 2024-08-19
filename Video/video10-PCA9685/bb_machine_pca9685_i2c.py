# bb_machine_pca9685_i2c.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#

from machine import Pin, I2C
import time
import pca9685
from servo import Servos

I2C_PORT = 'I2C1'
I2C_SCL_PIN = 'PB6'
I2C_SDA_PIN = 'PB7'
I2C_FREQ = 400000

i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
print("*",i2c)

# print('Scanning I2C bus...')
# devices = i2c.scan() 
# print('Scan finished.')
# device_count = len(devices)

# if device_count == 0:
#     print('No I2C device found.')
# else:
#     print('I2C devices found:',device_count)
#     print("| Decimal Address | Hex Address |")
#     print("| --------------- | ----------- |")
#     for device in devices:
#         xdevice = str(hex(device))
#         print("| %15s " % device,end="")
#         print("| %9s " % xdevice," |")
            
servoboard = Servos(i2c, address=0x40, freq=50, min_us=600,
                    max_us=2400, degrees=180)

print("Example 1.  Position to zero.")
servoboard.position(0, degrees=0)
print("Position at zero.")
time.sleep(2)

print("Example 2.  Pan Servo 0 (180 degrees) in increments of 30 degrees.")
for i in range(0,185,30):
    print("Pan {} angle".format(i))
    servoboard.position(0, i)
    time.sleep(0.1)
time.sleep(2)

print("Example 3. Straight-ahead position.")
angle = 95
servoboard.position(0, degrees=angle)
#servoboard.position(0, degrees=90)
print("Position straight ahead {} angle".format(angle))
time.sleep(4)

print("Example 4. Reverse Servo 0 (180 degrees) in increments of 30 degrees.")
for i in range(180,-5,-30):
    print("Pan in reverse {} angle".format(i))
    servoboard.position(0, i)
    time.sleep(0.1)
time.sleep(2)


print("done")
