from flask import Flask, render_template, request
from flask_socketio import send, emit
from flask_graphql import GraphQLView

from app import app, socketio

# app imports
from utils.users import user_connect, user_disconnect, get_room_users, get_current_user
from utils.messages import format_message
from models.schema import schema

bot_name = 'Admin'

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/chat')
def get_chat():
    return render_template('chat.html')

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@socketio.on('connect')
def init_connection():
    print('A connection has been initiated')

@socketio.on('chatMessage')
def chat_message(message):
    user = get_current_user(request.sid)
    emit('message', format_message(user["username"], message), broadcast=True)

@socketio.on('joinRoom')
def joinRoom(data):
    # create user object
    user = user_connect(
        uid=request.sid,
        username=data['username'],
        room=data['room']
    )

    # welcome current user
    emit('message', format_message(bot_name, f'Welcome to {user["room"]}'), broadcast=False)

    # broadcast user
    emit('message', format_message(bot_name, f'{user["username"]} has joined {user["room"]}'), broadcast=True)
    # send room info
    emit('roomUsers', {
        'room': user["room"],
        'users': get_room_users(user["room"])
    }, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    user = user_disconnect(uid=request.sid)
    if user:
        emit('message', format_message(bot_name, f'{user["username"]} has left the chat'), broadcast=True)
        emit('roomUsers', {
            'room': user["room"],
            'users': get_room_users(user["room"])
        }, broadcast=True)

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 3001,
        debug=True
    )
    