document.addEventListener('DOMContentLoaded', function() {
    const signUpForm = document.querySelector('.btn'); 

    signUpForm.addEventListener('click', function(event) {
        event.preventDefault();

        const firstName = document.getElementById('first_name').value;
        const lastName = document.getElementById('last_name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const address = document.getElementById('address').value;
        const confirmPassword = document.getElementById('confirm_pass').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        const data = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            address: address
        };

        fetch('http://127.0.0.1:3000/pr-platform/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "User registered successfully") {
                console.log('Registration Successful:', data);
                // Redirect to login page or update UI as needed
            } else {
                console.error('Registration Failed:', data);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
