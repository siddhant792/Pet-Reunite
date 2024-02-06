document.getElementById("send-query").onclick = (e) => {
    e.preventDefault();

    const name = document.querySelector('#full_name').value;
    const email = document.querySelector('#Email').value;
    const message = document.querySelector('#message').value;

    // request payload
    const data = {
        name: name,
        email: email,
        message: message
    };

    axios.post('http://127.0.0.1:5000/pr-platform/contact-us', data)
        .then(response => {
            alert("Your query has been submitted successfully.")
        })
        .catch(error => {
            alert(error.response.data.message)
        });
}
