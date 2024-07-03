document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-olvido');
    const mensaje = document.getElementById('mensaje');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const email = form.email.value;

        // Aquí puedes agregar la lógica para enviar un correo de restablecimiento de contraseña
        if (validarEmail(email)) {
            mensaje.textContent = '';
            // Mostrar el modal
            var modal = new bootstrap.Modal(document.getElementById('restablecerModal'));
            modal.show();
        } else {
            mensaje.textContent = 'Por favor, introduce un correo electrónico válido';
        }
    });

    // Función para validar el correo electrónico
    function validarEmail(email) {
        const patronEmail = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return patronEmail.test(email);
    }

 // Redireccionar al index.html al cerrar el modal
 $('#restablecerModal').on('hidden.bs.modal', function () {
    window.location.href = 'login.html';
});
});
