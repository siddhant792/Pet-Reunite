const user = localStorage.getItem("user")
if(user) {
    // navigate
    window.location.href = "http://127.0.0.1:5500/Home"
}

document.addEventListener('DOMContentLoaded', function() {
    const signUpForm = document.querySelector('.btn'); 

    signUpForm.addEventListener('click', function(event) {
        event.preventDefault();

        const firstName = document.getElementById('first_name').value;
        const lastName = document.getElementById('last_name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const address = document.getElementById('address').value;
        const confirmPassword = document.getElementById('confirm_pass').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        const data = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            address: address
        };

        axios.post('http://127.0.0.1:5000/pr-platform/register', data)
            .then(response => {
                alert("Registration Successful, please login")
            })
            .catch(error => {
                alert(error.response.data.message)
            });
    });
});
