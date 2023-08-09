const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);

function sendMessage() {
    const message = userInput.value;
    
    if (message.trim() !== '') {
        displayMessage('user', message);
        // Replace this with your chatbot's response logic
        setTimeout(() => displayMessage('bot', 'Hi,I am your Fashion Advisor, How may I assist you?'), 1500);
        
        userInput.value = '';
    }
}

function displayMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender);
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
