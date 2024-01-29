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
        let radius = document.getElementById('radius').value;

        if (!Number.isInteger(Number(radius))) {
            alert("Please enter a valid integer for radius.");
            return;
        }

        const simulatedApiResponse = [
            {
                name: "Sam",
                age: "14 years old",
                breed: "Toy poodle",
                color: "White",
                gender: "Male",
                image: "path_to_pet_image.jpg",
                created: "40 minutes ago",
                status: "Found"
            }
        ];

        const resultsContainer1 = document.getElementById('searchResultsContainer1');
        const resultsContainer2 = document.getElementById('searchResultsContainer2');

        function populateResults(container, data) {
            container.innerHTML = '';

            if (data && data.length > 0) {
                data.forEach(pet => {
                    const petDiv = document.createElement('div');
                    petDiv.className = 'div-30';

                    petDiv.innerHTML = `
                        <div class="div-31">
                          <div class="column-a1">
                            <div class="div-32">
                              Name: <span style="font-weight: 400">${pet.name}</span><br />
                              Age: <span style="font-weight: 400">${pet.age}</span><br />
                              Breed: <span style="font-weight: 400">${pet.breed}</span><br />
                              Color: <span style="font-weight: 400">${pet.color}</span><br />
                              Gender: <span style="font-weight: 400">${pet.gender}</span>
                            </div>
                          </div>
                          <div class="column-a2">
                            <div class="div-33">
                              <img src="${pet.image}" class="img-a11" alt="Pet Image">
                              <div class="div-34">
                                <div class="div-36">${pet.created}</div>
                                <div class="div-37">
                                  <div class="div-38">Explore<br />Location</div>
                                  <div class="div-39">${pet.status}</div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                    `;

                    container.appendChild(petDiv);
                });
            } else {
                container.innerHTML = '<p>No pets found based on your search criteria.</p>';
            }
        }

        // Replace the following line with an actual API call
        populateResults(resultsContainer1, simulatedApiResponse);
        populateResults(resultsContainer2, simulatedApiResponse);
    });
});
