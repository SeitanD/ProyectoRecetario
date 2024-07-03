document.addEventListener('DOMContentLoaded', () => {
    // Obtiene el formulario de contacto
    const form = document.getElementById('form-contacto');
    // Obtiene el elemento para mostrar mensajes
    const respuesta = document.getElementById('respuesta');
    // Obtiene el modal y el botón para cerrarlo
    const modal = document.getElementById('modal-confirmacion');
    const cerrarModal = document.getElementById('cerrar-modal');

    // Expresiones regulares para validaciones
    const nombreRegex = /^[a-zA-Z\s]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const telefonoRegex = /^\d{9}$/;

    // Función de validación para el nombre (solo letras y espacios)
    function validarNombre(nombre) {
        return nombreRegex.test(nombre);
    }

    // Función de validación para el teléfono (exactamente 9 dígitos)
    function validarTelefono(telefono) {
        return telefonoRegex.test(telefono);
    }

    // Agrega un evento de escucha al formulario para prevenir su envío predeterminado
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Obtiene los valores de los campos del formulario
        const nombre = form.nombre.value;
        const email = form.email.value;
        const telefono = form.telefono.value;
        const asunto = form.asunto.value;
        const mensaje = form.mensaje.value;

        // Validaciones
        if (!validarNombre(nombre)) {
            respuesta.textContent = 'Por favor, ingresa un nombre válido (solo letras y espacios)';
        } else if (!emailRegex.test(email)) {
            respuesta.textContent = 'Por favor, ingresa un correo electrónico válido';
        } else if (!validarTelefono(telefono)) {
            respuesta.textContent = 'Por favor, ingresa un número de teléfono válido (exactamente 9 dígitos)';
        } else if (asunto.trim() === '') {
            respuesta.textContent = 'Por favor, ingresa el asunto';
        } else if (mensaje.trim() === '') {
            respuesta.textContent = 'Por favor, ingresa tu mensaje';
        } else {
            // Muestra el modal de confirmación
            modal.style.display = 'block';
            respuesta.textContent = ''; // Limpia cualquier mensaje previo

            // Limpia los campos del formulario después de enviar el mensaje
            form.reset();
        }
    });

    // Agrega un evento de escucha al botón del modal para cerrarlo
    cerrarModal.addEventListener('click', () => {
        modal.style.display = 'none';
        window.location.href = 'index.html';
    });
});
