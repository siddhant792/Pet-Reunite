document.addEventListener('DOMContentLoaded', function() {
    const petForm = document.getElementById('petForm');

    petForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const petType = document.getElementById('pet_type').value;
        const description = document.getElementById('description').value;
        const petBreed = document.getElementById('pet_breed').value;
        const userAddress = document.getElementById('user_address').value; // Corrected the typo here
        const petColor = document.getElementById('pet_color').value;
        const gender = document.getElementById('gender').value;

        const data = {
            pet_type: petType,
            description: description,
            pet_breed: petBreed,
            user_address: userAddress,
            pet_color: petColor,
            gender: gender
        };

        fetch('http://127.0.0.1:5000/pr-platform/report-found-pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => console.error('Error:', error));
    });
});
