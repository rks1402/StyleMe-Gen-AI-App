// JavaScript code for adding messages
function addBotMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.classList.add('message', 'bot-message');
    chatBox.appendChild(messageElement);
    // Scroll chat box to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addCustomerMessage(message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.classList.add('message', 'customer-message');
    chatBox.appendChild(messageElement);
    // Clear the input field
    document.getElementById('user-input').value = '';
    // Scroll chat box to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Event listener for the send button
document.getElementById('send-button').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput) {
        addCustomerMessage(userInput);
        // Here, you would typically call a function to process the user's input and get a bot response
        // For now, I'll simulate a bot response after a short delay
        setTimeout(function() {
            addBotMessage("Here's a stylish dress recommendation for you!");
        }, 1000);
    }
});


