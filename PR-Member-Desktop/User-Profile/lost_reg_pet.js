const user = JSON.parse(localStorage.getItem("user"));
// Get the modal
var modal = document.getElementById("lostPetModal");
var address = "";
var latitude = "";
var longitude = "";
var activePet = "";

document.getElementById("welcome-name").innerHTML = "Welcome, " + user.first_name;

function markLost(pet_id) {
    modal.style.display = "block";
    activePet = pet_id;
}

document.getElementById("close-model-span").onclick = () => {
    modal.style.display = "none";
}

var petContainer = document.getElementById('pet-container');

axios.get(`http://127.0.0.1:5000/pr-platform/get-user-pets/${user._id}`)
    .then(async response => {
        let arr = response.data.data;
        var petCard = arr.map(pet => `
        <div class="column-2">
            <span class="span-7">
            <div class="div-24">
                <div class="text-container">
                Name:
                <span style="font-weight: 400">${pet.name}</span>
                <br />
                Age:
                <span style="font-weight: 500">${pet.age}</span>
                <span style="font-weight: 400">years old</span>
                <br />
                Gender
                <span style="font-weight: 400">: ${pet.gender}</span>
                <br />
                Breed:
                <span style="font-weight: 400">${pet.breed}</span>
                <br />
                Color:
                <span style="font-weight: 400">${pet.color}</span>
                <br />
                Status:
                <span style="font-weight: 400">${pet.status}</span>
                <br />
                Pet ID:
                <span style="font-weight: 400">${pet.id}</span>
                </div>

                <img loading="lazy"
                src=${pet.image}
                class="pet-image-2" />

            </div>
            <div class="div-25">
                <div class="button-group">
                <div onclick="markLost('${pet.id}')" class="button lost-button">Lost</div>
                <div class="button found-button">Found</div>
                </div>
            </div>
            </span>
        </div>
      `).join('');

        petContainer.innerHTML += petCard;
    })
    .catch(error => {
        console.log(error)
    });

function initAutocomplete() {
    var input = document.getElementById('streetAddress');
    var autocomplete = new google.maps.places.Autocomplete(input);

    autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();

        address = place.formatted_address;
        latitude = place.geometry.location.lat();
        longitude = place.geometry.location.lng();

    });
}

initAutocomplete();

document.getElementById("update-lost-pet").onclick = () => {
    const data = {
        user_id: user._id,
        pet_id: activePet,
        address: address,
        latitude: latitude.toString(),
        longitude: longitude.toString()
    }
    axios.post("http://127.0.0.1:5000/pr-platform/update-registered-pet-lost-status", data)
        .then(async response => {
            alert("Your pet has been marked as lost successfully")
        })
        .catch(error => {
            console.log(error);
            alert(error)
        });
}
