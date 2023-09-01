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