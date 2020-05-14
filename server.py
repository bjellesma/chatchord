from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_socketio import send, emit, join_room, leave_room
from flask_graphql import GraphQLView
from flask_login import current_user, login_user, logout_user #used for login
from models.models import UsersModel #used for login
import json
import random

from app import app, socketio

# app imports
from utils.users import user_connect, user_disconnect, get_room_users, get_current_user
from utils.messages import format_message
from models.schema import schema
from models.datastore import bots, get_bot_phrases_by_name
from secure import UserTokens

bot_name = 'Admin'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':      
        rooms_query = '''
            {
                allRooms {
                    edges {
                        node {
                            id
                            name
                            requiresAuth
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
    elif request.method == 'POST':
        data = request.get_json()
        username = data['username']
        room = data['room']
        # create jwt for an anonymous user
        json_web_token = UserTokens.create_token(username=username,room=room,anonyous=True)
        return jsonify({
            'token': json_web_token,
        })

@app.route('/api/postbotmessage', methods=['POST'])
def post_bot_message():
    data = request.get_json()
    # data = json.loads(data)
    bot_name = data['botName']
    bot_phrases = get_bot_phrases_by_name(bot_name)
    bot_phrase = random.choice(bot_phrases)
    socketio.emit(
        'message', 
        format_message(bot_name, bot_phrase), 
        broadcast=True
    )
    return 'Success'

@app.route('/chat', methods=['GET', 'POST'])
def get_chat():
    if request.method == 'GET':
        chats_query='''
            {
                allBots {
                    edges {
                        node {
                            id
                            name
                            phrases
                        }
                    }
                }
            }
        '''
        jwt = request.args.get('token')
        jwt_payload = UserTokens.read_token(jwt)
        username = jwt_payload.get('username')
        room = jwt_payload.get('room')
        try:
            result = schema.execute(chats_query)
        except Exception as err:
            print(f'There was an error performing a graphql query for {rooms_query}. Error: {err}')
        bots_graphql = result.data['allBots']['edges']
        # Load bots into datastore
        for bot in bots_graphql:
            bots.append(
                {
                    'name': bot['node']['name'],
                    'phrases': bot['node']['phrases']
                }
            )
        return render_template('chat.html', bots=bots, username=username, room=room)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        room = request.args.get('room')
        username = request.args.get('username')
        return render_template('login.html', room=room)
    elif request.method == 'POST':
        # if the user is already authenticated
        if current_user.is_authenticated:
            return redirect(url_for('get_chat'))
        username = request.form.get('username')
        password = request.form.get('password')
        room = request.form.get('roomName')
        user = UsersModel().find_user_by_username(username)
        # the existence of a user is checked first and then a password will be checked only if the user exists
        if user and user.check_password(password):
            login_user(user)
            # create jwt for an authenticated user
            json_web_token = UserTokens.create_token(username=username,room=room,anonymous=False)
            return redirect(url_for('get_chat', token=json_web_token))
        else:
            flash('Invalid username and/or password')
            return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET'
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        if username and len(username) == 4 and password == confirmPassword:
            user = UsersModel()
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

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
    user_token = data['userToken']['token']
    # decode token
    jwt_payload = UserTokens.read_token(user_token.encode())
    # create user object
    user = user_connect(
        uid=request.sid,
        username=jwt_payload.get('username'),
        room=jwt_payload.get('room')
    )  

    #since we'll use the room option often, we'll extract the room name
    #maybe change to ids in the future
    room = jwt_payload.get('room')

    join_room(room)

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