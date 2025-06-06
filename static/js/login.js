document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const message = document.getElementById('loginMessage');

    //Add listener to login submit button
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        //Send username and password to server
        try {
            const response = await fetch('login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                console.log(data.message);
                window.location.href = data.redirect; // Redirect to home if login succesfull
            } else {
                console.error(data.message);
                message.textContent = data.message; //Show message if not succesfull
                message.style.display = 'block';
            }
        } catch (error) {
            console.error('Error during login:', error);
            message.textContent = 'An error occurred. Please try again.'; //Show message if error
            message.style.display = 'block';
        }
    });

    // Add listener to signup form submit button
    signupForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const forename = document.getElementById('signupForename').value;
        const surname = document.getElementById('signupSurname').value;
        const username = document.getElementById('signupUsername').value;
        const password = document.getElementById('signupPassword').value;

        // Validate password length and alphanumeric
        const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/;
        if (!passwordRegex.test(password)) {
            signupMessage.textContent =
                'Password must be at least 8 characters long and contain both letters and numbers.';
            signupMessage.style.display = 'block';
            return;
        }

        try {
            const response = await fetch('/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ forename, surname, username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                console.log(data.message);
                window.location.href = data.redirect; // Redirect to home if signup successful
            } else {
                console.error(data.message);
                signupMessage.textContent = data.message; // Show message if not successful
                signupMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Error during signup:', error);
            signupMessage.textContent = 'An error occurred. Please try again.'; // Show error message
            signupMessage.style.display = 'block';
        }
    });


});
