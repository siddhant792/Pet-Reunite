const user = localStorage.getItem("user")
if(!user) {
    // navigate
    window.location.href = "http://127.0.0.1:5500/Login/login.html"
}