document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatbox = document.getElementById('chat-box');
    const productContainer = document.querySelector('.product-container');

    // Initialize the conversation list
    const conversationList = [];

    sendButton.addEventListener('click', () => {
        const userQuestion = userInput.value;

        if (!userQuestion) {
            return; // Do nothing if the input is empty
        }

        // Display the user's message in the chatbox
        addUserMessage(userQuestion);

        // Clear the user input field
        userInput.value = '';

        // Make a request to the Cloud Run API with userQuestion for chatbot response
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

            // Add the conversation to the list
            conversationList.push({ 'User': userQuestion, 'Fashion Advisor': answer });

            // Now, make a request to fetch products based on the conversation
            fetch('/styleme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ conversation: conversationList }),
            })
            .then(response => response.json())
            .then(data => {
                // Assuming that 'data.products' contains the list of products
                const products = data.products.slice(0, 3);

                // Clear existing products in the productContainer
                productContainer.innerHTML = '';

                // Add the new products to the productContainer
                products.forEach(product => {
                    const productDiv = document.createElement('div');
                    productDiv.className = 'product';
                    productDiv.innerHTML = `
                        <a href="${product.product_url}">
                            <img src="${product.image_URL}" alt="${product.product_name}">
                            <h2>${product.product_name}</h2>
                            <p>$${product.price}</p>
                        </a>`;
                    productContainer.appendChild(productDiv);
                });
            })
            .catch(error => {
                console.error('Error fetching and displaying products:', error);
            });
        })
        .catch(error => {
            console.error('Error fetching answer:', error);
        });
    });

    // ... (rest of your code)

    // Define addUserMessage and addBotMessage functions if not already defined
});

// Rest of your code...





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
