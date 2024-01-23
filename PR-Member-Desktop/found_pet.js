document.addEventListener('DOMContentLoaded', function() {
    const signUpForm = document.querySelector('.btn'); 

    signUpForm.addEventListener('click', function(event) {
        event.preventDefault();

        const petType = document.getElementById('pet_type').value;
        const description = document.getElementById('description').value;
        const petBreed = document.getElementById('pet_breed').value;
        const userAddress = document.getElementById('used_address').value;
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