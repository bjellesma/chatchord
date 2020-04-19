# format message
import moment
from datetime import datetime

def format_message(username, text):
    return {
        'username': username,
        'text': text,
        'time': moment.now().format("MM/DD/YYYY")
    }