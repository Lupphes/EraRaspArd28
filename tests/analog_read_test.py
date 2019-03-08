""" Data read test
MIT License """
#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyduino import *
import time

if __name__ == '__main__':

    print('Establishing connection to Arduino...')

    # If your Arduino is running on a serial port other than '/dev/ttyACM0/'
    # Declare: a = Arduino(serial_port='/dev/ttyXXXX')
    a = Arduino()

    # Sleep to ensure ample time for computer to make serial connection
    time.sleep(3)
    print('Established!')

    # Define our LED pin
    PIN = 13

    # Initialize the digital pin as output
    a.set_pin_mode(PIN, 'O')

    # Allow time to make connection
    time.sleep(1)

    # Turn LED on
    a.digital_write(PIN, 1)

    for i in range(0, 1000):

        try:
            # Read the analog value from analogpin 0
            analog_val = a.analog_read(0)

            # Print value in range between 0-100
            print('ANALOG READ =', int((analog_val/1023.) * 100))
            time.sleep(1)

        except KeyboardInterrupt:
            break  # Kill for loop

    # To make sure we turn off the LED and close our serial connection
    print('CLOSING...')
    a.digital_write(PIN, 0)  # Turn LED off
    a.close()
