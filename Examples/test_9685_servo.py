from pyb import Pin
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

print('Scanning I2C bus...')
devices = i2c.scan() 
print('Scan finished.')
device_count = len(devices)

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
            
            
servoboard = Servos(i2c, address=0x40, freq=50, min_us=600, max_us=2400,
                 degrees=180)

print("servo 0 pan")
for i in range(0,190,50):
    print("pan {} angle".format(i))
    servoboard.position(0, i)
    time.sleep(0.1)

print("servo 1 tilt")
for i in range(0,90,10):
    print("tilt {} angle".format(i))
    servoboard.position(0, i)
    time.sleep(0.1)

print("zero position")
servoboard.position(0, degrees=0)
servoboard.position(1, degrees=94)

for i in range(180,0,-10):
    print("tilt {} angle".format(i))
    servoboard.position(1, i)
    time.sleep(0.1)
servoboard.position(1, degrees=90)
print("done")
