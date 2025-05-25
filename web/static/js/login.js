document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("id_username");
    const passwordInput = document.getElementById("id_password");

    if (usernameInput) {
        usernameInput.placeholder = "Ingresa tu usuario";
    }

    if (passwordInput) {
        passwordInput.placeholder = "Ingresa tu contraseña";
    }
});