from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modelo para las categorías de recetas
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo para las recetas
class Receta(models.Model):
    titulo = models.CharField(max_length=100, default='Título de la receta')  # Título de la receta
    ingredientes = models.TextField(default='Ingredientes no especificados')  # Ingredientes de la receta
    preparacion = models.TextField(default='Preparación no especificada')  # Método de preparación
    imagen = models.ImageField(upload_to='recetas/', default='path/to/default/image.jpg')  # Imagen de la receta
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor de la receta
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la receta
    valoracion = models.FloatField(default=0.0)  # Valoración promedio de la receta
    total_valoraciones = models.IntegerField(default=0)  # Número total de valoraciones
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría de la receta

    def __str__(self):
        return self.titulo

# Modelo para las valoraciones de las recetas
class Valoracion(models.Model):
    receta = models.ForeignKey(Receta, related_name='valoraciones', on_delete=models.CASCADE)  # Receta valorada
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que realizó la valoración
    puntuacion = models.PositiveSmallIntegerField()  # Puntuación de la valoración
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de la valoración

    class Meta:
        unique_together = ('receta', 'usuario')  # Asegura que un usuario solo pueda valorar una receta una vez

# Modelo para los comentarios en las recetas
class Comentario(models.Model):
    receta = models.ForeignKey(Receta, related_name='comentarios', on_delete=models.CASCADE)  # Receta comentada
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor del comentario
    texto = models.TextField()  # Texto del comentario
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del comentario

    def __str__(self):
        return f'Comentario de {self.autor} en {self.receta}'

# Modelo para el perfil de usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Usuario al que pertenece el perfil
    favoritos = models.ManyToManyField(Receta, blank=True)  # Recetas favoritas del usuario

    def __str__(self):
        return self.user.username

# Señal para crear el perfil de usuario cuando se crea un nuevo usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Señal para guardar el perfil de usuario cuando se guarda un usuario
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Modelo para los mensajes de contacto
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del remitente
    email = models.EmailField()  # Email del remitente
    telefono = models.CharField(max_length=15, blank=True)  # Teléfono del remitente
    asunto = models.CharField(max_length=200)  # Asunto del mensaje
    mensaje = models.TextField()  # Texto del mensaje
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de envío del mensaje

    def __str__(self):
        return f'Mensaje de {self.nombre} - {self.email}'

# Modelo para el carrito de compras
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Usuario al que pertenece el carrito
    creado_en = models.DateTimeField(auto_now_add=True)  # Fecha de creación del carrito

    def __str__(self):
        return f'Carrito de {self.usuario.username}'

# Modelo para los productos en la tienda
class Producto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField()  # Descripción del producto
    precio = models.IntegerField()  # Precio del producto
    imagen = models.ImageField(upload_to='productos/', default='path/to/default/image.jpg')  # Imagen del producto
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del producto

    def __str__(self):
        return self.nombre

# Modelo para los ítems del carrito de compras
class ProductoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)  # Carrito al que pertenece el ítem
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto agregado al carrito
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad del producto

    def __str__(self):
        return f'{self.cantidad} de {self.producto.nombre}'

# Modelo para los pedidos
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que realiza el pedido
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto pedido
    cantidad = models.PositiveIntegerField()  # Cantidad del producto pedido
    fecha_pedido = models.DateTimeField(auto_now_add=True)  # Fecha del pedido

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre}'
