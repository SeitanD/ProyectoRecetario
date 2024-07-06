from django.urls import path  # Importa el módulo path para definir las rutas de URL
from django.contrib.auth import views as auth_views  # Importa las vistas de autenticación de Django con un alias
from cuentas import views as cuentas_views  # Importa las vistas de la aplicación cuentas con un alias

urlpatterns = [
    path('', cuentas_views.index, name='index'),  # Ruta para la vista de índice, la página principal
    path('aperitivos/', cuentas_views.aperitivos, name='aperitivos'),  # Ruta para la vista de aperitivos
    path('comida/', cuentas_views.comida, name='comida'),  # Ruta para la vista de comida
    path('batidos/', cuentas_views.batidos, name='batidos'),  # Ruta para la vista de batidos
    path('contacto/', cuentas_views.contacto, name='contacto'),  # Ruta para la vista de contacto
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),  # Ruta para la vista de inicio de sesión, usando la vista de inicio de sesión de Django con una plantilla personalizada
    path('registro/', cuentas_views.registro, name='registro'),  # Ruta para la vista de registro de nuevos usuarios
    path('olvido_contraseña/', auth_views.PasswordResetView.as_view(template_name='cuentas/olvido_contraseña.html'), name='olvido_contraseña'),  # Ruta para la vista de restablecimiento de contraseña, usando la vista de Django con una plantilla personalizada
    path('perfil/', cuentas_views.perfil, name='perfil'),  # Ruta para la vista del perfil de usuario
    path('blog/', cuentas_views.blog, name='blog'),  # Ruta para la vista del blog
    path('eliminar_receta/<int:receta_id>/', cuentas_views.eliminar_receta, name='eliminar_receta'),  # Ruta para eliminar una receta, pasando el ID de la receta
    path('eliminar_comentario/<int:comentario_id>/', cuentas_views.eliminar_comentario, name='eliminar_comentario'),  # Ruta para eliminar un comentario, pasando el ID del comentario
    path('add_to_favorites/<int:receta_id>/', cuentas_views.add_to_favorites, name='add_to_favorites'),  # Ruta para añadir una receta a favoritos, pasando el ID de la receta
    path('eliminar_favorito/<int:receta_id>/', cuentas_views.eliminar_favorito, name='eliminar_favorito'),  # Ruta para eliminar una receta de favoritos, pasando el ID de la receta
    path('add_comment/<int:receta_id>/', cuentas_views.add_comment, name='add_comment'),  # Ruta para añadir un comentario a una receta, pasando el ID de la receta
    path('logout/', cuentas_views.custom_logout_view, name='logout'),  # Ruta para cerrar sesión, usando una vista personalizada
    path('editar_receta/<int:receta_id>/', cuentas_views.editar_receta, name='editar_receta'),  # Ruta para editar una receta, pasando el ID de la receta
    path('editar_comentario/<int:comentario_id>/', cuentas_views.editar_comentario, name='editar_comentario'),  # Ruta para editar un comentario, pasando el ID del comentario
    path('actualizar_perfil/', cuentas_views.actualizar_perfil, name='actualizar_perfil'),  # Ruta para actualizar el perfil de usuario
    path('eliminar_cuenta/', cuentas_views.eliminar_cuenta, name='eliminar_cuenta'),  # Ruta para eliminar una cuenta de usuario
]
