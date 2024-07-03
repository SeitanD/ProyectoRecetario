document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-registro'); // Obtener el formulario de registro
    const mensaje = document.getElementById('mensaje'); // Obtener el elemento de mensaje de error
    const registroExitosoModal = document.getElementById('registroExitosoModal'); // Obtener el modal de registro exitoso

    form.addEventListener('submit', (e) => { // Agregar un evento de escucha para el envío del formulario
        e.preventDefault(); // Prevenir el envío predeterminado del formulario

        // Obtener los valores de los campos del formulario
        const nombre = form.nombre.value;
        const telefono = form.telefono.value;
        const email = form.email.value;
        const confirmarEmail = form.confirmarEmail.value;
        const password = form.password.value;
        const confirmarPassword = form.confirmarPassword.value;

        // Expresiones regulares para validar el nombre y el número de teléfono
        const patronNombre = /^[a-zA-Z\s]+$/;
        const patronTelefono = /^\d{09}$/; // Asume un número de teléfono de 09 dígitos

        // Validar el nombre con la expresión regular
        if (!patronNombre.test(nombre)) {
            mensaje.textContent = 'El nombre solo puede contener letras';
            return;
        }

        // Validar el número de teléfono con la expresión regular
        if (!patronTelefono.test(telefono)) {
            mensaje.textContent = 'Ingrese un número de teléfono válido (09 dígitos)';
            return;
        }

        // Validar si el correo electrónico está vacío
        if (email.trim() === '') {
            mensaje.textContent = 'Por favor, ingrese su correo electrónico';
            return;
        }

        // Validar si los correos electrónicos coinciden
        if (email !== confirmarEmail) {
            mensaje.textContent = 'Los correos electrónicos no coinciden';
            return;
        }

        // Validar si la contraseña está vacía
        if (password.trim() === '') {
            mensaje.textContent = 'Por favor, ingrese su contraseña';
            return;
        }

        // Validar si las contraseñas coinciden
        if (password !== confirmarPassword) {
            mensaje.textContent = 'Las contraseñas no coinciden';
            return;
        }

        // Si todas las validaciones son exitosas, mostrar el modal de registro exitoso
        mensaje.textContent = 'Registro exitoso';
        $('#registroExitosoModal').modal('show'); // Mostrar el modal de registro exitoso
        form.reset(); // Restablecer el formulario después del registro exitoso
    });

    // Agregar un evento de escucha para el evento de cierre del modal de registro exitoso
    registroExitosoModal.addEventListener('hidden.bs.modal', function () {
        // Redireccionar al usuario al índice (index.html)
        window.location.href = 'index.html';
    });
});