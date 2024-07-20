from django.contrib import admin
from .models import Receta, Comentario, Profile, Valoracion, MensajeContacto, Categoria, Producto, Carrito, ProductoItem

# Configuración del modelo Receta para el administrador
@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de recetas
    list_display = ('titulo', 'autor', 'fecha_creacion')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('titulo', 'autor__username')
    # Filtros disponibles para la lista de recetas
    list_filter = ('fecha_creacion',)

# Configuración del modelo Comentario para el administrador
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de comentarios
    list_display = ('receta', 'autor', 'fecha_creacion')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('autor__username', 'receta__titulo')
    # Filtros disponibles para la lista de comentarios
    list_filter = ('fecha_creacion',)

# Configuración del modelo Profile para el administrador
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Campo a mostrar en la lista de perfiles
    list_display = ('user',)
    # Campos por los que se puede buscar en el administrador
    search_fields = ('user__username',)
    # Habilitar selección múltiple de recetas favoritas
    filter_horizontal = ('favoritos',)

# Configuración del modelo Valoracion para el administrador
@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de valoraciones
    list_display = ('receta', 'usuario', 'puntuacion', 'fecha')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('usuario__username', 'receta__titulo')
    # Filtros disponibles para la lista de valoraciones
    list_filter = ('fecha', 'puntuacion')

# Configuración del modelo MensajeContacto para el administrador
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de mensajes de contacto
    list_display = ('nombre', 'email', 'asunto', 'fecha')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('nombre', 'email', 'asunto')
    # Filtros disponibles para la lista de mensajes de contacto
    list_filter = ('fecha',)

# Configuración del modelo Categoria para el administrador
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Campo a mostrar en la lista de categorías
    list_display = ('nombre',)
    # Campo por el que se puede buscar en el administrador
    search_fields = ('nombre',)

# Configuración del modelo Producto para el administrador
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de productos
    list_display = ('nombre', 'precio', 'fecha_creacion')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('nombre',)
    # Filtros disponibles para la lista de productos
    list_filter = ('fecha_creacion',)

# Configuración del modelo Carrito para el administrador
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de carritos
    list_display = ('usuario', 'creado_en')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('usuario__username',)
    # Filtros disponibles para la lista de carritos
    list_filter = ('creado_en',)

# Configuración del modelo ProductoItem para el administrador
@admin.register(ProductoItem)
class ProductoItemAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de ítems de producto
    list_display = ('carrito', 'producto', 'cantidad')
    # Campos por los que se puede buscar en el administrador
    search_fields = ('carrito__usuario__username', 'producto__nombre')
