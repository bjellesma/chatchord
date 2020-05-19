const chatForm = document.getElementById('chat-form');
const chatMessages = document.querySelector('.chat-messages');
const roomName = document.getElementById('room-name');
const userList = document.getElementById('users');

interface HTMLInputEvent extends Event {
    target: HTMLInputElement & EventTarget;
}

// Get username and room from URL



if(document.getElementById('chatRoom')){
  //@ts-ignore
  const userToken = Qs.parse(location.search, {
    ignoreQueryPrefix: true
  });
  //@ts-ignore
  const socket = io.connect({transports: ['websocket']});

  // Join chatroom
  socket.on('connect', function(){
    socket.emit('joinRoom', { userToken });
  })
  


  // Get room and users
  socket.on('roomUsers', ({ room, users }) => {
    outputRoomName(room);
    outputUsers(users);
  });

  // Message from server
  socket.on('message', message => {
    console.log('receiving message')
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

  // fetch call to /api/getbots
  fetch('/api/getbots',{
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  // need in between step to parse response
  .then(res => res.json())
  .then(bots => {
    document.getElementById('bots').innerHTML = `
      ${bots.map(bot => `<li class="botTalk">${bot.name}</li>`).join('')}
    `
  }).then(() => {
    // When the user clicks on a bot
    document.querySelectorAll('.botTalk').forEach((bot) => {
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
  })
}

  //submit button on main page
document.getElementById('submit').addEventListener('click', async function(event){
  const username = <HTMLInputElement>document.getElementById('username')
  const room = <HTMLSelectElement>document.getElementById('room')
  const data = {
    username: (username).value,
    room: (room).value
  }
  const auth_rooms = [
    'Office',
    'Conference Room'
  ]
  // TODO make an attribute on room object in database for if it requires auth
  // if the room that the user is entering requires login
  if(auth_rooms.includes(room.value)){
    // redirect to login page
    window.location.href = `/login?room=${room.value}&username=${username.value}`
  }else{
    //if login is not required, we can simply request to get a token from the main page
    const response = await fetch('/', {
      method: 'post',
      body: JSON.stringify(data),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    })
    const result = await response.json()
    window.location.href = `/chat?token=${result.token.toString()}`
  }
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
