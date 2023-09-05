// Get a reference to the "Regenerate Promotional Text" button
const reloadButton = document.querySelector('.reload-button button');

// Get a reference to the "User Promotional Text" ul
const userPromotionalTextUl = document.getElementById('user-promotional-text');

// Set the maximum number of promotional texts to display
const maxPromotionalTexts = 10;

// Add an event listener to the "Regenerate Promotional Text" button
reloadButton.addEventListener('click', function() {
  // Get the promotional text from the "Promotional Text" div
  const promotionalText = document.querySelector('.template h6').nextSibling.textContent.trim();

  // Store the promotional text in an array in localStorage
  const storedPromotionalTexts = JSON.parse(localStorage.getItem('promotionalTexts')) || [];

  // Add the new promotional text to the beginning of the array
  storedPromotionalTexts.unshift(promotionalText);

  // Limit the stored texts to the maximum allowed
  if (storedPromotionalTexts.length > maxPromotionalTexts) {
    storedPromotionalTexts.pop(); // Remove the oldest text
  }

  localStorage.setItem('promotionalTexts', JSON.stringify(storedPromotionalTexts));

  // Clear the user promotional text ul
  userPromotionalTextUl.innerHTML = '';

  // Create a new list item for each promotional text and append it to the "User Promotional Text" ul
  for (const text of storedPromotionalTexts) {
    const listItem = document.createElement('li');
    listItem.textContent = text;
    userPromotionalTextUl.appendChild(listItem);
  }

  // Scroll to the bottom of the "User Promotional Text" ul to show the latest text
  userPromotionalTextUl.scrollTop = userPromotionalTextUl.scrollHeight;
});

// Retrieve and display stored promotional texts from localStorage
const storedPromotionalTexts = JSON.parse(localStorage.getItem('promotionalTexts')) || [];
for (const text of storedPromotionalTexts) {
  const listItem = document.createElement('li');
  listItem.textContent = text;

  userPromotionalTextUl.appendChild(listItem);
}


// Get a reference to the "Shop Now" button
const shopNowButton = document.getElementById('shopNowButton');

// Get a reference to the "productDisplayContainer"
const productDisplayContainer = document.getElementById('productDisplayContainer');

// Add a click event listener to the button
shopNowButton.addEventListener('click', function() {
  // Toggle the display property between 'none' and 'flex'
  if (productDisplayContainer.style.display === 'none' || productDisplayContainer.style.display === '') {
    productDisplayContainer.style.display = 'flex';
  } else {
    productDisplayContainer.style.display = 'none';
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

// JavaScript to toggle the flip card
document.addEventListener('DOMContentLoaded', function () {
    const flipCards = document.querySelectorAll('.flip-card');
    
    flipCards.forEach(card => {
        card.addEventListener('click', function () {
            card.querySelector('.flip-card-inner').classList.toggle('flipped');
        });
    });
    });    

    