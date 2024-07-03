document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-login');
    const mensaje = document.getElementById('mensaje');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const usuario = form.usuario.value;
        const password = form.password.value;

        // Aquí puedes agregar la lógica de validación del usuario y contraseña
        // Por ejemplo:
        if(usuario === 'admin' && password === 'admin') {
            mensaje.textContent = 'Inicio de sesión exitoso';
            // Aquí puedes redirigir al usuario a otra página
        } else {
            mensaje.textContent = 'Usuario o contraseña incorrectos';
        }
    });
});
