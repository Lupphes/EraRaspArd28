""" Script for managing and creating JSON database
Features - creates database, appends to database, read/initialize database
MIT License """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import json
import datetime


class DatabaseJSON():
    """ Creates and manages database updated """

    def __init__(self):
        self.dir_path = os.path.dirname(
            os.path.realpath(__file__))    # = /var/www/server
        self.json_path = os.path.join(self.dir_path, 'database.json')
        self.last_update = time.time()

    def _get_database_json(self):
        """ Reads data from file and format them into dictionary, which also returns. """
        with open(self.json_path, 'r') as file:
            return json.load(file)

    def _initialize_database(self):
        """ Creates the core of database structure.
        Creates JSON file in same directory with these values. """

        print('Database initialized here:')
        print(self.json_path)

        with open(self.json_path, 'w+') as file:
            json.dump({
                'lastEntry': {
                    'analog': {},
                    'digital': {
                        'led': 0
                    }
                },
                'entries': {}
            }, file, indent=4, sort_keys=True)
	return self._get_database_json()

    def update_database(self, dictionary):
        """ Loads the data from database JSON file.
        Gets actual data from dictionary variable.
        Append ActualData from dictionary to PastData. Then reset update.
        Dumps data to JSON and updates the file. """

        data = self._get_database_json()

        if (time.time() - self.last_update) >= 10:
            print('Time of logged value')
            timestamp = datetime.datetime.utcnow().strftime('%y-%m-%d-%H-%M-%S.%f')
            print(timestamp + ' - data stored')
            data['entries'].update({timestamp: dictionary['lastEntry']})
            print(str(data))
            self.last_update = time.time()

        data['lastEntry'].update(dictionary['lastEntry'])

        with open(self.json_path, 'w') as data_file:
            json.dump(data, data_file, indent=4, sort_keys=True)

    def get_database_data(self):
        """ Execute initialiseDatabase function If the database file does not exists.
        Opens the database file.
        Format data from JSON to dictionary.
        Return the dictionary. """

        return self._get_database_json() if os.path.isfile(
            self.json_path) else self._initialize_database()

