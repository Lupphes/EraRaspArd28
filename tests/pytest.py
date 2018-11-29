from pyduino import *
import time

if __name__ == '__main__':

    a = Arduino()
    # if your arduino was running on a serial port other than '/dev/ttyACM0/'
    # declare: a = Arduino(serial_port='/dev/ttyXX')

    time.sleep(3)
    # sleep to ensure ample time for computer to make serial connection

    PIN = 13
    a.set_pin_mode(PIN,'O')
    # initialize the digital pin as output

    time.sleep(1)
    # allow time to make connection

    for i in range(0,1000):
        if i%2 == 0:
            a.digital_write(PIN,1) # turn LED on
        else:
            a.digital_write(PIN,0) # turn LED off

        time.sleep(1)
