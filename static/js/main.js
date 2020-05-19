var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var chatForm = document.getElementById('chat-form');
var chatMessages = document.querySelector('.chat-messages');
var roomName = document.getElementById('room-name');
var userList = document.getElementById('users');
// Get username and room from URL
if (document.getElementById('chatRoom')) {
    //@ts-ignore
    var userToken_1 = Qs.parse(location.search, {
        ignoreQueryPrefix: true
    });
    //@ts-ignore
    var socket_1 = io.connect('wss:?/chatchord.herokuapp.com', { transports: ['websocket'] });
    // Join chatroom
    socket_1.on('connect', function () {
        socket_1.emit('joinRoom', { userToken: userToken_1 });
    });
    // Get room and users
    socket_1.on('roomUsers', function (_a) {
        var room = _a.room, users = _a.users;
        outputRoomName(room);
        outputUsers(users);
    });
    // Message from server
    socket_1.on('message', function (message) {
        console.log('receiving message');
        outputMessage(message);
        // Scroll down
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
    // Message submit
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        // Get message text
        var messageTextArea = document.getElementById('msg');
        var msg = messageTextArea.value;
        // Emit message to server
        socket_1.emit('chatMessage', msg);
        // Clear input
        messageTextArea.value = '';
        messageTextArea.focus();
    });
    // fetch call to /api/getbots
    fetch('/api/getbots', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        // need in between step to parse response
        .then(function (res) { return res.json(); })
        .then(function (bots) {
        document.getElementById('bots').innerHTML = "\n      " + bots.map(function (bot) { return "<li class=\"botTalk\">" + bot.name + "</li>"; }).join('') + "\n    ";
    }).then(function () {
        // When the user clicks on a bot
        document.querySelectorAll('.botTalk').forEach(function (bot) {
            bot.addEventListener('click', function () {
                var botData = {
                    botName: this.innerHTML
                };
                fetch('/api/postbotmessage', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(botData)
                });
            });
        });
    });
}
//submit button on main page
document.getElementById('submit').addEventListener('click', function (event) {
    return __awaiter(this, void 0, void 0, function () {
        var username, room, data, auth_rooms, response, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    username = document.getElementById('username');
                    room = document.getElementById('room');
                    data = {
                        username: (username).value,
                        room: (room).value
                    };
                    auth_rooms = [
                        'Office',
                        'Conference Room'
                    ];
                    if (!auth_rooms.includes(room.value)) return [3 /*break*/, 1];
                    // redirect to login page
                    window.location.href = "/login?room=" + room.value + "&username=" + username.value;
                    return [3 /*break*/, 4];
                case 1: return [4 /*yield*/, fetch('/', {
                        method: 'post',
                        body: JSON.stringify(data),
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        }
                    })];
                case 2:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 3:
                    result = _a.sent();
                    window.location.href = "/chat?token=" + result.token.toString();
                    _a.label = 4;
                case 4: return [2 /*return*/];
            }
        });
    });
});
// Output message to DOM
function outputMessage(message) {
    var div = document.createElement('div');
    div.classList.add('message');
    div.innerHTML = "<p class=\"meta\">" + message.username + " <span>" + message.time + "</span></p>\n  <p class=\"text\">\n    " + message.text + "\n  </p>";
    document.querySelector('.chat-messages').appendChild(div);
}
// Add room name to DOM
function outputRoomName(room) {
    roomName.innerText = room;
}
// Add users to DOM
function outputUsers(users) {
    userList.innerHTML = "\n    " + users.map(function (user) { return "<li>" + user.username + "</li>"; }).join('') + "\n  ";
}
