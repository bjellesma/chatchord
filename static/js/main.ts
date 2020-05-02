const chatForm = document.getElementById('chat-form');
const chatMessages = document.querySelector('.chat-messages');
const roomName = document.getElementById('room-name');
const userList = document.getElementById('users');

interface HTMLInputEvent extends Event {
    target: HTMLInputElement & EventTarget;
}

// Get username and room from URL
//@ts-ignore
const { username, room } = Qs.parse(location.search, {
  ignoreQueryPrefix: true
});

//@ts-ignore
var socket = io.connect();

  //submit button on main page
document.getElementById('submit').addEventListener('click', async function(event){
  const data = {
    username: (<HTMLInputElement>document.getElementById('username')).value,
    room: (<HTMLSelectElement>document.getElementById('room')).value
  }
  const response = await fetch('/', {
    method: 'post',
    body: JSON.stringify(data),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  const result = await response.json()
  window.location.href = '/chat'
})

// Get room and users
socket.on('roomUsers', ({ room, users }) => {
  outputRoomName(room);
  outputUsers(users);
});

// Message from server
socket.on('message', message => {
  outputMessage(message);
  // Scroll down
  chatMessages.scrollTop = chatMessages.scrollHeight;
});

// Message submit
chatForm.addEventListener('submit', e => {
  e.preventDefault();

  // Get message text
  const messageTextArea = (<HTMLTextAreaElement>document.getElementById('msg'))
  const msg = messageTextArea.value;

  // Emit message to server
  socket.emit('chatMessage', msg);

  // Clear input
  messageTextArea.value = '';
  messageTextArea.focus();
});



// When the user clicks on a bot
const bots = document.querySelectorAll('.botTalk')
bots.forEach((bot) => {
  bot.addEventListener('click', function(){
    const botData = {
      botName: this.innerHTML
    }
    fetch('/api/postbotmessage', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(botData)
    })
  })
})

// Output message to DOM
function outputMessage(message) {
  const div = document.createElement('div');
  div.classList.add('message');
  div.innerHTML = `<p class="meta">${message.username} <span>${message.time}</span></p>
  <p class="text">
    ${message.text}
  </p>`;
  document.querySelector('.chat-messages').appendChild(div);
}

// Add room name to DOM
function outputRoomName(room) {
  roomName.innerText = room;
}

// Add users to DOM
function outputUsers(users) {
  userList.innerHTML = `
    ${users.map(user => `<li>${user.username}</li>`).join('')}
  `;
}
