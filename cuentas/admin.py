from django.contrib import admin
from .models import Receta, Comentario, Profile, Valoracion, MensajeContacto, Categoria

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion')
    search_fields = ('titulo', 'autor__username')
    list_filter = ('fecha_creacion',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('receta', 'autor', 'fecha_creacion')
    search_fields = ('autor__username', 'receta__titulo')
    list_filter = ('fecha_creacion',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    filter_horizontal = ('favoritos',)

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('receta', 'usuario', 'puntuacion', 'fecha')
    search_fields = ('usuario__username', 'receta__titulo')
    list_filter = ('fecha', 'puntuacion')

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha')
    search_fields = ('nombre', 'email', 'asunto')
    list_filter = ('fecha',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
