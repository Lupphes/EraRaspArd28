""" LED test
MIT License """
#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyduino import *
import time

if __name__ == '__main__':

    a = Arduino()
    # If your arduino is running on a serial port other than '/dev/ttyACM0/'
    # Declare: a = Arduino(serial_port='/dev/ttyXX')

    time.sleep(3)
    # Sleep to ensure ample time for computer to make serial connection

    PIN = 13
    a.set_pin_mode(PIN, 'O')
    # Initialize the digital pin as output

    time.sleep(1)
    # Allow time to make connection

    for i in range(0, 1000):
        if i % 2 == 0:
            a.digital_write(PIN, 1)  # Turn LED on
        else:
            a.digital_write(PIN, 0)  # Turn LED off

        time.sleep(1)
