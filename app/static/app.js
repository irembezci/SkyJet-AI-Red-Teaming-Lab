const loginPage = document.getElementById("login-page");
const chatPage = document.getElementById("chat-page");

const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");

const userName = document.getElementById("user-name");

const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatMessages = document.getElementById("chat-messages");

const logoutButton = document.getElementById("logout-button");


async function checkSession() {
    try {
        const response = await fetch("/me", {
            credentials: "include"
        });

        if (!response.ok) {
            showLogin();
            return;
        }

        const user = await response.json();
        showChat(user);

    } catch (error) {
        showLogin();
    }
}


function showLogin() {
    loginPage.classList.remove("hidden");
    chatPage.classList.add("hidden");
}


function showChat(user) {
    loginPage.classList.add("hidden");
    chatPage.classList.remove("hidden");

    userName.textContent = `Signed in as ${user.name}`;
    messageInput.focus();
}


loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    loginError.textContent = "";

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            loginError.textContent = data.detail || "Login failed.";
            return;
        }

        showChat(data.user);

    } catch (error) {
        loginError.textContent = "Unable to connect to SkyJet AI.";
    }
});


chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            addMessage(data.detail || "Something went wrong.", "assistant");
            return;
        }

        addMessage(data.response, "assistant");

    } catch (error) {
        addMessage(
            "Unable to connect to SkyJet AI.",
            "assistant"
        );
    }
});


function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    message.appendChild(bubble);
    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


logoutButton.addEventListener("click", async () => {
    await fetch("/logout", {
        method: "POST",
        credentials: "include"
    });

    showLogin();
});


checkSession();