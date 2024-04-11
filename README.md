# Car Base Board
A printed circuit board (board) using the BlackPill microcontroller as a base platform for robot car projects.

* Platform: STM32
* Board: STM32F411CEU6 (BlackPill)
* Copyright (C) 2024 KW Services.
* MIT License
* MicroPython 1.20

## Scope.
Jump start your robot car project with the <B>Car Base Board</B>.  The board provides a patch-wire friendly (flexible) base for the low-cost WeAct Studios' BlackPill v3.1 USB Stick board. The BlackPill, the devices, wiring and battry are not included, However the low-cost BlackPill and these popular devices are available from popular retailers.  

The board includes power components, a User Button, and LEDs.  
It includes **wiring ports** for these external devices:
<div align="left">
    <table >
    <tr>
        <td><b>Control</b></td>
        <td><b>Monitor</b></td>
        <td><b>Communicate</b></td>
    </tr>
     <tr>
        <td>
        &#x2022; L298N Dual Motor Control</br>
        &#x2022; PC9685 Sensor (6v servos)</br>
        &#x2022; (2x) Servos (5v servos)</br>
        </td>
        <td>
        &#x2022; Ultrasonic (SR-HC04/05)</br>
        &#x2022; (3x) Infrared Obs. Tracker</br>
        &#x2022; (2x) Slotted optical “Speed”</br>
        </td>
        <td>
        &#x2022; UART port (Bluetooth)</br>
        &#x2022; Infrared Receiver (IR1838)</br>
        &#x2022; OLED port (SSD1306)</br>
         &#x2022; NRF24 port</br>
        </td>
     </tr>
    </table>
</div>

This GitHub site includes simple MicroPython examples.

![](Board_image.jpg)

The board is compatible with popular Integrated Development Environments (IDE).  The board is well suited to creating projects in MicroPython. [Future YouTube Video]()

### Power Management
During development the BlackPill board is powered from a USB-C cable to a desktop computer.  An external battery could provide power to the high volt components and for the five volt devices via a onboard regulator.  Power from the battery is controlled by an ON/OFF switch.

The diagram below suggests the power management capable with this board.
![](PowerDiagram.jpg)

For Autonomous operation, battery power is supplied to the BlackPill via the USB-A Power Port.

## Acquiring the Car Base Board.
To learn more, [click this future link]() to visit the <B>Applying Microcontroller Solutions</B> store at Tindie.

## Acquiring the <B>BlackPill</B> (STM32F411) from WeAct Studios.
[Link to GitHub web site](https://GitHub.com/WeActStudio/WeActStudio.MiniSTM32F4x1)

1. Make sure you are getting BlackPill (STM32F411) v3.1.
2. You should get the optional 8 MB or 16 MB Flash chip pre-soldered to the bottom of the board.
3. Some retailers will sell the BlackPill board with the headers pre-soldered.
4. Also, from your favorite retailer, I suggest you acquire a "ST LINK-V2" dongle.

A copy of MicoPython firmware (version 1.20) resides on the GitHub site. [Link](https://GitHub.com/kwinter745321/STM32F411BaseBoard/tree/main/Firmware).  

