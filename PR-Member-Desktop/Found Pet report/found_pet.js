document.addEventListener('DOMContentLoaded', function() {
    const petForm = document.getElementById('petForm');
    const shelterLink = document.getElementById('shelterLink');
    const modal = document.getElementById('myModal');
    const span = document.getElementsByClassName('close')[0];

    function fetchNearbyShelters() {
        const userLatitude = 'user_latitude';
        const userLongitude = 'user_longitude';

        const url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${userLatitude},${userLongitude}&radius=5000&type=animal_shelter&key=YOUR_GOOGLE_MAPS_API_KEY`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                populateModalWithShelters(data.results);
            })
            .catch(error => console.error('Error:', error));
    }

    function populateModalWithShelters(shelters) {
        const modalBody = document.querySelector('.modal-body');
        modalBody.innerHTML = '';

        shelters.forEach(shelter => {
            const shelterDiv = document.createElement('div');
            shelterDiv.className = 'div-30';
            shelterDiv.innerHTML = `
            <div class="div-30">
            <div class="div-31">Animal Shelters</div>
            <div class="div-32">Pick a shelter near you</div>
            <div class="div-33">
              <div class="div-34">
                <div class="div-35">${shelter.name}</div>
                <img
                  loading="lazy"
                  srcset="https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/22375695048c4830128a6ff496d5af30cb21cfad52d244791573865ba6394e9e?apiKey=6c234474d5484635a95c9b3a2387c63f&"
                  class="img-a1"
                />
              </div>
              <div class="div-36">
                <div class="div-37">
                ${shelter.address}
                  <br />
                </div>
                <div class="div-38">
                  <div class="div-39">
                  <img
                        loading="lazy"
                        srcset="https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/24fd3464581da9067f60b4d924d02485d5af8a355aad509987ba502f9d051bef?apiKey=6c234474d5484635a95c9b3a2387c63f&"
                        class="img-a2"
                  />
                
                    <div class="div-42">
                      
                      <span style="font-size: 13px">${shelter.phone}</span>
                    </div>
                  </div>
                  <div class="div-39">
                        <img
                        loading="lazy"
                        src="https://cdn.builder.io/api/v1/image/assets/TEMP/a89d298cf024d66ffdc2917a3a7ba6c937f077763ab7b0990b5febe07793d5f9?apiKey=6c234474d5484635a95c9b3a2387c63f&"
                        class="img-a4"
                        />
        
                    <div class="div-42">
                      
                      <span style="font-size: 13px">${shelter.openingHours}</span>
                    </div>
                   
                  </div>
                 
                  </div>
                  <button class="select-button" div class="div-45" data-address="${shelter.address}">Select</button>
                </div>
              </div>
            </div>
          </div>
            `;
            modalBody.appendChild(shelterDiv);

            shelterDiv.querySelector('.select-button').addEventListener('click', function() {
                document.getElementById('user_address').value = this.getAttribute('data-address');
                modal.style.display = 'none'; 
            });

        });
    };

    shelterLink.onclick = function(event) {
        event.preventDefault();
        modal.style.display = "block";
        fetchNearbyShelters(); 
    };

    span.onclick = function() {
        modal.style.display = "none";
    };
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    petForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const petType = document.getElementById('pet_type').value;
        const description = document.getElementById('description').value;
        const petBreed = document.getElementById('pet_breed').value;
        const userAddress = document.getElementById('user_address').value;
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
        .then(data => {
            console.log('Success:', data);
            // Handle success, update UI, close modal, etc.
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors here, such as displaying a message to the user
        });
    });
});
