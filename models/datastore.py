bots = []
rooms = []

def get_bot_phrases_by_name(name):
    for bot in bots:
        if bot['name'] == name:
            return bot['phrases']
    return 'Not Found'