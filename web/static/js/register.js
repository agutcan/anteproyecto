document.addEventListener('DOMContentLoaded', function () {
    const placeholders = {
        username: 'Ej: gamer123',
        email: 'Ej: correo@example.com',
        password1: 'Crea una contraseña segura',
        password2: 'Confirma tu contraseña',
    };

    Object.keys(placeholders).forEach(function (name) {
        const input = document.querySelector(`input[name="${name}"]`);
        if (input) {
            input.placeholder = placeholders[name];
        }
    });
});