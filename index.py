# index.py
# Main application for python web server
# Features - showing data collected from arduino
# MIT License

# Import core funtions
import traceback
import os
import sys

from threading import Thread, Event

from flask import Flask, make_response, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit

# Import supporting functions
import json
from time import sleep

# Import custom functions
from pyduino import *
from databaseJSON import updateDatabase, getDatabaseData, getDatabaseJSON

# Setting up the application
application = Flask(__name__)

application.config['SECRET_KEY'] = os.urandom(28)
application.config['DEBUG'] = True
socketio = SocketIO(application)

thread = Thread()
thread_stop_event = Event()

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
if CURRENTDIR not in sys.path:
    sys.path.insert(0, CURRENTDIR)

# Initialize connection to Arduino
a = Arduino()
sleep(3)

# Pins declaration
LED_PIN = 13
ANALOG_PIN = 0
WRITE_PIN = 2

# Setting up the pins
a.set_pin_mode(LED_PIN,'O')
a.set_pin_mode(ANALOG_PIN,'I')
a.set_pin_mode(WRITE_PIN,'O')
print 'Arduino and pins initialised'

# Database initialisation
database = getDatabaseData()
print('Databaze initialised with data:')
print(str(database))

sleep(1) # Waits for data load

# Setting up values from database
if 'led' in database['actValues']['digital']:
    a.digital_write(LED_PIN,database['actValues']['digital']['led'])
if 'userTemp' in database['actValues']['analog']:
    a.analog_write(WRITE_PIN,database['actValues']['analog']['userTemp'])

class ReadAnalogValues(Thread):
    """
    Class which has init funtion, which reads data from arduino and push them into dictionary
    It keeps executing, because of socket which communicate with .js file in webpage.
    """
    def __init__(self):
        self.delay = 1 # Needs delay :c
        super(ReadAnalogValues, self).__init__()

    def getAnalogValue(self):
        # Reads values from arduino
        print("Reading values")
        while not thread_stop_event.isSet():

    	    # List of analog pins which their information needs to be stored
	    currTemp = a.analog_read(ANALOG_PIN)

	    # Send data to dictionary
	    database['actValues']['analog']['actTemp'] = currTemp

	    socketio.emit('newnumber', {'number': currTemp}, namespace='/test') # Socket thread

	    updateDatabase(database) # Upload data to JSON file
            sleep(self.delay)

    def run(self):
	self.getAnalogValue()

# Renders main page
@application.route('/', methods = ['POST','GET'])
def index():
    userTemp = ''

    if request.method == 'POST':

        if 'turnon' in request.form:
            print 'LED TURNED ON'
	    database['actValues']['digital']['led'] = 1
            a.digital_write(LED_PIN,1)

        elif 'turnoff' in request.form:
            print 'LED TURNED OFF'
	    database['actValues']['digital']['led'] = 0
            a.digital_write(LED_PIN,0)

        elif 'setTemp' in request.form:
	    print 'Setting temp'
	    try:
   		userTemp = float(request.form['temperature_val'])
		database['actValues']['analog']['userTemp'] = userTemp
		a.analog_write(WRITE_PIN,database['actValues']['analog']['userTemp'])
   		print('User set temperature to ' + str(userTemp))
	    except ValueError:
   		print('User did not wrote a number')

        elif 'ledcheck' in request.form:
	    print 'LED check'
	    if database['actValues']['digital']['led'] == 1:
		database['actValues']['digital']['led'] = 0
	        a.digital_write(LED_PIN,0)
	    else:
		database['actValues']['digital']['led'] = 1
		a.digital_write(LED_PIN,1)
	else:
	    pass

    # Sends info into database
    updateDatabase(database)

    # Renders the final template with given variables
    return render_template('index.html', setTemp=database['actValues']['analog']['userTemp'] if 'userTemp' in database['actValues']['analog'] else userTemp, tempFromArd='Loading...')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the read from arduino only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = ReadAnalogValues()
	thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

# API
@application.route('/turnon', methods=['GET'] )
def turn_on():
    # turn on LED on arduino
    a.digital_write(LED_PIN,1)
    return redirect( url_for('index') )

@application.route('/turnoff', methods=['GET'] )
def turn_off():
    # turn off LED on arduino
    a.digital_write(LED_PIN,0)
    return redirect( url_for('index') )

def displayErrorHTML(error):
    # Formats an error in HTML for debugging on web page
    err = "<p>PYTHON ERROR</p>"
    err += "<pre>" + error + "</pre>"
    return err

@application.errorhandler(500)
def internalServerError(error):
    err = "<p>ERROR! 500</p>"
    err += "<pre>"+ str(error) + "</pre>"
    err += "<pre>"+ str(traceback.format_exc()) + "</pre>"
    return err

# Data available in JSON format
@application.route('/api', methods=['GET'])
def json():
    with open('/var/www/server/database.json') as json_file:
        data = json_file.read()
	response = make_response(data)
        response.headers['Content-Type'] = 'application/json'
        return response

# Run the app
if __name__ == "__main__":
    socketio.run(application)
    application.debug = True
    application.run('0.0.0.0')
