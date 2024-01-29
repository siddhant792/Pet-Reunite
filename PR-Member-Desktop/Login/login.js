document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.querySelector('.span-5'); 

    loginButton.addEventListener('click', function(event) {
        event.preventDefault();


        const email = document.getElementById('email').value; 
        const password = document.getElementById('password').value; 

        const data = {
            email: email,
            password: password
        };

        fetch('http://127.0.0.1:3000/pr-platform/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Login successful") {
                console.log('Login Successful:', data);
                
            } else {
                console.error('Login Failed:', data);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
