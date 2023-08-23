document.addEventListener('DOMContentLoaded', function () {
    const chatArea = document.getElementById('chat-area');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    // Function to add a chat message to the chat area
    function addChatMessage(message, isUser) {
        const chatMessage = document.createElement('div');
        chatMessage.className = isUser ? 'user-chat-message' : 'bot-chat-message';
        chatMessage.textContent = message;
        chatArea.appendChild(chatMessage);
    }

    // Function to handle sending a chat message
    function sendChatMessage() {
        const userMessage = chatInput.value;
        if (userMessage) {
            addChatMessage(userMessage, true);
            chatInput.value = ''; // Clear the input field

            // Send user's message to the server
            fetch('/submit_chat', {
                method: 'POST',
                body: new URLSearchParams({ user_message: userMessage }),
            })
            .then(response => response.json())
            .then(data => {
                const botResponse = data.bot_response;
                addChatMessage(botResponse, false);
            })
            .catch(error => {
                console.error('Error sending message:', error);
            });
        }
    }

    // Event listener for sending chat message
    sendButton.addEventListener('click', sendChatMessage);

    // Event listener for Enter key in chat input
    chatInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            sendChatMessage();
        }
    });
});

// Event listener for sending chat message
sendChatButton.addEventListener('click', () => {
    // Get the chat input text
    const userInput = chatInput.value;
    if (userInput) {
        addChatMessage(userInput, true);
        chatInput.value = ''; // Clear the input field
        sendChatMessage(userInput);
    }
});

// Event listener for Enter key in chat input
chatInput.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        // Get the chat input text
        const userInput = chatInput.value;
        if (userInput) {
            addChatMessage(userInput, true);
            chatInput.value = ''; // Clear the input field
            sendChatMessage(userInput);
        }
    }
});

// Event listener for generate prompt button
generatePromptButton.addEventListener('click', async () => {
    // Call a function to generate and display the prompt
    const generatedPrompt = generatePrompt(); // Implement the generatePrompt function

    // Display the generated prompt in the prompt box
    promptBox.innerHTML = generatedPrompt;
});

// Implement your own function to generate a prompt
function generatePrompt() {
    // Replace this with your logic to generate a prompt
    return 'Sample prompt generated here';
}
