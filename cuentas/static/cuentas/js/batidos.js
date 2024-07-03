$(document).ready(function() {
    // Función para mostrar u ocultar el menú
    function mostrarOcultarMenu() {
        // Alterna la visibilidad del menú de navegación
        $('nav').toggle();
    }

    // Mostrar/ocultar el menú en dispositivos móviles
    $('#bar').click(function() {
        // Llama a la función mostrarOcultarMenu() cuando se hace clic en el elemento con ID 'bar'
        mostrarOcultarMenu();
    });

    // Función para ocultar el menú al seleccionar una opción
    function seleccionar() {
        // Oculta el menú de navegación con ID 'nav'
        $('#nav').hide();
    }

    // Obtener y mostrar recetas de bebidas saludables
    function getBebidasSaludables() {
        // Define la URL de la API para obtener recetas de bebidas sin alcohol
        var apiURL = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic';

        // Realiza una solicitud a la API
        fetch(apiURL)
            .then(response => response.json()) // Convierte la respuesta a JSON
            .then(data => {
                if (data && data.drinks) {
                    // Si la respuesta contiene datos de bebidas, llama a mostrarBebidas() con los datos
                    mostrarBebidas(data.drinks);
                } else {
                    // Si no se encuentran bebidas, muestra un mensaje informativo
                    mostrarMensaje('No se encontraron recetas de bebidas saludables.');
                }
            })
            .catch(error => {
                // Maneja errores de la solicitud
                console.error('Error al obtener las recetas de bebidas saludables:', error);
                mostrarMensaje('Ocurrió un error al obtener las recetas de bebidas saludables.');
            });
    }

    // Función para mostrar las recetas de bebidas en tarjetas HTML
    function mostrarBebidas(bebidas) {
        // Genera el HTML para las primeras 6 bebidas de la lista
        var bebidasHTML = bebidas.slice(0, 6).map(bebida => `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="${bebida.strDrinkThumb}" class="card-img-top" alt="${bebida.strDrink}">
                    <div class="card-body">
                        <h5 class="card-title">${bebida.strDrink}</h5>
                        <a href="https://www.thecocktaildb.com/drink.php?c=${bebida.idDrink}" target="_blank" rel="noopener noreferrer">Ver Receta</a>
                    </div>
                </div>
            </div>
        `).join('');

        // Inserta el HTML generado en el contenedor correspondiente
        $('#Recetas .row').html(bebidasHTML);
    }

    // Función para mostrar mensajes de error o información
    function mostrarMensaje(mensaje) {
        // Inserta un mensaje dentro del contenedor con clase 'row' dentro del elemento con ID 'Recetas'
        $('#Recetas .row').html(`<p>${mensaje}</p>`);
    }

    // Llamar a la función para obtener y mostrar las recetas de bebidas saludables al cargar la página
    getBebidasSaludables();

    // Ocultar el menú después de seleccionar una opción
    $('#nav a').click(function() {
        // Llama a la función seleccionar() cuando se hace clic en un enlace dentro del elemento con ID 'nav'
        seleccionar();
    });
});
