document.addEventListener('DOMContentLoaded', function() {
    const signUpForm = document.querySelector('.btn');

    if (signUpForm) {
        signUpForm.addEventListener('click', function(event) {
            event.preventDefault();

            const Pet_ID = document.getElementById('Pet_ID').value;
            const Pet_Name = document.getElementById('Pet_Name').value;
            const Pet_Type = document.getElementById('Pet_Type').value;
            let Pet_Breed = document.getElementById('Pet_Breed').value;
            const Pet_Color = document.getElementById('Pet_Color').value;
            const Pet_Age = document.getElementById('Pet_Age').value;
            const Pet_Gender = document.getElementById('Pet_Gender').value;
            const confirmPassword = document.getElementById('confirm_pass').value;
            const password = document.getElementById('password').value; // Assuming there's a password input

            if (password !== confirmPassword) {
                alert('Passwords do not match');
                return;
            }

            // If breed is 'other', use the custom breed value
            if (Pet_Breed === 'other') {
                Pet_Breed = document.getElementById('custom_breed').value;
            }

            const data = {
                Pet_ID: Pet_ID,
                Pet_Name: Pet_Name,
                Pet_Type: Pet_Type,
                Pet_Breed: Pet_Breed,
                Pet_Color: Pet_Color,
                Pet_Age: Pet_Age,
                Pet_Gender: Pet_Gender
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
                if (data.message === "registered successfully") {
                    console.log('Registration Successful:', data);
                    // Redirect or update UI as needed
                } else {
                    console.error('Registration Failed:', data);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
});

function showCustomBreed(selectElement) {
    var customBreedContainer = document.getElementById('customBreedContainer');
    if (selectElement.value === 'other') {
        customBreedContainer.style.display = 'block';
    } else {
        customBreedContainer.style.display = 'none';
    }
}

