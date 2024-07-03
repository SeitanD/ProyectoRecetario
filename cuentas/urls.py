from django.urls import path
from .views import index, aperitivos

urlpatterns = [
    path('', index, name='index'),
    path('aperitivos', aperitivos, name='aperitivos'),
]