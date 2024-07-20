from django.urls import path
from django.contrib.auth import views as auth_views
from cuentas import views

# Definición de las URL del proyecto
urlpatterns = [
    # Ruta para la página principal
    path('', views.index, name='index'),

    # Ruta para la página de aperitivos
    path('aperitivos/', views.aperitivos, name='aperitivos'),

    # Ruta para la página de comida
    path('comida/', views.comida, name='comida'),

    # Ruta para la página de batidos
    path('batidos/', views.batidos, name='batidos'),

    # Ruta para la página de contacto
    path('contacto/', views.contacto, name='contacto'),

    # Ruta para la página de inicio de sesión
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),

    # Ruta para la página de registro de nuevos usuarios
    path('registro/', views.registro, name='registro'),

    # Ruta para la página de olvido de contraseña
    path('olvido_contraseña/', auth_views.PasswordResetView.as_view(template_name='cuentas/olvido_contraseña.html'), name='olvido_contraseña'),

    # Ruta para la página del perfil del usuario
    path('perfil/', views.perfil, name='perfil'),

    # Ruta para la página del blog
    path('blog/', views.blog, name='blog'),

    # Ruta para la página de publicación de recetas
    path('publicar_receta/', views.publicar_receta, name='publicar_receta'),

    # Ruta para eliminar una receta
    path('eliminar_receta/<int:receta_id>/', views.eliminar_receta, name='eliminar_receta'),

    # Ruta para eliminar un comentario
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),

    # Ruta para agregar una receta a los favoritos
    path('add_to_favorites/<int:receta_id>/', views.add_to_favorites, name='add_to_favorites'),

    # Ruta para eliminar una receta de los favoritos
    path('eliminar_favorito/<int:receta_id>/', views.eliminar_favorito, name='eliminar_favorito'),

    # Ruta para agregar un comentario a una receta
    path('add_comment/<int:receta_id>/', views.add_comment, name='add_comment'),

    # Ruta para cerrar sesión
    path('logout/', views.custom_logout_view, name='logout'),

    # Ruta para editar una receta
    path('editar_receta/<int:receta_id>/', views.editar_receta, name='editar_receta'),

    # Ruta para editar un comentario
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),

    # Ruta para actualizar el perfil del usuario
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),

    # Ruta para eliminar la cuenta del usuario
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),

    # Ruta para agregar una valoración a una receta
    path('add_rating/<int:receta_id>/', views.add_rating, name='add_rating'),

    # Ruta para listar las valoraciones de una receta
    path('listar_valoraciones/<int:receta_id>/', views.listar_valoraciones, name='listar_valoraciones'),

    # Ruta para eliminar una valoración
    path('eliminar_valoracion/<int:valoracion_id>/', views.eliminar_valoracion, name='eliminar_valoracion'),

    # Ruta para listar mensajes de contacto
    path('listar_mensajes_contacto/', views.listar_mensajes_contacto, name='listar_mensajes_contacto'),

    # Ruta para eliminar un mensaje de contacto
    path('eliminar_mensaje_contacto/<int:mensaje_id>/', views.eliminar_mensaje_contacto, name='eliminar_mensaje_contacto'),

    # Ruta para listar categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),

    # Ruta para crear una categoría
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),

    # Ruta para editar una categoría
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),

    # Ruta para eliminar una categoría
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Nuevas rutas para la tienda y el carrito de compras
    # Ruta para la página de la tienda
    path('tienda/', views.tienda, name='tienda'),

    # Ruta para crear un producto en la tienda
    path('tienda/crear/', views.crear_producto, name='crear_producto'),

    # Ruta para editar un producto en la tienda
    path('tienda/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),

    # Ruta para eliminar un producto de la tienda
    path('tienda/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # Ruta para ver el carrito de compras
    path('carrito/', views.ver_carrito, name='ver_carrito'),

    # Ruta para agregar un producto al carrito de compras
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    # Ruta para actualizar un ítem en el carrito de compras
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),

    # Ruta para eliminar un ítem del carrito de compras
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    # Ruta para validar un pedido
    path('carrito/validar/', views.validar_pedido, name='validar_pedido'),

    # Ruta para ver los pedidos del usuario
    path('pedidos/', views.ver_pedidos, name='ver_pedidos'),
]
