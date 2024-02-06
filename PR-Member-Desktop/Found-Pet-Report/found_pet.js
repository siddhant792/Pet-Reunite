var breedSelector = document.getElementById("breed");
const user = JSON.parse(localStorage.getItem("user"));
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

var popupContainer = document.getElementById('popup-container');

axios.get('http://127.0.0.1:5000/pr-platform/get-animal-shelters')
  .then(async response => {
    let arr = response.data.data;
    // arr.forEach(function (breed) {
    //   var option = document.createElement("option");
    //   option.text = breed;
    //   breedSelector.add(option);
    // });

    var shelterCardsHTML = arr.map(shelter => `
        <div class="shelter-card">
          <div class="name-image-holder">
            <div class="shelter-header">${shelter.name}</div>
            <img src="${shelter.image}" alt="${shelter.name}" style="width: 100%;">
          </div>
          <div class="shelter-content">
            <div class="shelter-add"><p>${shelter.address}</p> </div>
            <div class="shelter-details">
              <p><strong>Any Pets</strong></p>
              <p><strong>Phone Number:</strong> ${shelter.phoneNumber}</p>
              <p><strong>Opening Time:</strong> ${shelter.opens}</p>
              <button class="select-button" onclick="selectShelter('${shelter._id}')">Select</button>
            </div>
          </div>
          
        </div>
      `).join('');

    // Insert the generated HTML into the popup container
    popupContainer.innerHTML += shelterCardsHTML;
  })
  .catch(error => {
    alert(error.response.data.message)
  });

var address = "";
var latitude = "";
var longitude = "";
var shelterId = "";

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

document.getElementById("report-pet-button").onclick = () => {
  const uploadImage = document.getElementById('upload_image').files[0];

  var reader = new FileReader();
  reader.onload = function () {
    // Resolve the promise with the Base64-encoded string
    var base64String = reader.result.split(',')[1];
    callAPI(base64String);
  };

  // Read the file as Data URL
  reader.readAsDataURL(uploadImage);
}

function callAPI(base64String) {
  const description = document.getElementById('description').value;
  const Pet_Breed = document.getElementById('breed').value;
  const Pet_Color = document.getElementById('color').value;
  const gender = document.getElementById('gender').value;
  const age = document.getElementById('age').value;

  const data = {
    description: description,
    color: Pet_Color,
    gender: gender,
    age: age,
    user_id: user._id,
    image: base64String
  };

  if (Pet_Breed != "") {
    data.breed = Pet_Breed
  }

  if (shelterId == "") {
    data.shelter_type = "home";
    data.address = address;
    data.latitude = latitude.toString();
    data.longitude = longitude.toString();
  } else {
    data.shelter_type = "animal_shelter";
    data.animal_shelter_id = shelterId
  }

  console.log(data);

  axios.post('http://127.0.0.1:5000/pr-platform/report-found-pet', data)
    .then(response => {
      alert("Pet has been reported successfully")
    })
    .catch(error => {
      alert(error.response.data.message)
    });
}


document.getElementById("shelterLink").onclick = () => {
  popupContainer.style.display = 'block';
}

function selectShelter(itemId) {
  shelterId = itemId;
  popupContainer.style.display = 'none';
}

function closePopup() {
  popupContainer.style.display = 'none';
}