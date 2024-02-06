var breedSelector = document.getElementById("breed");
axios.get('http://127.0.0.1:5000/pr-platform/get-register-pet-details')
    .then(async response => {
        let arr = response.data.data.dog_breeds;
        arr.forEach(function (breed) {
            var option = document.createElement("option");
            option.text = breed;
            breedSelector.add(option);
        });
    })
    .catch(error => {
        alert(error.response.data.message)
    });

var address = "";
var latitude = "";
var longitude = "";

const lostPetsButton = document.getElementById('lostPetsButton');
const foundPetsButton = document.getElementById('foundPetsButton');
const lostPetsContent = document.getElementById('lostPetsContent');
const foundPetsContent = document.getElementById('foundPetsContent');


lostPetsButton.addEventListener('click', function () {
    lostPetsContent.style.display = 'block';
    foundPetsContent.style.display = 'none';
    lostPetsButton.style.backgroundColor = '#dec4ff';
    foundPetsButton.style.backgroundColor = '#f0eeee';
});

foundPetsButton.addEventListener('click', function () {
    lostPetsContent.style.display = 'none';
    foundPetsContent.style.display = 'block';
    lostPetsButton.style.backgroundColor = '#f0eeee';
    foundPetsButton.style.backgroundColor = '#dec4ff';
});


function initAutocomplete() {
    var input = document.getElementById('user_address');
    var autocomplete = new google.maps.places.Autocomplete(input);

    autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();

        address = place.formatted_address;
        latitude = place.geometry.location.lat();
        longitude = place.geometry.location.lng();

    });
}

initAutocomplete();

const cardContainer = document.getElementById("cardContainer");

function capitalizeFirstLetter(str) {
    return str.replace(/\b\w/g, function (match) {
        return match.toUpperCase();
    });
}

function startChat(user_id, user_name) {
    window.open("http://127.0.0.1:5500/Chat/chat.html?user_id=" + user_id + "&user_name=" + user_name, "_blank")
}

document.getElementById("search-pets").onclick = () => {
    const breed = document.getElementById('breed').value;
    const color = document.getElementById('color').value;
    const gender = document.getElementById('gender').value;
    const radius = document.getElementById('radius').value;

    const data = {
        breed: breed.toLowerCase().replace(" ", "_"),
        color: color.toLowerCase(),
        gender: gender.toLowerCase(),
        search_radius: parseInt(radius),
        search_address: address,
        search_latitude: latitude.toString(),
        search_longitude: longitude.toString()
    }

    let url = searchType == "lost" ? "search-lost-pets" : "search-found-pets"
    console.log(data);
    axios.post(`http://127.0.0.1:5000/pr-platform/${url}`, data)
        .then(async response => {
            let arr = response.data.data;
            cardContainer.innerHTML = "";
            arr.forEach(function (petData) {
                const card = document.createElement("div");
                card.className = "card";

                card.innerHTML = `
                    <img class="pet-image" src="${petData.image}" alt="Pet Image">
                    <div class="pet-details">
                        <div class="pet-info">
                            ${petData.name ? `<strong>Pet Name:</strong> ${capitalizeFirstLetter(petData.name)}<br>` : ''}
                            ${petData.age ? `<strong>Pet Age:</strong> ${petData.age} Years<br>`: ''}
                            <strong>Pet Breed:</strong> ${capitalizeFirstLetter(petData.breed)}<br>
                            <strong>Pet Color:</strong> ${capitalizeFirstLetter(petData.color)}
                        </div>
                        <div class="pet-description">
                            <strong>Pet Description:</strong><br>
                            ${petData.description}
                        </div>
                        <div class="last-seen">
                            <strong>Last Seen Location:</strong> ${petData.last_seen.address}<br>
                            ${petData.lostReportingTimeStamp ? `<strong>Reporting Time:</strong> ${petData.lostReportingTimeStamp}` : ''}
                        </div>
                    </div>
                    <button class="start-chat-button" onclick="startChat('${petData.user_id}', '${petData.user_name}')">Start Chat</button>
                `;
                cardContainer.appendChild(card);
            });
        })
        .catch(error => {
            console.log(error);
            alert(error.response.data.message)
        });
}

var searchType = "lost";

document.getElementById("foundPetsButton").onclick = () => {
    searchType = "found"
}

document.getElementById("lostPetsButton").onclick = () => {
    searchType = "lost"
}


