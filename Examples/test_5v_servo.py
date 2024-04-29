from pyb import Servo
import time

SERVO_PAN_PIN = 'PA1'  #1
SERVO_TILT_PIN = 'PA3'  #4


servo1 = Servo(2)
#servo4 = Servo(4)

def set_servo1(ang):
    servo1.angle(ang)
    
def doservo1(start,fin):
    for i in range(start,fin):
        set_servo1(i)
        time.sleep_ms(100)
    
def doservo4(ang):
    servo4.angle(ang)

print("angle 0")
servo1.angle(0)
time.sleep(0.1)
#servo4.angle(0)
time.sleep(1.5)

print("angle 45")
servo1.angle(45)
time.sleep(0.1)
#servo4.angle(45)
time.sleep(1.5)

print("angle 90")
servo1.angle(90)
time.sleep(0.1)
#servo4.angle(90)
time.sleep(1.5)

print("angle 135")
servo1.angle(135)
time.sleep(0.1)
#servo4.angle(135)
time.sleep(1.5)

print("angle 180")
servo1.angle(180)
time.sleep(0.1)
#servo4.angle(180)
time.sleep(1.5)

print("angle 0")
servo1.angle(0)
time.sleep(0.1)
#servo4.angle(0)
time.sleep(1.5)

print("angle -45")
servo1.angle(-45)
time.sleep(0.1)
#servo4.angle(-45)
time.sleep(1.5)

print("angle -90")
servo1.angle(-90)
time.sleep(0.1)
#servo4.angle(-90)
time.sleep(1.5)

print("angle -135")
servo1.angle(-135)
time.sleep(0.1)
#servo4.angle(-135)
time.sleep(1.5)

print("angle -90")
servo1.angle(-90)
time.sleep(0.1)
#servo4.angle(-90)
time.sleep(1.5)

print("angle -45")
servo1.angle(-45)
time.sleep(0.1)
#servo4.angle(-45)
time.sleep(1.5)

print("angle 0")
servo1.angle(0)
time.sleep(0.1)
#servo4.angle(0)
time.sleep(0.5)