let token = localStorage.getItem("access");
let socket = null;
let currentUsername = "";

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access");
    if (token) {
        fetch("/chat/api/auth/users/me/", {
            headers : { "Authorization": `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                currentUsername = data.username;
                console.log("Автоматически вошли как ", data.username);
                document.getElementById("user").innerHTML = currentUsername;
                document.getElementById("auth").style.display = "none";
                document.getElementById("chat").style.display = "block";
                loadRooms();
            } else {
                localStorage.removeItem("access");
            }
        });
    }
});

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/chat/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("access", data.access);
        token = data.access;
        currentUsername = username;
        document.getElementById("user").innerHTML = currentUsername;
        document.getElementById("auth").style.display = "none";
        document.getElementById("chat").style.display = "block";
        loadRooms();
    } else {
        alert("Ошибка авторизации");
    }
}

async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/chat/api/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        alert("Регистрация успешна, теперь войдите");
    } else {
        alert("Ошибка регистрации");
    }
}

// Функция для загрузки комнат

async function loadRooms() {
    const response = await fetch("/chat/api/rooms/", {
        headers: { "Authorization": `Bearer ${token}` }
    });
    const rooms = await response.json();
    console.log("Полученные комнаты:", rooms);

    const roomList = document.getElementById("roomList");
    roomList.innerHTML = "";
    rooms.forEach(room => {
        const li = document.createElement("li");
        li.textContent = `${room.name} - ${room.id}`;
        li.onclick = () => joinRoom(room.name);

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = `❌ ${room.id}`;
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            deleteRoom(room.id);
        };

        li.appendChild(deleteBtn);
        roomList.appendChild(li);
    });
}

async function createRoom() {
    const roomName = document.getElementById("roomName").value;

    const response = await fetch("/chat/api/rooms/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name: roomName })
    });

    if (response.ok) {
        loadRooms();
    } else {
        alert("Ошибка создания комнаты");
    }
}

async function deleteRoom(roomId) {
    console.log("Удаляем комнату с идентификатором:", roomId);
    const response = await fetch(`/chat/api/rooms/${roomId}/`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        loadRooms();
    } else {
        alert("Ошибка удаления комнаты");
    }
}

async function joinRoom(roomName) {
    document.getElementById("messagesContainer").style.display = "block";
    document.getElementById("roomTitle").textContent = roomName;

    if (socket) {
        console.log("Закрываем существующее подключение");
        socket.close();
        console.log("Существующее подключение закрыто, websocket:", socket);
    } else if (!socket) {
        console.log("Нет существующего подключения, websocket:", socket);
    }

    console.log("Используемый токен:", token);
    socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/?token=${token}`);
    if (socket) {
        console.log("Подключаемся к комнате:", roomName);
    } else if (!socket) {
        console.log("Не удалось подключиться к комнате");
    }

    socket.onopen = () => console.log("WebSocket открыт");
    socket.onclose = () => console.log("WebSocket закрыт");
    socket.onerror = (error) => console.error("WebSocket ошибка:", error);

    console.log("WebSocket статус после создания:", socket);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const messages = document.getElementById("messages");
        const messageElement = document.createElement("p");
        messageElement.textContent = `${data.user}: ${data.message}`;
        messages.appendChild(messageElement);
    };
}

function leaveRoom() {
    socket.close();
    document.getElementById("messagesContainer").style.display = "none";
}

// 🔹 Отправка сообщения
function sendMessage() {
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value;

    if (message && socket) {
        const messageData = { message, user: currentUsername };
        socket.send(JSON.stringify(messageData));
        displayMessage(currentUsername, message);
        messageInput.value = "";
    }
}

// 🔹 Вывод сообщений в чат
function displayMessage(user, message) {
    const messages = document.getElementById("messages");
    const messageElement = document.createElement("p");
    messageElement.innerHTML = `<strong>${user}:</strong> ${message}`;
    messageElement.className = "msg-right";
    messages.appendChild(messageElement);
}

function logout() {
    localStorage.removeItem("access");
    token = null;
    currentUsername = "";
    document.getElementById("user").innerHTML = "";
    document.getElementById("auth").style.display = "block";
    document.getElementById("chat").style.display = "none";
}