from flask import Flask, render_template, request
from flask_socketio import send, emit, join_room, leave_room
from flask_graphql import GraphQLView
import json
import random

from app import app, socketio

# app imports
from utils.users import user_connect, user_disconnect, get_room_users, get_current_user
from utils.messages import format_message
from models.schema import schema

bot_name = 'Admin'

@app.route('/')
def hello_world():
    rooms_query = '''
        {
            allRooms {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
    '''
    try:
        result = schema.execute(rooms_query)
    except Exception as err:
        print(f'There was an error performing a graphql query for {rooms_query}. Error: {err}')
    rooms = result.data['allRooms']['edges']
    return render_template('index.html', rooms=rooms)

@app.route('/api/postbotmessage', methods=['POST'])
def post_bot_message():
    data = request.get_json()
    # data = json.loads(data)
    bot_name = data['botName']
    bot_phrases = [
        'I want chicken',
        'I want liver',
        'Meow Mix meow mix',
        'Please deliver'
    ]
    bot_phrase = random.choice(bot_phrases)
    socketio.emit(
        'message', 
        format_message(bot_name, bot_phrase), 
        broadcast=True
    )
    return 'Success'

@app.route('/chat')
def get_chat():
    chats_query='''
        {
            allBots {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
    '''
    
    try:
        result = schema.execute(chats_query)
    except Exception as err:
        print(f'There was an error performing a graphql query for {rooms_query}. Error: {err}')
    bots = result.data['allBots']['edges']
    return render_template('chat.html', bots=bots)

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
    room = user["room"]
    emit(
        'message', 
        format_message(user["username"], message), 
        broadcast=True,
        room=room
    )

@socketio.on('joinRoom')
def joinRoom(data):
    # create user object
    user = user_connect(
        uid=request.sid,
        username=data['username'],
        room=data['room']
    )  

    #since we'll use the room option often, we'll extract the room name
    #maybe change to ids in the future
    room = user["room"]

    join_room(user["room"])

    # welcome current user
    emit(
        'message', 
        format_message(bot_name, f'Welcome to {room}'), 
        broadcast=False
    )

    # broadcast user
    emit(
        'message', 
        format_message(bot_name, f'{user["username"]} has joined {user["room"]}'), 
        broadcast=True,
        room=room
    )
    # send room info
    emit(
        'roomUsers', 
        {'room': room, 'users': get_room_users(room)}, 
        broadcast=True,
        room=room)

@socketio.on('disconnect')
def disconnect():
    user = user_disconnect(uid=request.sid)
    if user:
        emit(
            'message', 
            format_message(bot_name, f'{user["username"]} has left the chat'), 
            broadcast=True,
            room=room
        )
        emit(
            'roomUsers', 
            {'room': user["room"],'users': get_room_users(user["room"])}, 
            broadcast=True,
            room=room)

if __name__ == '__main__':
    socketio.run(app, port=3001, debug=True)