// Signup Page JavaScript
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirm-password");
const signupButton = document.getElementById("login-btn");

// Function to enable/disable signup button
function validateForm() {
    const name = nameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (name && email && password && confirmPassword && password === confirmPassword) {
        signupButton.removeAttribute("disabled");
    } else {
        signupButton.setAttribute("disabled", "disabled");
    }
}

// Event listeners for form validation
nameInput.addEventListener("input", validateForm);
emailInput.addEventListener("input", validateForm);
passwordInput.addEventListener("input", validateForm);
confirmPasswordInput.addEventListener("input", validateForm);
