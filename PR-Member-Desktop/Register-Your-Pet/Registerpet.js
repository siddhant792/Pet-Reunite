const user = JSON.parse(localStorage.getItem("user"));

var breedSelector = document.getElementById("breed");
axios.get('http://127.0.0.1:5000/pr-platform/get-register-pet-details')
    .then(async response => {
        let arr = response.data.data.dog_breeds;
        arr.forEach(function (breed) {
            var option = document.createElement("option");
            option.text = breed;
            breedSelector.add(option);
        });
        // breedSelector.add("None of the above/Don't know");
        document.getElementById("pet_id").value = response.data.data.pet_unique_id;
    })
    .catch(error => {
        alert(error.response.data.message)
    });

document.getElementById("register-pet-button").onclick = () => {
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
    const Pet_ID = document.getElementById('pet_id').value;
    const Pet_Name = document.getElementById('name').value;
    const Pet_Type = document.getElementById('type').value;
    const Pet_Breed = document.getElementById('breed').value;
    const Pet_Color = document.getElementById('color').value;
    const Pet_Age = document.getElementById('age').value;
    const Pet_Gender = document.getElementById('gender').value;
    const Pet_Description = document.getElementById('description').value;

    let data = {
        "id": Pet_ID,
        "name": Pet_Name,
        "color": Pet_Color,
        "age": parseInt(Pet_Age),
        "gender": Pet_Gender,
        "description": Pet_Description,
        "image": base64String,
        "breed": Pet_Breed,
        "user_id": user._id
    }

    axios.post('http://127.0.0.1:5000/pr-platform/register-pet', data)
            .then(response => {
                alert("Your pet has been registered successfully")
            })
            .catch(error => {
                alert(error.response.data.message)
            });
}

