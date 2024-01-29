document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('.column-2'); 
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const name = document.querySelector('#full_name').value;
        const email = document.querySelector('#Email').value;
        const message = document.querySelector('#message').value;

        // request payload
        const data = {
            name: name,
            email: email,
            message: message
        };

        // POST request
        fetch('http://127.0.0.1:5000/pr-platform/contact-us', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('We will get back to you'); 
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.'); 
        });
    });
});
