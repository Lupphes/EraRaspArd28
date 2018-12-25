# databaseJSON.py
# Script for managing and creating JSON database
# Features - creates database, appends to database, read/initialize database
# MIT License

import json
import os.path
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__)) # = /var/www/server

updates = 0 # Counter of updates. Every 10th update is appended into database as (PastValue)

def getDatabaseJSON():
    """
    Reads the data from file  and format them to dictionary, which returns.
    """
    with open(dir_path + '/database.json', 'r') as f:
        data = json.load(f)
	return data

def initializeDatabase():
    """
    Creates the core of database structure.
    Creates JSON file in same directory with these values.
    """
    data = {}
    data['actValues'] = {
        'analog': {  },
        'digital': {
	    'led': 0
	}
    }
    data['pastValues'] = {}

    print('Database inicialized here:')
    print(dir_path + '/database.json')

    with open(dir_path + '/database.json', 'w+') as f:
        json.dump(data, f)

def updateDatabase(dict):
    """
    Loads the data from database JSON file.
    Gets actual data from dictionary varible.
    When update counter counts to 10. Append ActualData from dictionary to PastData. Then reset update.
    Dumps data to JSON and updates the file.
    """
    data = getDatabaseJSON()
    global updates

    if (updates == 10):
	print('Time of logged value')
        ts = datetime.datetime.utcnow().strftime('%y-%m-%d-%H-%M-%S.%f')[:-3]
	print(ts + ' - data stored')
        data['pastValues'].update({ts: {} })
        data['pastValues'][ts].update(dict['actValues'])
        updates = 0
	print(str(data))

    updates += 1

    data['actValues'].update(dict['actValues'])

    with open(dir_path + '/database.json', 'w') as f:
        f.write(json.dumps(data, f))

def getDatabaseData():
    """
    Execute initialiseDatabase function If the database file does not exists.
    Opens the databse file.
    Format data from JSON to dictionary.
    Return the dictionary.
    """

    if not os.path.isfile(dir_path + '/database.json'):
	initializeDatabase()

    dict = getDatabaseJSON()
    #print('Inicialized database with values:')
    #print(dict)
    return dict
