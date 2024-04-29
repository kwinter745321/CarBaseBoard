# test_synchronizeMotors.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from pyb import Pin, Timer, UART
import time
import math
##################################################
USER_BUTTON_PIN = 'PB10'
BUILTIN_LED_PIN = 'PC13'

key = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = (BUILTIN_LED_PIN, Pin.OUT)
##################################################

# Pin Definitions for Motor A/B (L298N Device)
MOTORA_EN_PIN = 'PA2'
MOTOR_IN1_PIN = 'PA15'
MOTOR_IN2_PIN = 'PB3'

MOTORB_EN_PIN = 'PA3'
MOTOR_IN3_PIN = 'PB4'
MOTOR_IN4_PIN = 'PB5'

ena = Pin(MOTORA_EN_PIN, Pin.OUT)
in1 = Pin(MOTOR_IN1_PIN, Pin.OUT)
in2 = Pin(MOTOR_IN2_PIN, Pin.OUT)
enb = Pin(MOTORB_EN_PIN, Pin.OUT)
in3 = Pin(MOTOR_IN3_PIN, Pin.OUT)
in4 = Pin(MOTOR_IN4_PIN, Pin.OUT)

# Pin Definition for Motor A/B Speed Sensors
SENSORA_PIN = 'PB1'
SENSORB_PIN = 'PB2'

# Global variables and Call Back Functions
countera = 0
counterb = 0

pwmatimer = Timer(2, freq=500)
pwmbtimer = Timer(2, freq=500)
# PWM.
pwmachannel = pwmatimer.channel(3, Timer.PWM, pin=ena)
pwmbchannel = pwmbtimer.channel(4, Timer.PWM, pin=enb)
print("PWM Timer for Motor A:{} \n Channel:{}".format(pwmatimer,pwmachannel))
print("PWM Timer for Motor B:{} \n Channel:{}".format(pwmbtimer,pwmbchannel))

sensora = None
sensorb = None

#Interrupt callbacks for Speed Sensor
def counta(pin):
    global countera
    countera = countera + 1
    return

def countb(pin):
    global counterb
    counterb = counterb + 1
    return

######################################

# Setup Interrupt Call Back Functions
def SetupMotorsAndSpeedSensors(SENSORA_PIN,SENSORB_PIN):
    global sensora, sensorb
    # Infrared (IR) Slotted Optical Speed Sensor.
    sensora = Pin(SENSORA_PIN, Pin.IN)
    sensorb = Pin(SENSORB_PIN, Pin.IN)
    # Handle Interrupts.
    sensora.irq(trigger=Pin.IRQ_RISING, handler=counta)
    sensorb.irq(trigger=Pin.IRQ_RISING, handler=countb)
    return

print("Program Begin.")
done = False
steps = 500
show_a = False
show_b = False
print("*******************************************")
print("**** Enable Motors forward for counts:",steps)
print("**** Show counter for Motor A: {} and Motor B: {}".format(show_a,show_b))
print("*******************************************")
print("Press User Button to start. Ctrl-C to exit.")
try: 
    while not done:
        key_btn = key.value()
        #print("Key:",key_btn)
        if key_btn == 0:
            key_btn = 1
            # Operate.
            SetupMotorsAndSpeedSensors(SENSORA_PIN,SENSORB_PIN)
            print("start motor A and B going forward")
            in1.on()
            in2.off()
            in3.on()
            in4.off()
            countera = 0
            counterb = 0
            idle_a = 0
            idle_b = 0
            t1 = time.time()
            t2 = time.time()
            print("Use the Speed sensors to synchronize Motor A and B.")
            while not done:
                #print("Speed Counters A:{} B:{} cnts.".format(countera,counterb))
                if (countera < steps):
                    pwmachannel.pulse_width_percent(100)
                else:
                    pwmachannel.pulse_width_percent(0)
                    idle_a = idle_a + 1
                    
                if (counterb < steps):
                    pwmbchannel.pulse_width_percent(100)
                else:
                    pwmbchannel.pulse_width_percent(0)
                    idle_b = idle_b + 1

                if (countera > steps) and (counterb > steps):
                    print("Motors stopped.")
                    t2 = time.time()
                    done = True
                #print("Speed Counters A:{} B:{} cnts.".format(countera,counterb))
                #time.sleep(0.1)
            print("Speed Counters A:{} B:{} cnts.".format(countera,counterb))
            print("Idle Counters A:{} B:{} cnts.".format(idle_a,idle_b))
            elapsed = t2 - t1
            print("Elapsed time: {} secs.".format(elapsed))
             # gear speed=counter x 60 sec/min divided by 20 cnts/revolution
             #            and divided by elapsed time 
            geara = (countera*3)/elapsed
            gearb = (counterb*3)/elapsed
            # RPM is gear divided by 2 Pi
            rpma = geara /(2 * math.pi)
            rpmb = gearb /(2 * math.pi)
            print("RPM A={:4.1f} RPM B={:4.1f} RPM".format(rpma,rpmb))
            print("Done.")
        time.sleep(0.2)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
    # Make sure counters are done spinning
    time.sleep(1)
finally:
    pwmatimer.deinit()
    pwmbtimer.deinit()
    print("Program end.")
