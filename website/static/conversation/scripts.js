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
        fetch('/qna', {
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


    // Get the summary button and the summary section
const summaryButton = document.getElementById("summary-button");
const summarySection = document.getElementById("summary");

// Add a click event listener to the button
summaryButton.addEventListener("click", function () {
    // Toggle the visibility of the summary section
    if (summarySection.style.display === "none" || summarySection.style.display === "") {
        summarySection.style.display = "block";
        summaryButton.textContent = "Hide Summary"; // Change button text
    } else {
        summarySection.style.display = "none";
        summaryButton.textContent = "Show Summary"; // Change button text
    }
});
