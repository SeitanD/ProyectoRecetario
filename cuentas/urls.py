from django.urls import path
from django.contrib.auth import views as auth_views
from cuentas import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aperitivos/', views.aperitivos, name='aperitivos'),
    path('comida/', views.comida, name='comida'),
    path('batidos/', views.batidos, name='batidos'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('registro/', views.registro, name='registro'),
    path('olvido_contraseña/', auth_views.PasswordResetView.as_view(template_name='cuentas/olvido_contraseña.html'), name='olvido_contraseña'),
    path('perfil/', views.perfil, name='perfil'),
    path('blog/', views.blog, name='blog'),
    path('publicar_receta/', views.publicar_receta, name='publicar_receta'),
    path('eliminar_receta/<int:receta_id>/', views.eliminar_receta, name='eliminar_receta'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('add_to_favorites/<int:receta_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('eliminar_favorito/<int:receta_id>/', views.eliminar_favorito, name='eliminar_favorito'),
    path('add_comment/<int:receta_id>/', views.add_comment, name='add_comment'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('editar_receta/<int:receta_id>/', views.editar_receta, name='editar_receta'),
    path('editar_comentario/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('add_rating/<int:receta_id>/', views.add_rating, name='add_rating'),
    path('listar_valoraciones/<int:receta_id>/', views.listar_valoraciones, name='listar_valoraciones'),
    path('eliminar_valoracion/<int:valoracion_id>/', views.eliminar_valoracion, name='eliminar_valoracion'),
    path('listar_mensajes_contacto/', views.listar_mensajes_contacto, name='listar_mensajes_contacto'),
    path('eliminar_mensaje_contacto/<int:mensaje_id>/', views.eliminar_mensaje_contacto, name='eliminar_mensaje_contacto'),

    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Nuevas rutas para la tienda y el carrito de compras
    path('tienda/', views.tienda, name='tienda'),
    path('tienda/crear/', views.crear_producto, name='crear_producto'),
    path('tienda/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('tienda/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
]

