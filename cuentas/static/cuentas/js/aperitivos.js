// Función para obtener y mostrar recetas de aperitivos
function getAperitivos() {
    // URL de la API de TheMealDB para obtener recetas de aperitivos
    var apiURL = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=Appetizer';

    // Realizar la solicitud a la API
    fetch(apiURL)
        .then(response => {
            // Verificar si la respuesta de la API es exitosa
            if (!response.ok) {
                throw new Error('La solicitud no fue exitosa. Código: ' + response.status);
            }
            // Convertir la respuesta a JSON
            return response.json();
        })
        .then(data => {
            // Imprimir los datos en la consola para depuración
            console.log('Datos recibidos:', data);
            // Verificar si se obtuvieron datos y procesarlos
            if (data && data.meals) {
                // Si se obtienen datos de la API, procesar y mostrar las recetas
                mostrarRecetas(data.meals);
            } else {
                // Manejar la situación donde no se encuentran recetas
                mostrarMensaje('No se encontraron recetas de aperitivos.');
            }
        })
        .catch(error => {
            // Manejar errores de la solicitud
            console.error('Error al obtener las recetas de aperitivos:', error);
            mostrarMensaje('Ocurrió un error al obtener las recetas de aperitivos.');
        });
}

// Función para mostrar las recetas de aperitivos en tarjetas HTML
function mostrarRecetas(recetas) {
    // Crear una variable para almacenar el HTML de las recetas
    var recetasHTML = '';
    // Iterar sobre cada receta y generar el HTML correspondiente
    recetas.forEach(function(receta) {
        recetasHTML += `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="${receta.strMealThumb}" class="card-img-top" alt="${receta.strMeal}">
                    <div class="card-body">
                        <h5 class="card-title">${receta.strMeal}</h5>
                        <p class="card-text">${receta.strInstructions.slice(0, 100)}...</p>
                        <button class="btn btn-primary btn-show-recipe">Ver Receta</button>
                        <div class="recipe-content" style="display: none;">
                            <p>${receta.strInstructions}</p>
                        </div>
                    </div>
                </div>
            </div>`;
    });
    // Agregar las tarjetas de recetas al contenedor en el HTML
    document.getElementById('recetas-dinamicas').innerHTML = recetasHTML;
}

// Función para mostrar mensajes de error o información en caso de problemas
function mostrarMensaje(mensaje) {
    // Mostrar el mensaje dentro del contenedor de recetas
    document.getElementById('recetas-dinamicas').innerHTML = `<p>${mensaje}</p>`;
}

// Llamar a la función para obtener y mostrar las recetas de aperitivos al cargar la página
window.onload = function() {
    getAperitivos();
};
