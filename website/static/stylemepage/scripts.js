document.addEventListener('DOMContentLoaded', () => {
    // Add a click event listener to the "Send" button
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    
    sendButton.addEventListener('click', () => {
        const userQuestion = userInput.value;

        if (!userQuestion) {
            return; // Do nothing if the input is empty
        }

        // Display the user's message in the chatbox
        addUserMessage(userQuestion);

        // Clear the user input field
        userInput.value = '';

        // Make a request to the Cloud Run API with userQuestion
        fetch('/stylemeqna', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userQuestion }),
        })
        .then(response => response.json())
        .then(data => {
            const answer = data.answer;

            // Display the bot's response in the chatbox
            addBotMessage(answer);
        })
        .catch(error => {
            console.error('Error fetching answer:', error);
        });
    });
    
});

// Function to add a user message to the chatbox
function addUserMessage(message) {
    const chatbox = document.getElementById('chat-box');
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user-message');
    userMessageElement.textContent = message;
    chatbox.appendChild(userMessageElement);
}

// Function to add a bot message to the chatbox
function addBotMessage(message) {
    const chatbox = document.getElementById('chat-box');
    const botMessageElement = document.createElement('div');
    botMessageElement.classList.add('message', 'bot-message');
    botMessageElement.textContent = message;
    chatbox.appendChild(botMessageElement);
}

function flipCard(element) {
    element.closest('.flip-card').classList.toggle('flipped');
}

// Get the height of both containers
const chatContainer = document.querySelector('.chat-container');
const productContainer = document.querySelector('.product-container');
const maxHeight = Math.max(chatContainer.clientHeight, productContainer.clientHeight);

// Set both containers to have the same height
chatContainer.style.height = `${maxHeight}px`;
productContainer.style.height = `${maxHeight}px`;




const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    // Listen for the "Enter" keypress event in the user input field
    userInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            // Prevent the default "Enter" key behavior (e.g., line break)
            event.preventDefault();

            // Simulate a click on the send button
            sendButton.click();
        }
    });



    /*document.addEventListener('DOMContentLoaded', () => {
        const chatHistory = []; // Create an array to store the conversation history
    
        // ... (other code)
    
        // Add a click event listener to the "Submit Chat" button
        const submitButton = document.getElementById('submit-button');
    
        submitButton.addEventListener('click', () => {
            // Get the user's input
            const userInput = document.getElementById('user-input').value;
    
            if (!userInput) {
                return; // Do nothing if the input is empty
            }
    
            // Add the user's message to the conversation history
            chatHistory.push({ role: 'user', message: userInput });
    
            // Clear the user input field
            document.getElementById('user-input').value = '';
    
            // Make a request to the server with the entire conversation
            fetch('/submit_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ conversation: chatHistory }), // Send the entire conversation
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response as needed
            })
            .catch(error => {
                console.error('Error submitting chat:', error);
            });
        });
    
        // ... (other code)
    });
    */