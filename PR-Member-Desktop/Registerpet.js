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
            const uploadImage = document.getElementById('upload_image').files[0];

            const formData = new FormData();
            formData.append('Pet_ID', Pet_ID);
            formData.append('Pet_Name', Pet_Name);
            formData.append('Pet_Type', Pet_Type);
            formData.append('Pet_Color', Pet_Color);
            formData.append('Pet_Age', Pet_Age);
            formData.append('Pet_Gender', Pet_Gender);
            formData.append('Pet_Description', Pet_Description);

            // Check if an image was uploaded and append it to the FormData
            if (uploadImage && Pet_Breed === 'other') {
                formData.append('Pet_Image', uploadImage);
            }

            // If breed is not 'other', send Pet_Breed as part of the form data
            if (Pet_Breed !== 'other') {
                formData.append('Pet_Breed', Pet_Breed);
            }

            fetch('http://127.0.0.1:5000/pr-platform/register-pet', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const messageElement = document.getElementById('registrationMessage');
                if (data.message === "registered successfully") {
                    console.log('Registration Successful:', data);
                    messageElement.innerHTML = "Pet registered successfully.";
                    messageElement.style.display = 'block';
                    messageElement.style.color = 'green';
                    if (data.breedIdentified) {
                        document.getElementById('breed').value = data.breedIdentified;
                    }
                } else {
                    console.error('Registration Failed:', data);
                    messageElement.innerHTML = "Registration failed. Please try again.";
                    messageElement.style.display = 'block';
                    messageElement.style.color = 'red';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                const messageElement = document.getElementById('registrationMessage');
                messageElement.innerHTML = "An error occurred. Please try again.";
                messageElement.style.display = 'block';
                messageElement.style.color = 'red';
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

