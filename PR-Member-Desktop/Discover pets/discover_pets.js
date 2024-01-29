document.addEventListener("DOMContentLoaded", function() {
    const lostPetsButton = document.getElementById('lostPetsButton');
    const foundPetsButton = document.getElementById('foundPetsButton');
    const lostPetsContent = document.getElementById('lostPetsContent');
    const foundPetsContent = document.getElementById('foundPetsContent');
    const petForm = document.querySelector('.purple-block .pet-form');

    function resetForm() {
        petForm.reset();
    }

    lostPetsButton.addEventListener('click', function() {
        lostPetsContent.style.display = 'block';
        foundPetsContent.style.display = 'none';
        lostPetsButton.style.backgroundColor = '#dec4ff';
        foundPetsButton.style.backgroundColor = '#f0eeee';
        resetForm();
    });

    foundPetsButton.addEventListener('click', function() {
        lostPetsContent.style.display = 'none';
        foundPetsContent.style.display = 'block';
        lostPetsButton.style.backgroundColor = '#f0eeee';
        foundPetsButton.style.backgroundColor = '#dec4ff';
        resetForm();
    });

    petForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const petType = document.getElementById('petType').value;
        const petColor = document.getElementById('petColor').value;
        const petGender = document.getElementById('petGender').value;
        const petBreed = document.getElementById('petBreed').value;
        const lastSeen = document.getElementById('lastSeen').value;
        const radius = document.getElementById('radius').value;

        const url = `http://127.0.0.1:5000/pr-platform/search-lost-pets?color=${encodeURIComponent(petColor)}&breed=${encodeURIComponent(petBreed)}&gender=${encodeURIComponent(petGender)}&search_address=${encodeURIComponent(lastSeen)}&search_radius=${encodeURIComponent(radius)}`;

        // Fetch data from the server
        fetch(url)
            .then(response => response.json())
            // ... existing JavaScript code ...

            .then(data => {
                // reference to the results containers
                const resultsContainer1 = document.getElementById('searchResultsContainer1');
                const resultsContainer2 = document.getElementById('searchResultsContainer2');

                // populate search results
                function populateResults(container, data) {
                    container.innerHTML = ''; 

                    if (data && data.length > 0) {
                        data.forEach(pet => {
                            const petDiv = document.createElement('div');
                            petDiv.className = 'pet-item';

                            petDiv.innerHTML = `
                                <img src="${pet.image}" alt="Pet Image" class="pet-image">
                                <p><strong>Name:</strong> ${pet.name}</p>
                                <p><strong>Breed:</strong> ${pet.breed}</p>
                                <p><strong>Color:</strong> ${pet.color}</p>
                                <p><strong>Age:</strong> ${pet.age}</p>
                                <p><strong>Last Seen:</strong> ${pet.last_seen.address}</p>
                            `;

                            container.appendChild(petDiv);
                        });
                    } else {
                        container.innerHTML = '<p>No pets found based on your search criteria.</p>';
                    }
                }

                // Populate both containers with search results
                populateResults(resultsContainer1, data.data);
                populateResults(resultsContainer2, data.data);
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
            });

             
    });
});
