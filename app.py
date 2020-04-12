#!/usr/bin/env python3.7
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['ENV'] = 'development'
app.secret_key = "any random string"
socketio = SocketIO(app)
