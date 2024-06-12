//GLOBAL Varriables
var messagesArea = document.getElementById("messages-container");
var userInput = document.getElementById("message-input");

        // Function to add a new message div
        function sendMessage() {
            userMessage = userInput.value;
            appendUserMessage(userMessage);
            userInput.value = "";
            document.getElementById("greeting-text").style.display = "none";
            appendBotMessage("This is the message from the bot...");
            scrollChatsToBottom();
            /*var messageContainer = document.getElementById('messages-container');
            var newMessage = document.createElement('div');
            newMessage.textContent = message;
            newMessage.classList.add(sender);
            messageContainer.appendChild(newMessage);*/
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
            botMessageContainer.textContent = message;
            messagesArea.appendChild(botMessageContainer);
        }

        function scrollChatsToBottom() {
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }
   

        // Function to set bottom margin of messages-container to match the height of input-area-container
function setMessagesContainerPadding() {
    var inputAreaHeight = document.getElementById('input-area-container').offsetHeight;
    document.getElementById('chats-area-container').style.bottom = (inputAreaHeight) + 'px';
}

// Call the setMessagesContainerMargin function initially to set the bottom margin
document.addEventListener('DOMContentLoaded', function() {
    setMessagesContainerPadding();
});

// Event listener to adjust bottom margin of messages-container when window is resized
window.addEventListener('resize', function() {
    setMessagesContainerMargin();
});