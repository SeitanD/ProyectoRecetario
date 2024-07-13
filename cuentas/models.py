from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Receta(models.Model):
    titulo = models.CharField(max_length=100, default='Título de la receta')
    ingredientes = models.TextField(default='Ingredientes no especificados')
    preparacion = models.TextField(default='Preparación no especificada')
    imagen = models.ImageField(upload_to='recetas/', default='path/to/default/image.jpg')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    valoracion = models.FloatField(default=0.0)
    total_valoraciones = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo
    
class Valoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='valoraciones')
    puntuacion = models.IntegerField()


class Comentario(models.Model):
    receta = models.ForeignKey(Receta, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor} en {self.receta}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favoritos = models.ManyToManyField(Receta, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

