from django.contrib import admin  # Importa el módulo de administración de Django
from .models import Receta, Comentario, Profile  # Importa los modelos Receta, Comentario y Profile del archivo models.py

@admin.register(Receta)  # Registra el modelo Receta en el sitio de administración usando un decorador
class RecetaAdmin(admin.ModelAdmin):  # Define una clase para personalizar la administración del modelo Receta
    list_display = ('titulo', 'autor', 'fecha_creacion')  # Muestra las columnas 'titulo', 'autor' y 'fecha_creacion' en la lista de recetas
    search_fields = ('titulo', 'autor__username')  # Permite buscar recetas por 'titulo' y el 'username' del autor
    list_filter = ('fecha_creacion',)  # Añade un filtro lateral para filtrar recetas por 'fecha_creacion'

@admin.register(Comentario)  # Registra el modelo Comentario en el sitio de administración usando un decorador
class ComentarioAdmin(admin.ModelAdmin):  # Define una clase para personalizar la administración del modelo Comentario
    list_display = ('receta', 'autor', 'fecha_creacion')  # Muestra las columnas 'receta', 'autor' y 'fecha_creacion' en la lista de comentarios
    search_fields = ('autor__username', 'receta__titulo')  # Permite buscar comentarios por el 'username' del autor y el 'titulo' de la receta
    list_filter = ('fecha_creacion',)  # Añade un filtro lateral para filtrar comentarios por 'fecha_creacion'

@admin.register(Profile)  # Registra el modelo Profile en el sitio de administración usando un decorador
class ProfileAdmin(admin.ModelAdmin):  # Define una clase para personalizar la administración del modelo Profile
    list_display = ('user',)  # Muestra la columna 'user' en la lista de perfiles
    search_fields = ('user__username',)  # Permite buscar perfiles por el 'username' del usuario
    filter_horizontal = ('favoritos',)  # Configura un selector horizontal para el campo 'favoritos' en el modelo Profile

# Eliminar los registros duplicados
# admin.site.register(Receta)  # Registro directo del modelo Receta (comentado para evitar duplicados)
# admin.site.register(Comentario)  # Registro directo del modelo Comentario (comentado para evitar duplicados)
# admin.site.register(Profile)  # Registro directo del modelo Profile (comentado para evitar duplicados)

