from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aperitivos/', views.aperitivos, name='aperitivos'),
    path('comida/', views.comida, name='comida'),
    path('batidos/', views.batidos, name='batidos'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('olvido-contraseña/', views.olvido_contraseña, name='olvido-contraseña'),
]
