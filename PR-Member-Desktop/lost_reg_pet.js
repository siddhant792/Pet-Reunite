// Get the modal
var modal = document.getElementById("lostPetModal");

// Get the buttons that open the modal
var btns = document.getElementsByClassName("lost-button");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// Function to open the modal
function openModal() {
    modal.style.display = "block";
}

// Add event listeners to all lost-buttons
for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', openModal);
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

//form submission
document.getElementById("lostPetForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const userId = "Jsdp3xfxfBl0EFVDSU54"; // Replace with dynamic user ID if needed
    const petId = "2"; // Replace with dynamic pet ID if needed
    const streetAddress = document.getElementById("streetAddress").value;
    const suburb = document.getElementById("suburb").value;
    const postcode = document.getElementById("postcode").value;
    const state = document.getElementById("state").value;
    const country = document.getElementById("country").value;

    //address components
    const fullAddress = `${streetAddress}, ${suburb}, ${postcode}, ${state}, ${country}`;

    // Replace with actual method to get latitude and longitude based on address
    const latitude = "7658725782"; // Dummy value
    const longitude = "6235782223"; // Dummy value

    const data = {
        user_id: userId,
        pet_id: petId,
        address: fullAddress,
        latitude: latitude,
        longitude: longitude
    };

    fetch('http://127.0.0.1:5000/pr-platform/update-last-seen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Last seen recorded successfully") {
            console.log('Update Successful:', data);
            modal.style.display = "none";
            // Update UI or redirect as needed
        } else {
            console.error('Update Failed:', data);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
