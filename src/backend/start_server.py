#!/usr/bin/env python

import os
import sys

# Add your project's root directory to the Python path
# so imports will work correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from daphne.server import Server
from twisted.internet import reactor

# Get the ASGI application entry point
# Replace 'your_project_name' with your actual project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
from server.asgi import application as asgi_application

# You can configure server parameters here
HOST = "127.0.0.1"
PORT = 8000

# Create an instance of the Daphne server with proper parameters
server = Server(
    application=asgi_application,
    endpoints=[f"tcp:port={PORT}:interface={HOST}"]
)

if __name__ == "__main__":
    print(f"Starting Daphne server at http://{HOST}:{PORT}/...")
    # Run the server using Twisted's reactor
    server.run()