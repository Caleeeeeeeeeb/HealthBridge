function validateRegisterForm() {
    const firstname = document.forms["registerForm"]["firstname"].value.trim();
    const lastname = document.forms["registerForm"]["lastname"].value.trim();
    const email = document.forms["registerForm"]["email"].value.trim();
    const password = document.forms["registerForm"]["password"].value;
    const confirmPassword = document.forms["registerForm"]["confirm_password"].value;
    const errorDiv = document.getElementById("error");

    errorDiv.innerHTML = "";

    if (firstname.length < 2) {
        errorDiv.innerHTML = "First name must be at least 2 characters long.";
        return false;
    }

    if (lastname.length < 2) {
        errorDiv.innerHTML = "Last name must be at least 2 characters long.";
        return false;
    }

    // Simple email validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        errorDiv.innerHTML = "Please enter a valid email address.";
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