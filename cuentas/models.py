from django.db import models  # Importa el módulo models de Django
from django.contrib.auth.models import User  # Importa el modelo User del módulo de autenticación de Django
from django.db.models.signals import post_save  # Importa la señal post_save
from django.dispatch import receiver  # Importa el decorador receiver para conectar señales

class Receta(models.Model):  # Define el modelo Receta
    titulo = models.CharField(max_length=500)  # Campo de texto con un máximo de 500 caracteres para el título
    descripcion = models.TextField()  # Campo de texto para la descripción
    imagen = models.ImageField(upload_to='recetas/')  # Campo de imagen que se sube a la carpeta 'recetas/'
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación muchos a uno con el modelo User, elimina la receta si el usuario se elimina
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Campo de fecha y hora que se establece automáticamente al crear la receta

    def __str__(self):  # Método de cadena para representar el modelo
        return self.titulo  # Devuelve el título de la receta como su representación

class Comentario(models.Model):  # Define el modelo Comentario
    receta = models.ForeignKey(Receta, related_name='comentarios', on_delete=models.CASCADE)  # Relación muchos a uno con el modelo Receta, elimina los comentarios si la receta se elimina
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación muchos a uno con el modelo User, elimina el comentario si el usuario se elimina
    texto = models.TextField()  # Campo de texto para el comentario
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Campo de fecha y hora que se establece automáticamente al crear el comentario

    def __str__(self):  # Método de cadena para representar el modelo
        return f'Comentario de {self.autor} en {self.receta}'  # Devuelve una representación del comentario

class Profile(models.Model):  # Define el modelo Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo User, elimina el perfil si el usuario se elimina
    favoritos = models.ManyToManyField('Receta', blank=True)  # Relación muchos a muchos con el modelo Receta, permite estar en blanco

    def __str__(self):  # Método de cadena para representar el modelo
        return self.user.username  # Devuelve el nombre de usuario del perfil como su representación

@receiver(post_save, sender=User)  # Conecta la señal post_save del modelo User
def create_user_profile(sender, instance, created, **kwargs):  # Define la función para crear un perfil de usuario
    if created:  # Si el usuario fue creado
        Profile.objects.create(user=instance)  # Crea un perfil para el usuario

@receiver(post_save, sender=User)  # Conecta la señal post_save del modelo User
def save_user_profile(sender, instance, **kwargs):  # Define la función para guardar un perfil de usuario
    instance.profile.save()  # Guarda el perfil del usuario
