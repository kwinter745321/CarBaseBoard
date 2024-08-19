# README.md - Video 10


Files for the video.


List of files:
- pca9685 Directory.  This directory contains the PCA9685 library.  Deploy this into the lib directory of the /flash directory of the BlackPill (STM32).
- bb_machine_test_i2c.py - application test file that scans the I2C bus for any devices connected to the microcontroller.
- bb_machine_pca9685_i2c.py - appliction file for the four example routines to actiopn the servo connected to the PCA9675 board and the microcontroller.
- PCA9685.pdf - A copy of the PCA9685 datasheet.
- STL directory
    - PCA9685PlateB-BodyPocket002.stl - This is a file suitable for a 3D printer.  The object built is a plate that holds the PCA9685 board.
      The STL object inner mounting holes match the PCA9685 board which uses 2.5 MM mounting holes.  The outer mounting holes are suitable
      for 3mm hex screws.  The mounting holes are 25mm apart (suited to attach to a DIN rale connector.)  A second DIN connector would be 85 mm.
    This STL file is MIT Licence. And freely can be used and distributed.

    