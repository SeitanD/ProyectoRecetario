let menuVisible = false;

// Función que oculta o muestra el menú
function mostrarOcultarMenu() {
    if (menuVisible) {
        document.getElementById("nav").classList = "";
        menuVisible = false;
    } else {
        document.getElementById("nav").classList = "responsive";
        menuVisible = true;
    }
}

// Función para seleccionar una opción del menú
function seleccionar() {
    // oculta el menú una vez que selecciona una opción
    document.getElementById("nav").classList = "";
    menuVisible = false;
}
