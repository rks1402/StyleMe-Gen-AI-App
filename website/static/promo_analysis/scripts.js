// Get a reference to the "Shop Now" button
const shopNowButton = document.getElementById('shopNowButton');


// Add a click event listener to the button
shopNowButton.addEventListener('click', function() {
  // Toggle the display property between 'none' and 'flex'
  if (productDisplayContainer.style.display === 'none' || productDisplayContainer.style.display === '') {
    productDisplayContainer.style.display = 'flex';
  } else {
    productDisplayContainer.style.display = 'none';
  }
});