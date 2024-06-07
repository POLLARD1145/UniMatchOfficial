
        // Function to add a new message div
        function sendMessage() {
            alert("button clicked");
            /*var messageContainer = document.getElementById('messages-container');
            var newMessage = document.createElement('div');
            newMessage.textContent = message;
            newMessage.classList.add(sender);
            messageContainer.appendChild(newMessage);*/
        }
        userInput = document.getElementById("message-input");
        userInput.addEventListener('keypress', function(event) {
            if (event.keyCode === 13 || event.key === "Enter") {
                alert("Enter key pressed");
                // You can add your logic here to handle the Enter key press
            }
        });

        
        /*
        // Function to handle user input
        function handleUserInput() {
            var userInput = document.getElementById('message-input').value;
            addMessage(userInput, 'user');

            // Simulate bot response (replace with actual bot response)
            var botResponse = "This is a bot response.";
            addMessage(botResponse, 'bot');

            // Clear input field
            document.getElementById('message-input').value = '';
        }

        // Event listener for Send Message button click
        document.getElementById('send-message-button').addEventListener('click', function() {
            handleUserInput();
        });

        // Event listener for Enter key press
        document.getElementById('message-input').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                handleUserInput();
            }
        });
    */