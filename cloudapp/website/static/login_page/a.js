/*const form = document.querySelector('form');
const usernameInput = document.querySelector('#username');
const passwordInput = document.querySelector('#password');

form.addEventListener('submit', (e) => {
	e.preventDefault();

	const username = usernameInput.value;
	const password = passwordInput.value;

	if (username === 'admin' && password === 'password') {
		window.location.href = 'dashboard.html';
	} else {
		alert('Invalid username or password. Please try again.');
	}
});

const form = document.querySelector('form');
const emailInput = document.querySelector('#email');
const passwordInput = document.querySelector('#password');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const email = emailInput.value;
    const password = passwordInput.value;

    const data = {
        email: email,
        password: password
    };

    fetch('https://us-central1-pokerestimation-380716.cloudfunctions.net/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        if (response.ok) {
            // Success: handle login successful
            return response.json();
        } else {
            // Error: handle login failed
            throw new Error('Login failed');
        }
    })
    .then(function(data) {
        console.log(data);
        // Update UI or perform further actions on successful login
    })
    .catch(function(error) {
        console.error(error);
        // Update UI or perform error handling for failed login
    });
});*/

