$(document).ready(function() {
    // URL de la API de MealDB para obtener recetas aleatorias
    var apiURL = "https://www.themealdb.com/api/json/v1/1/random.php";

    // Número de recetas que deseas obtener
    var numRecipes = 6;

    // Función para obtener y mostrar recetas
    function getRecipes() {
        // Iterar para obtener el número deseado de recetas
        for (var i = 0; i < numRecipes; i++) {
            // Realizar una solicitud GET a la API para obtener una receta aleatoria
            $.get(apiURL, function(data) {
                // Iterar sobre las recetas obtenidas en la respuesta
                data.meals.forEach(function(recipe) {
                    // Crear una tarjeta de receta con la información obtenida
                    var recipeCard = `
                        <div class="col-md-4 mb-4">
                            <div class="card h-100">
                                <img src="${recipe.strMealThumb}" class="card-img-top" alt="${recipe.strMeal}">
                                <div class="card-body">
                                    <h5 class="card-title">${recipe.strMeal}</h5>
                                    <p class="card-text">${recipe.strInstructions.slice(0, 100)}...</p>
                                    <button class="btn btn-primary btn-show-recipe">Ver Receta</button>
                                    <div class="recipe-content" style="display: none;">
                                        <p>${recipe.strInstructions}</p>
                                    </div>
                                </div>
                            </div>
                        </div>`;
                    
                    // Agregar la tarjeta de receta al contenedor
                    $('#recipeCards').append(recipeCard);
                });
            });
        }
    }

    // Llamar a la función para obtener las recetas cuando el documento esté listo
    getRecipes();

    // Evento de clic en el botón "Ver Receta"
    $(document).on('click', '.btn-show-recipe', function() {
        // Obtener el contenido de la receta asociado al botón clicado
        var recipeContent = $(this).siblings('.recipe-content');
        // Alternar la visibilidad del contenido de la receta
        if (recipeContent.is(':visible')) {
            recipeContent.slideUp();
        } else {
            recipeContent.slideDown();
        }
    });
});
