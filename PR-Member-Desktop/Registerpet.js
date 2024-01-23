document.addEventListener('DOMContentLoaded', function() {
    const signUpForm = document.querySelector('.btn'); 

    signUpForm.addEventListener('click', function(event) {
        event.preventDefault();

        const Pet_ID = document.getElementById('Pet_ID').value;
        const Pet_Name = document.getElementById('Pet_Name').value;
        const Pet_Type = document.getElementById('Pet_Type').value;
        const Pet_Breed = document.getElementById('Pet_Breed').value;
        const Pet_Color = document.getElementById('Pet_Color').value;
        const Pet_Age = document.getElementById('Pet_Age').value;
        const Pet_Gender = document.getElementById('Pet_Gender').value;
        
        const confirmPassword = document.getElementById('confirm_pass').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        const data = {
            Pet_ID: Pet_ID,
            Pet_Name:Pet_Name,
            Pet_Type:Pet_Type,
            Pet_Breed:Pet_Breed,
            Pet_Color:Pet_Color,
            Pet_Age:Pet_Age
            Pet_Gender:Pet_Gender
        };

        fetch('http://127.0.0.1:5000/pr-platform/register-pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === " registered successfully") {
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
