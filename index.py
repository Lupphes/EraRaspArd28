# index.py
# Main application for python web server
# Features - showing data collected from arduino
# MIT License

from flask_socketio import SocketIO, emit
from threading import Thread, Event

from flask import (
    Flask, make_response, redirect, render_template, request, url_for
)
from pyduino import *
import time
from time import sleep

application = Flask(__name__)

application.config['SECRET_KEY'] = 'secret!'
application.config['DEBUG'] = True
socketio = SocketIO(application)

import traceback
import os
import sys

thread = Thread()
thread_stop_event = Event()

CURRENTDIR = os.path.dirname(os.path.abspath(__file__))
if CURRENTDIR not in sys.path:
    sys.path.insert(0, CURRENTDIR)

# Initialize connection to Arduino
a = Arduino()
time.sleep(3)

# Pins declaration
LED_PIN = 13
ANALOG_PIN = 0

a.set_pin_mode(LED_PIN,'O')
print 'Arduino initialized'


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

class ReadAnalogValues(Thread):
    def __init__(self):
        self.delay = 1
        super(ReadAnalogValues, self).__init__()

    def getAnalogValue(self):
        # Reads values from arduino
        print("Reading values")
        while not thread_stop_event.isSet():
	    number = a.analog_read(ANALOG_PIN)
            socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)

    def run(self):
	self.getAnalogValue()

# Renders main page
@application.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':

        if request.form['submit'] == 'Turn On':
           print 'TURN ON'
           a.digital_write(LED_PIN,1)

        elif request.form['submit'] == 'Turn Off':
            print 'TURN ON'
            a.digital_write(LED_PIN,0)
        else:
            pass

    # Read ANALOG value from PIN
    analogData = 0 #a.analog_read(ANALOG_PIN)

    # Renders the final template with given variables
    return render_template('index.html', temp=analogData)

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


# Run the app
if __name__ == "__main__":
    socketio.run(application)
    application.debug = True
    application.run('0.0.0.0')

