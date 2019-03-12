"""  Main application for python web server
Features - showing data collected from arduino
MIT License """
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import core functions
import traceback
import os
import sys
import time

from threading import Thread, Event

from flask import Flask, make_response, redirect, render_template, request, url_for
from flask_socketio import SocketIO

from pyduino import Arduino
from database_json import DatabaseJSON

# Setting up the application
application = Flask(__name__)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
if DIR_PATH not in sys.path:
    sys.path.insert(0, DIR_PATH)

application.config['SECRET_KEY'] = os.urandom(28)
socketio = SocketIO(application)

# Initialize SocketIO
thread = Thread()
thread_stop_event = Event()

# Initialize connection to Arduino
a = Arduino()
time.sleep(3)

# Pins declaration
LED_PIN = 13
TEMP_INSIDE_PIN = 0
TEMP_OUTSIDE_PIN = 0
SOIL_PIN = 0
HUMIDITY_PIN = 0
LIGHT_INTENSITY_PIN = 0
WRITE_PIN = 2

# Setting up the pins
a.set_pin_mode(LED_PIN, 'O')
a.set_pin_mode(TEMP_INSIDE_PIN, 'I')
a.set_pin_mode(TEMP_OUTSIDE_PIN, 'I')
a.set_pin_mode(SOIL_PIN, 'I')
a.set_pin_mode(HUMIDITY_PIN, 'I')
a.set_pin_mode(LIGHT_INTENSITY_PIN, 'I')
a.set_pin_mode(WRITE_PIN, 'O')
print('Arduino and pins initialized')

# Database initialization
dat = DatabaseJSON()
database = dat.get_database_data()
print('Database initialized')

dataA = database['lastEntry']['analog']
dataD = database['lastEntry']['digital']

time.sleep(1)  # Waits for data load

# Setting up values from database
if 'led' in dataD:
    a.digital_write(LED_PIN, dataD['led'])
if 'userTemp' in dataA:
    a.analog_write(WRITE_PIN, dataA['userTemp'])


class ReadAnalogValues(Thread):
    """ Class which has init function, which reads data from arduino and push them into dictionary
    It keeps executing, because of socket which communicate with .js file in webpage. """

    def __init__(self):
        self.delay = 1  # Needs delay :c
        super(ReadAnalogValues, self).__init__()

    def get_analog_value(self):
        # Reads values from arduino
        print("Reading values")

        while not thread_stop_event.isSet():
            # List of analog pins which their information needs to be stored
            tempInEntry = a.analog_read(TEMP_INSIDE_PIN)
            tempOutEntry = a.analog_read(TEMP_OUTSIDE_PIN)
            soilEntry = a.analog_read(SOIL_PIN)
            humidityEntry = a.analog_read(HUMIDITY_PIN)
            lightIntensityEntry = a.analog_read(LIGHT_INTENSITY_PIN)

            # Send data to dictionary
            dataA['inTemp'] = tempInEntry
            dataA['outTemp'] = tempOutEntry
            dataA['soil'] = soilEntry
            dataA['humidity'] = humidityEntry
            dataA['lightIntensity'] = lightIntensityEntry
            
            socketio.emit('newnumber', {'number': tempInEntry}, namespace='/test')  # Socket thread
            dat.update_database(database)  # Upload data to JSON file
            time.sleep(self.delay)

    def run(self):
        self.get_analog_value()


def displayErrorHTML(error):
    # Formats an error in HTML for debugging on web page
    err = "<p>PYTHON ERROR</p>"
    err += "<pre>" + error + "</pre>"
    return err


@application.errorhandler(500)
def internalServerError(error):
    err = "<p>ERROR! 500</p>"
    err += "<pre>" + str(error) + "</pre>"
    err += "<pre>" + str(traceback.format_exc()) + "</pre>"
    return err

# Renders main page
@application.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'turnon' in request.form:
            print('LED TURNED ON')
            dataD['led'] = 1
            a.digital_write(LED_PIN, 1)
        elif 'turnoff' in request.form:
            print('LED TURNED OFF')
            dataD['led'] = 0
            a.digital_write(LED_PIN, 0)
        elif 'setTemp' in request.form:
            print('Setting temp')
            try:
                userTemp = float(request.form['temperature_val'])
                dataA['userTemp'] = userTemp
                a.analog_write(WRITE_PIN, dataA['userTemp'])
                print('User set temperature to ' + str(userTemp))
            except ValueError:
                print('User did not write a number')
        else:
            pass

    # Sends info into database
    dat.update_database(database)

    # Renders the final template with given variables
    return render_template('index.html')


@application.route('/data', methods=['POST', 'GET'])
def data():
    userTemp = ''
    return render_template('data.html', setTemp=dataA['userTemp'] if 'userTemp' in dataA else userTemp, tempInEntry='Loading...', tempOutEntry='Loading...', soilEntry='Loading...', humidityEntry='Loading...', lightIntensityEntry='Loading...')

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
@application.route('/turnon', methods=['GET'])
def turn_on():
    # turn on LED on arduino
    dataD['led'] = 1
    a.digital_write(LED_PIN, 1)
    return redirect(url_for('index'))


@application.route('/turnoff', methods=['GET'])
def turn_off():
    # turn off LED on arduino
    dataD['led'] = 0
    a.digital_write(LED_PIN, 0)
    return redirect(url_for('index'))


# Data available in JSON format
@application.route('/api', methods=['GET'])
def api():
    with open(os.path.join(DIR_PATH, 'database.json')) as json_file:
        data = json_file.read()
        response = make_response(data)
        response.headers['Content-Type'] = 'application/json'
        return response


# Run the app
if __name__ == "__main__":
    socketio.run(application)
    application.debug = True
    application.run('0.0.0.0')
