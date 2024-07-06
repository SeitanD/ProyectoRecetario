from django.contrib import admin
from .models import Receta, Comentario, Profile

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

# Eliminar los registros duplicados
# admin.site.register(Receta)
# admin.site.register(Comentario)
# admin.site.register(Profile)
