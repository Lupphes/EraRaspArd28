# coreFunctions.py
# Main functions for this project
#
# MIT License

import os
import serial
import json
from portUtils import PortUtils;
CURRENTDIR = os.path.dirname(__file__)
BASEDIR = os.path.dirname(CURRENTDIR)

ardVar = {}
# Replaces part of a template with the data
class DisplayCore():
    def getData(self):
	port = PortUtils('/dev/ttyACM0', 9600)
        data = port.read()

	# Split the data into separate
        split = data.split(":")
        temp = split[0] # Temperature
        testVar = split[1] # Test

	ardVar.update({'temp':temp,'test':testVar})
	#ardVar.update({'temp': str(data)})

    def webUpdate(self):
	html = ''
	render_template('templates/index.html')
	#with open(CURRENTDIR + '/template.html') as template:
		#html = template.read()
        	#html = html.replace("%TEMP%", ardVar['temp'])
        	#html = html.replace("%TESTVAR%", ardVar['test'])
        return html

    def retJSON(self):
        ardVarJSON = json.dumps(ardVar)
	return ardVarJSON

if __name__ == "__main__":
	print "Err"
