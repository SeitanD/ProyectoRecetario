document.addEventListener('DOMContentLoaded', function() {
    const productos = document.querySelectorAll('[id^="cantidad-"]');
    
    productos.forEach(function(producto) {
        producto.addEventListener('input', function() {
            const productoId = this.id.split('-')[1];
            actualizarPrecioTotal(productoId);
        });
    });
});

function actualizarPrecioTotal(productoId) {
    const cantidadInput = document.getElementById(`cantidad-${productoId}`);
    const precioUnitarioText = document.getElementById(`precio-unitario-${productoId}`).innerText;
    const precioUnitario = parseInt(precioUnitarioText.replace('$', '').replace(/\s+/g, '')); // Elimina el símbolo de dólar y los espacios
    const cantidad = parseInt(cantidadInput.value);
    const precioTotal = cantidad * precioUnitario;
    document.getElementById(`precio-total-${productoId}`).innerText = `${precioTotal.toLocaleString('es-CL')}`;
}
