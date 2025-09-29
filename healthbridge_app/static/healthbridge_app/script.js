function validateRegisterForm() {
    const username = document.forms["registerForm"]["username"].value;
    const password = document.forms["registerForm"]["password1"].value;
    const confirmPassword = document.forms["registerForm"]["password2"].value;
    const errorDiv = document.getElementById("error");

    errorDiv.innerHTML = "";

    if (username.length < 3) {
        errorDiv.innerHTML = "Username must be at least 3 characters long.";
        return false;
    }

    if (password.length < 6) {
        errorDiv.innerHTML = "Password must be at least 6 characters long.";
        return false;
    }

    if (password !== confirmPassword) {
        errorDiv.innerHTML = "Passwords do not match.";
        return false;
    }

    return true;
}