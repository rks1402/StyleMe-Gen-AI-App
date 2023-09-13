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

// JavaScript to toggle the flip card
document.addEventListener('DOMContentLoaded', function () {
  const flipCards = document.querySelectorAll('.flip-card');
  
  flipCards.forEach(card => {
      card.addEventListener('click', function () {
          card.classList.toggle('flipped'); // Toggle the 'flipped' class on click
      });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const flipCards = document.querySelectorAll('.flip-card');

  flipCards.forEach(card => {
      const summaryText = card.querySelector('#summaryText');
      const editButton = card.querySelector('#editButton');

      // Function to toggle between displaying text and an input field
      function toggleEditable() {
          const isEditing = summaryText.contentEditable === 'true';
          summaryText.contentEditable = !isEditing;
          summaryText.style.border = isEditing ? 'none' : '1px solid #ccc';

          if (isEditing) {
              editButton.textContent = 'Edit';
          } else {
              editButton.textContent = 'Save';
          }
      }

      // Prevent card flipping when clicking the "Edit" button
      editButton.addEventListener('click', function (e) {
          e.stopPropagation(); // Prevent the click event from reaching the card
          toggleEditable();
      });

      // Prevent card flipping when clicking the text area
      summaryText.addEventListener('click', function (e) {
          e.stopPropagation(); // Prevent the click event from reaching the card
      });
  });
});


    