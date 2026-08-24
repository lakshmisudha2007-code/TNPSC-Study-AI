// ==========================================
// GET HTML ELEMENTS
// ==========================================

const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const chatContainer = document.getElementById("chatContainer");
const languageSelect = document.getElementById("languageSelect");
const newChatBtn = document.querySelector(".new-chat-btn");


// ==========================================
// SEND BUTTON
// ==========================================

sendBtn.addEventListener("click", sendMessage);


// ==========================================
// ENTER KEY
// ==========================================

userInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }

});


// ==========================================
// SEND MESSAGE
// ==========================================

async function sendMessage() {

    const message = userInput.value.trim();

    // Empty message
    if (message === "") {
        return;
    }


    // Show user message
    addUserMessage(message);


    // Clear input
    userInput.value = "";


    // Get selected language
    const selectedLanguage = languageSelect.value;


    // Show typing
    showTyping();


    try {

        // ==================================
        // SEND MESSAGE TO PYTHON BACKEND
        // ==================================

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: message,

                language: selectedLanguage

            })

        });


        // Convert response to JSON
        const data = await response.json();


        // Remove typing
        removeTyping();


        // ==================================
        // SHOW BOT RESPONSE
        // ==================================

        if (data.success) {

            addBotMessage(data.reply);

        } else {

            addBotMessage(
                data.reply || "Something went wrong. Please try again."
            );

        }


    } catch (error) {

        console.error("Backend Error:", error);

        removeTyping();

        addBotMessage(
            "Backend connection problem. Please check whether Python server is running."
        );

    }

}


// ==========================================
// ADD USER MESSAGE
// ==========================================

function addUserMessage(message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        "user-message"
    );


    const contentDiv = document.createElement("div");

    contentDiv.classList.add("message-content");


    const paragraph = document.createElement("p");

    paragraph.textContent = message;


    contentDiv.appendChild(paragraph);


    const avatarDiv = document.createElement("div");

    avatarDiv.classList.add(
        "avatar",
        "user-avatar"
    );


    avatarDiv.innerHTML = `
        <i class="fa-solid fa-user"></i>
    `;


    messageDiv.appendChild(contentDiv);

    messageDiv.appendChild(avatarDiv);


    chatContainer.appendChild(messageDiv);


    scrollToBottom();

}


// ==========================================
// ADD BOT MESSAGE
// ==========================================

function addBotMessage(message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        "bot-message"
    );


    const avatarDiv = document.createElement("div");

    avatarDiv.classList.add(
        "avatar",
        "bot-avatar"
    );


    avatarDiv.innerHTML = `
        <i class="fa-solid fa-robot"></i>
    `;


    const contentDiv = document.createElement("div");

    contentDiv.classList.add("message-content");


    const paragraph = document.createElement("p");

    // Convert line breaks into separate lines
    paragraph.innerHTML = escapeHTML(message)
        .replace(/\n/g, "<br>");


    contentDiv.appendChild(paragraph);


    messageDiv.appendChild(avatarDiv);

    messageDiv.appendChild(contentDiv);


    chatContainer.appendChild(messageDiv);


    scrollToBottom();

}


// ==========================================
// PROTECT BOT TEXT
// ==========================================

function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


// ==========================================
// TYPING ANIMATION
// ==========================================

function showTyping() {

    // Avoid duplicate typing message
    if (document.getElementById("typingMessage")) {
        return;
    }


    const typingDiv = document.createElement("div");

    typingDiv.classList.add(
        "message",
        "bot-message"
    );


    typingDiv.id = "typingMessage";


    typingDiv.innerHTML = `

        <div class="avatar bot-avatar">

            <i class="fa-solid fa-robot"></i>

        </div>

        <div class="message-content typing">

            <span></span>
            <span></span>
            <span></span>

        </div>

    `;


    chatContainer.appendChild(typingDiv);


    scrollToBottom();

}


// ==========================================
// REMOVE TYPING ANIMATION
// ==========================================

function removeTyping() {

    const typingMessage =
        document.getElementById("typingMessage");


    if (typingMessage) {

        typingMessage.remove();

    }

}


// ==========================================
// SCROLL CHAT TO BOTTOM
// ==========================================

function scrollToBottom() {

    chatContainer.scrollTop =
        chatContainer.scrollHeight;

}


// ==========================================
// QUICK QUESTION BUTTONS
// ==========================================

const quickButtons =
    document.querySelectorAll(".quick-btn");


quickButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        userInput.value = button.textContent.trim();

        sendMessage();

    });

});


// ==========================================
// NEW CHAT
// ==========================================

if (newChatBtn) {

    newChatBtn.addEventListener("click", function () {

        const messages =
            chatContainer.querySelectorAll(".message");


        // Keep first welcome bot message
        messages.forEach(function (message, index) {

            if (index > 0) {

                message.remove();

            }

        });


        userInput.value = "";

        userInput.focus();

    });

}


// ==========================================
// INPUT FOCUS
// ==========================================

userInput.focus();