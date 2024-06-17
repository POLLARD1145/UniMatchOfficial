//GLOBAL Varriables
var messagesArea = document.getElementById("messages-container");
var userInput = document.getElementById("message-input");

        // Function to add a new message div
        function sendMessage() {
            userMessage = userInput.value;
            appendUserMessage(userMessage);
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
                body: JSON.stringify({ message: userMessage })
            })
            .then(response => response.json())
            .then(data => {
                // Append the bot's response to the chat
                appendBotMessage(data.botMessage);
                scrollChatsToBottom();
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        //add event listner to the input area to wait for the enter key to send the message
        userInput.addEventListener('keypress', function(event) {
            if (event.keyCode === 13 || event.key === "Enter") {
                sendMessage();
            }
        });

        //create a new user message div when a message is sent.
        function appendUserMessage(message){
            var userMessageContainer = document.createElement("div");
            userMessageContainer.className = "user-message"
            userMessageContainer.textContent = message;
            messagesArea.appendChild(userMessageContainer);
        }

        //create a new bot message div when a message is sent and feedback is received from the bot.
        function appendBotMessage(message){
            var botMessageContainer = document.createElement("div");
            botMessageContainer.className = "bot-response bot-response-content"
            botMessageContainer.innerHTML = message;
            messagesArea.appendChild(botMessageContainer);
        }

        function scrollChatsToBottom() {
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }
   

        // Function to set bottom margin of messages-container to match the height of input-area-container
function setMessagesContainerPadding() {
    var inputAreaHeight = document.getElementById('input-area-container').offsetHeight;
    var chatsArea = document.getElementById('chats-area-container');
    chatsArea.style.bottom = (inputAreaHeight) + 'px';
    chatsArea.style.marginBottom = 900 + 'px';
}

// Call the setMessagesContainerMargin function initially to set the bottom margin
document.addEventListener('DOMContentLoaded', function() {
    setMessagesContainerPadding();
});

// Event listener to adjust bottom margin of messages-container when window is resized
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
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}