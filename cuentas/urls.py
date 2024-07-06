from django.urls import path
from django.contrib.auth import views as auth_views
from cuentas import views as cuentas_views

urlpatterns = [
    path('', cuentas_views.index, name='index'),
    path('aperitivos/', cuentas_views.aperitivos, name='aperitivos'),
    path('comida/', cuentas_views.comida, name='comida'),
    path('batidos/', cuentas_views.batidos, name='batidos'),
    path('contacto/', cuentas_views.contacto, name='contacto'),
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('registro/', cuentas_views.registro, name='registro'),
    path('olvido_contraseña/', auth_views.PasswordResetView.as_view(template_name='cuentas/olvido_contraseña.html'), name='olvido_contraseña'),
    path('perfil/', cuentas_views.perfil, name='perfil'),
    path('blog/', cuentas_views.blog, name='blog'),
    path('eliminar_receta/<int:receta_id>/', cuentas_views.eliminar_receta, name='eliminar_receta'),
    path('eliminar_comentario/<int:comentario_id>/', cuentas_views.eliminar_comentario, name='eliminar_comentario'),
    path('add_to_favorites/<int:receta_id>/', cuentas_views.add_to_favorites, name='add_to_favorites'),
    path('eliminar_favorito/<int:receta_id>/', cuentas_views.eliminar_favorito, name='eliminar_favorito'),
    path('add_comment/<int:receta_id>/', cuentas_views.add_comment, name='add_comment'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('editar_receta/<int:receta_id>/', cuentas_views.editar_receta, name='editar_receta'),
    path('editar_comentario/<int:comentario_id>/', cuentas_views.editar_comentario, name='editar_comentario'),
    path('actualizar_perfil/', cuentas_views.actualizar_perfil, name='actualizar_perfil'),
    path('eliminar_cuenta/', cuentas_views.eliminar_cuenta, name='eliminar_cuenta'),

]
