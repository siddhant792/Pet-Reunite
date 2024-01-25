document.addEventListener('DOMContentLoaded', function() {
    const signUpButton = document.querySelector('.div-44');

    if (signUpButton) {
        signUpButton.addEventListener('click', function(event) {
            event.preventDefault();

            const Pet_ID = document.getElementById('pet_id').value;
            const Pet_Name = document.getElementById('name').value;
            const Pet_Type = document.getElementById('type').value;
            let Pet_Breed = document.getElementById('breed').value;
            const Pet_Color = document.getElementById('color').value;
            const Pet_Age = document.getElementById('age').value;
            const Pet_Gender = document.getElementById('gender').value;
            const Pet_Description = document.getElementById('description').value;
    
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
                Pet_Gender: Pet_Gender,
                Pet_Description: Pet_Description
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

function showCustomBreed(select) {
    var customBreedInput = document.getElementById('custom_breed');
    if (select.value === 'other') {
        customBreedInput.style.display = 'block';
    } else {
        customBreedInput.style.display = 'none';
    }
}
