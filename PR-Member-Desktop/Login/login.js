const user = localStorage.getItem("user")
if(user) {
    // navigate
    window.location.href = "http://127.0.0.1:5500/Home"
}

document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.querySelector('.span-5');

    loginButton.addEventListener('click', function (event) {
        event.preventDefault();


        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const data = {
            email: email,
            password: password
        };

        axios.post('http://127.0.0.1:5000/pr-platform/login', data)
            .then(response => {
                localStorage.setItem("user", JSON.stringify(response.data.data));
                window.location.href = "http://127.0.0.1:5500/Home"
            })
            .catch(error => {
                alert(error.response.data.message)
            });
    });
});
