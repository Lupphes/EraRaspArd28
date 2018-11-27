# WSGI entry point for application
import sys
sys.path.insert(0, '/var/www/server/')
from index import application
