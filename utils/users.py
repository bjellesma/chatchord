users = []

# Join user to chat
def user_connect(uid, username, room):
    user = {
        'uid': uid,
        'username': username,
        'room': room
    }
    users.append(user)
    return user

# Get current user by id
def get_current_user(uid):
    for i in range(len(users)):
        if users[i]["uid"] == uid:
            return users[i]

# Remove user from list
def user_disconnect(uid):
    # Expense operation, remove later
    for i in range(len(users)):
        if users[i]["uid"] == uid:
            del users[i]

    return users

# Get current users in room
def get_room_users(room):
    room_users = [user for user in users if user['room'] == room]
    return room_users