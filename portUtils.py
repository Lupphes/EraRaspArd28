# portUtils.py A simple helper class to get the data from serial port 
# until a CR LF
#
# MIT License


import os
import serial

# A simple class helper class for serial
class PortUtils():
    def __init__(self, port, baud):
        self.__serialPort = serial.Serial(port, baud)
	self.__serialPort.flushInput()

    # Read data from the port until a CRLF
    def read(self):
        buffer = ''
        CRLF = '\r\n' # Carriage Return Line Feed
        while True:
            buffer += self.__serialPort.read()
            if CRLF in buffer:
                buffer = buffer.split(CRLF)
                return buffer[0]

    # Write data to the serial port
    def write(self, data):
        self.__serialPort.write(data)

if __name__ == "__main__":
    print "You need to run this from a python script!"
