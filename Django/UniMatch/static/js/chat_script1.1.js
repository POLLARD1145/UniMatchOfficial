// Global Variables
var messagesArea = document.getElementById("messages-container");
var userInput = document.getElementById("message-input");
var sessionID = getSessionID(); // Get the session ID from session storage

// Function to load chat history from session storage
function loadChatHistory() {
    var chatHistory = JSON.parse(sessionStorage.getItem("chatHistory")) || [];
    var storedSessionID = sessionStorage.getItem("sessionID");

    // Load chats only if the session ID matches
    if (storedSessionID && storedSessionID === sessionID) {
        chatHistory.forEach(messageObj => {
            if (messageObj.type === "user") {
                appendUserMessage(messageObj.message);
            } else if (messageObj.type === "bot") {
                appendBotMessage(messageObj.message);
            }
        });
    } else {
        clearChatHistory(); // Clear chat history if the session ID doesn't match
    }
}

// Function to save chat history to session storage
function saveChatHistory(type, message) {
    var chatHistory = JSON.parse(sessionStorage.getItem("chatHistory")) || [];
    chatHistory.push({ type: type, message: message });
    sessionStorage.setItem("chatHistory", JSON.stringify(chatHistory));
}

// Function to get or generate a session ID
function getSessionID() {
    var storedSessionID = sessionStorage.getItem("sessionID");
    if (!storedSessionID) {
        // Generate a new session ID if not present
        storedSessionID = generateSessionID();
        sessionStorage.setItem("sessionID", storedSessionID);
    }
    return storedSessionID;
}

// Function to generate a unique session ID
function generateSessionID() {
    return 'session-' + Math.random().toString(36).substr(2, 16);
}

// Function to send a message when user presses Enter or clicks send button
function userMessage() {
    if (userInput.value.trim() !== "") {
        sendMessage();
    }
}

// Function to send the user message and handle the bot's response
function sendMessage() {
    var userMessage = userInput.value.trim();
    if (userMessage === "") return;

    appendUserMessage(userMessage);
    saveChatHistory("user", userMessage); // Save user message
    userInput.value = "";
    document.getElementById("greeting-text").style.display = "none";
    scrollChatsToBottom();

    // Send the user message to the backend
    fetch('/get_bot_response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Django CSRF token if needed
        },
        body: JSON.stringify({ message: userMessage, sessionID: sessionID }) // Send session ID with the message
    })
    .then(response => response.json())
    .then(data => {
        // Append the bot's response to the chat
        appendBotMessage(data.botMessage);
        saveChatHistory("bot", data.botMessage); // Save bot message
        scrollChatsToBottom();

        // If feedback is requested, ask for feedback
        if (data.feedbackRequested) {
            askForFeedback();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Event listener for Enter key press
userInput.addEventListener('keypress', function(event) {
    if (event.key === "Enter") {
        userMessage();
    }
});

// Create a new user message div
function appendUserMessage(message) {
    var userMessageContainer = document.createElement("div");
    userMessageContainer.className = "user-message";
    userMessageContainer.textContent = message;
    messagesArea.appendChild(userMessageContainer);
}

// Create a new bot message div and render markdown content with typewriter effect
function appendBotMessage(message) {
    var converter = new showdown.Converter();
    var htmlContent = converter.makeHtml(message);

    var botMessageContainer = document.createElement("div");
    botMessageContainer.className = "bot-response bot-response-content";
    messagesArea.appendChild(botMessageContainer);

    let index = 0;
    let tempContent = '';

    function type() {
        if (index < htmlContent.length) {
            tempContent += htmlContent.charAt(index);
            botMessageContainer.innerHTML = tempContent; // Render full HTML content periodically
            index++;
            scrollChatsToBottom();
            setTimeout(type, 0.01); // Reduced delay for faster typing speed
        }
    }
    type();
}

// Scroll chat area to the bottom
function scrollChatsToBottom() {
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Function to adjust chat container padding
function setMessagesContainerPadding() {
    var inputAreaHeight = document.getElementById('input-area-container').offsetHeight;
    var chatsArea = document.getElementById('chats-area-container');
    chatsArea.style.bottom = (inputAreaHeight) + 'px';
    chatsArea.style.marginBottom = 900 + 'px';
}

// Initial setup for message container padding and load chat history
document.addEventListener('DOMContentLoaded', function() {
    setMessagesContainerPadding();
    loadChatHistory(); // Load chat history on page load
});

// Adjust padding when window is resized
window.addEventListener('resize', function() {
    setMessagesContainerPadding();
});

// Helper function to get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to ask for user feedback
function askForFeedback() {
    let feedback = prompt("How would you rate this response? (1-5)");
    if (feedback <= 3) {
        let additionalFeedback = prompt("What would you like to see improved?");
        console.log(additionalFeedback);
    }
    if (feedback > 3) {
        let additionalFeedback = prompt("Would you like to provide additional feedback?");
        console.log(additionalFeedback);
    }
}

// Function to handle logout
function handleLogout() {
    clearChatHistory(); // Clear chat history on logout
    sessionStorage.removeItem("sessionID"); // Clear session ID on logout
    window.location.href = "/logout/";
}

// Function to clear chat history
function clearChatHistory() {
    sessionStorage.removeItem("chatHistory");
}
