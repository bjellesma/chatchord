from flask import Flask, render_template
from flask_socketio import send
from app import app, socketio

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/chat')
def get_chat():
    return render_template('chat.html')

@socketio.on('connect')
def init_connection():
    print('A connection has been initiated')

@socketio.on('message')
def send_message(msg):
    send(f'message: {message}', broadcast=True)

@socketio.on('joinRoom')
def joinRoom(data):
    print(f'{data["username"]} has joined the room')
    send({
        'username': data["username"],
        'text': f'{data["username"]} has joined the room'
    })

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 3001,
        debug=True
    )
    