from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from .models import Receta, Comentario, Profile, Valoracion, MensajeContacto, Categoria, Carrito, ProductoItem, Producto, Pedido
from .forms import RecetaForm, ComentarioForm, UserRegistroForm, UserUpdateForm, ContactForm, ValoracionForm, CategoriaForm, ProductoItemForm, ProductoForm
from django.db import models
from django.views.decorators.csrf import csrf_exempt

# Vista para la página principal
def index(request):
    # Renderiza la plantilla 'index.html'
    return render(request, 'cuentas/index.html')

# Vista para la página de aperitivos
def aperitivos(request):
    # Renderiza la plantilla 'aperitivos.html'
    return render(request, 'cuentas/aperitivos.html')

# Vista para la página de comida
def comida(request):
    # Renderiza la plantilla 'comida.html'
    return render(request, 'cuentas/comida.html')

# Vista para la página de batidos
def batidos(request):
    # Renderiza la plantilla 'batidos.html'
    return render(request, 'cuentas/batidos.html')

# Vista para la página de inicio de sesión
def login_view(request):
    # Renderiza la plantilla 'login.html'
    return render(request, 'cuentas/login.html')

# Vista para el registro de nuevos usuarios
def registro(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de registro con los datos enviados
        form = UserRegistroForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda el nuevo usuario
            user = form.save()
            # Inicia sesión automáticamente al nuevo usuario
            login(request, user)
            # Asigna el nuevo usuario al grupo 'User'
            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')
            # Redirige a la página principal
            return redirect('index')
        else:
            messages.error(request, 'Error al registrarse. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario vacío
        form = UserRegistroForm()
    # Renderiza la plantilla 'registro.html' con el formulario de registro
    return render(request, 'cuentas/registro.html', {'form': form})

def blog(request):
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        # Filtra las recetas por la categoría seleccionada
        recetas = Receta.objects.filter(categoria_id=categoria_id)
    else:
        # Obtiene todas las recetas si no se selecciona ninguna categoría
        recetas = Receta.objects.all()
    # Obtiene todas las categorías para mostrarlas en el filtro
    categorias = Categoria.objects.all()
    comentario_form = ComentarioForm()
    
    context = {
        'recetas': recetas,
        'categorias': categorias,
        'comentario_form': comentario_form
    }
    
    # Renderiza la plantilla 'blog.html' con las recetas y categorías
    return render(request, 'cuentas/blog.html', context)

# Vista para publicar recetas (requiere autenticación)
@login_required
def publicar_receta(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de receta con los datos enviados
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            # Si el formulario es válido, guarda la receta pero sin guardar en la base de datos todavía
            receta = form.save(commit=False)
            # Asigna el usuario actual como autor de la receta
            receta.autor = request.user
            # Guarda la receta en la base de datos
            receta.save()
            messages.success(request, '¡Receta creada con éxito!')
            # Redirige al blog
            return redirect('blog')
        else:
            messages.error(request, 'Error al crear la receta. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario vacío
        form = RecetaForm()
    # Renderiza la plantilla 'publicar_receta.html' con el formulario de receta
    return render(request, 'cuentas/publicar_receta.html', {'form': form})

# Vista para agregar comentario (requiere autenticación)
@login_required
def add_comment(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == 'POST':
        # Crea un formulario de comentario con los datos enviados
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            # Si el formulario es válido, guarda el comentario pero sin guardar en la base de datos todavía
            comentario = comentario_form.save(commit=False)
            # Asigna la receta y el autor al comentario
            comentario.receta = receta
            comentario.autor = request.user
            # Guarda el comentario en la base de datos
            comentario.save()
            messages.success(request, '¡Comentario agregado con éxito!')
        else:
            messages.error(request, 'Error al agregar el comentario. Por favor, corrige los errores.')
    return redirect('blog')

@login_required
def add_rating(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == 'POST':
        # Crea un formulario de valoración con los datos enviados
        form = ValoracionForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, obtiene la puntuación
            puntuacion = form.cleaned_data['puntuacion']
            # Crea o actualiza la valoración del usuario para la receta
            valoracion, created = Valoracion.objects.update_or_create(
                receta=receta,
                usuario=request.user,
                defaults={'puntuacion': puntuacion},
            )
            # Calcula la nueva valoración promedio y el total de valoraciones
            nueva_valoracion = receta.valoraciones.aggregate(models.Avg('puntuacion'))['puntuacion__avg']
            total_valoraciones = receta.valoraciones.count()
            receta.valoracion = nueva_valoracion
            receta.total_valoraciones = total_valoraciones
            receta.save()
            # Devuelve la nueva valoración promedio y el total de valoraciones como JSON
            return JsonResponse({
                'new_rating': nueva_valoracion,
                'total_ratings': total_valoraciones
            })
        else:
            return JsonResponse({'error': 'Formulario no válido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista para listar valoraciones de una receta
@login_required
def listar_valoraciones(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    # Obtiene todas las valoraciones de la receta
    valoraciones = Valoracion.objects.filter(receta=receta)
    # Renderiza la plantilla 'listar_valoraciones.html' con las valoraciones
    return render(request, 'cuentas/listar_valoraciones.html', {'receta': receta, 'valoraciones': valoraciones})

# Vista para eliminar una valoración
@login_required
def eliminar_valoracion(request, valoracion_id):
    # Obtiene la valoración correspondiente al ID
    valoracion = get_object_or_404(Valoracion, id=valoracion_id)
    if valoracion.usuario == request.user:
        # Si el usuario es el autor de la valoración, la elimina
        valoracion.delete()
        messages.success(request, 'Valoración eliminada con éxito.')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta valoración.')
    return redirect('blog')

# Vista para eliminar una receta
@login_required
def eliminar_receta(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == "POST" and receta.autor == request.user:
        # Si el método de la solicitud es POST y el usuario es el autor, elimina la receta
        receta.delete()
        messages.success(request, 'Receta eliminada con éxito.')
    return redirect('blog')

# Vista para eliminar un comentario
@login_required
def eliminar_comentario(request, comentario_id):
    # Obtiene el comentario correspondiente al ID
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == "POST" and comentario.autor == request.user:
        # Si el método de la solicitud es POST y el usuario es el autor, elimina el comentario
        comentario.delete()
        messages.success(request, 'Comentario eliminado con éxito.')
    return redirect('blog')

# Vista para agregar una receta a los favoritos
@login_required
def add_to_favorites(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    profile = request.user.profile
    if receta not in profile.favoritos.all():
        # Si la receta no está en los favoritos, la añade
        profile.favoritos.add(receta)
        messages.success(request, '¡Receta añadida a tus favoritos!')
    else:
        messages.info(request, 'Esta receta ya está en tus favoritos.')
    return redirect('blog')

# Vista para eliminar una receta de los favoritos
@login_required
def eliminar_favorito(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    # Elimina la receta de los favoritos del usuario
    request.user.profile.favoritos.remove(receta)
    messages.success(request, 'Receta eliminada de tus favoritos.')
    return redirect('perfil')

# Vista para mostrar el perfil del usuario
@login_required
def perfil(request):
    profile = request.user.profile
    # Obtiene las recetas favoritas del usuario
    recetas_favoritas = profile.favoritos.all()
    # Renderiza la plantilla 'perfil.html' con la información del perfil y las recetas favoritas
    return render(request, 'cuentas/perfil.html', {'user': request.user, 'recetas_favoritas': recetas_favoritas})

# Vista para editar una receta
@login_required
def editar_receta(request, receta_id):
    # Obtiene la receta correspondiente al ID
    receta = get_object_or_404(Receta, id=receta_id)
    if receta.autor != request.user:
        # Si el usuario no es el autor, redirige al blog
        return redirect('blog')
    if request.method == "POST":
        # Si el método de la solicitud es POST, crea un formulario de receta con los datos enviados
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en la receta
            form.save()
            messages.success(request, 'Receta editada con éxito.')
            return redirect('blog')
        else:
            messages.error(request, 'Error al editar la receta. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario con los datos de la receta
        form = RecetaForm(instance=receta)
    # Renderiza la plantilla 'editar_receta.html' con el formulario de receta
    return render(request, 'cuentas/editar_receta.html', {'form': form})

# Vista para editar un comentario
@login_required
def editar_comentario(request, comentario_id):
    # Obtiene el comentario correspondiente al ID
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.autor != request.user:
        # Si el usuario no es el autor, redirige al blog
        return redirect('blog')
    if request.method == "POST":
        # Si el método de la solicitud es POST, crea un formulario de comentario con los datos enviados
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en el comentario
            form.save()
            messages.success(request, 'Comentario editado con éxito.')
            return redirect('blog')
        else:
            messages.error(request, 'Error al editar el comentario. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario con los datos del comentario
        form = ComentarioForm(instance=comentario)
    # Renderiza la plantilla 'editar_comentario.html' con el formulario de comentario
    return render(request, 'cuentas/editar_comentario.html', {'form': form})

# Vista para actualizar el perfil del usuario
@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de actualización con los datos enviados
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en el usuario
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario con los datos del usuario
        form = UserUpdateForm(instance=request.user)
    # Renderiza la plantilla 'actualizar_perfil.html' con el formulario de actualización
    return render(request, 'cuentas/actualizar_perfil.html', {'form': form})

# Vista para eliminar la cuenta del usuario
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, elimina la cuenta del usuario
        user = request.user
        user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada con éxito.')
        return redirect('index')
    # Renderiza la plantilla 'eliminar_cuenta.html' para confirmar la eliminación
    return render(request, 'cuentas/eliminar_cuenta.html')

# Vista para cerrar sesión
def custom_logout_view(request):
    # Cierra la sesión del usuario y redirige a la página de inicio de sesión
    logout(request)
    return redirect('login')

# Vista para manejar mensajes de contacto
@csrf_exempt
def contacto(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de contacto con los datos enviados
        form = ContactForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda el mensaje de contacto
            form.save()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'error', 'errors': form.errors})
    else:
        # Si el método de la solicitud no es POST, muestra un formulario vacío
        form = ContactForm()
    # Renderiza la plantilla 'contacto.html' con el formulario de contacto
    return render(request, 'cuentas/contacto.html', {'form': form})

# Vista para listar mensajes de contacto
@login_required
def listar_mensajes_contacto(request):
    # Obtiene todos los mensajes de contacto
    mensajes = MensajeContacto.objects.all()
    # Renderiza la plantilla 'listar_mensajes_contacto.html' con los mensajes
    return render(request, 'cuentas/listar_mensajes_contacto.html', {'mensajes': mensajes})

# Vista para eliminar mensaje de contacto
@login_required
def eliminar_mensaje_contacto(request, mensaje_id):
    # Obtiene el mensaje de contacto correspondiente al ID
    mensaje = get_object_or_404(MensajeContacto, id=mensaje_id)
    if request.method == "POST":
        # Si el método de la solicitud es POST, elimina el mensaje
        mensaje.delete()
        messages.success(request, 'Mensaje de contacto eliminado con éxito.')
    return redirect('listar_mensajes_contacto')

@login_required
def listar_categorias(request):
    # Obtiene todas las categorías
    categorias = Categoria.objects.all()
    # Renderiza la plantilla 'listar_categorias.html' con las categorías
    return render(request, 'cuentas/listar_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de categoría con los datos enviados
        form = CategoriaForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guarda la nueva categoría
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('listar_categorias')
        else:
            messages.error(request, 'Error al crear la categoría. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario vacío
        form = CategoriaForm()
    # Renderiza la plantilla 'crear_categoria.html' con el formulario de categoría
    return render(request, 'cuentas/crear_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    # Obtiene la categoría correspondiente al ID
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de categoría con los datos enviados
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en la categoría
            form.save()
            messages.success(request, '¡Categoría actualizada exitosamente!')
            return redirect('listar_categorias')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario con los datos de la categoría
        form = CategoriaForm(instance=categoria)
    # Renderiza la plantilla 'editar_categoria.html' con el formulario de categoría
    return render(request, 'cuentas/editar_categoria.html', {'form': form})

@login_required
def eliminar_categoria(request, categoria_id):
    # Obtiene la categoría correspondiente al ID
    categoria = get_object_or_404(Categoria, id=categoria_id)
    # Elimina la categoría
    categoria.delete()
    messages.success(request, '¡Categoría eliminada exitosamente!')
    return redirect('listar_categorias')

@login_required
def tienda(request):
    # Obtiene todos los productos
    productos = Producto.objects.all()
    # Renderiza la plantilla 'tienda.html' con los productos
    return render(request, 'cuentas/tienda.html', {'productos': productos})

@login_required
def ver_carrito(request):
    # Obtiene o crea un carrito para el usuario actual
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    # Renderiza la plantilla 'ver_carrito.html' con el carrito
    return render(request, 'cuentas/ver_carrito.html', {'carrito': carrito})

@login_required
def agregar_al_carrito(request, producto_id):
    # Obtiene el producto correspondiente al ID
    producto = get_object_or_404(Producto, id=producto_id)
    # Obtiene o crea un carrito para el usuario actual
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    # Obtiene la cantidad de producto a agregar
    cantidad = int(request.POST.get('cantidad', 1))
    # Obtiene o crea un ítem de producto en el carrito
    item, created = ProductoItem.objects.get_or_create(carrito=carrito, producto=producto)
    # Incrementa la cantidad del ítem
    item.cantidad += cantidad
    # Guarda el ítem
    item.save()
    messages.success(request, 'Producto agregado al carrito con éxito.')
    return redirect('ver_carrito')

@login_required
def validar_pedido(request):
    # Obtiene o crea un carrito para el usuario actual
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        # Crea un pedido para cada ítem en el carrito
        for item in carrito.items.all():
            Pedido.objects.create(usuario=request.user, producto=item.producto, cantidad=item.cantidad)
        # Vacía el carrito después de realizar el pedido
        carrito.items.all().delete()
        messages.success(request, 'Pedido realizado con éxito.')
        return redirect('ver_pedidos')
    return redirect('carrito')

@login_required
def ver_pedidos(request):
    # Obtiene todos los pedidos del usuario actual, ordenados por fecha de pedido descendente
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    # Renderiza la plantilla 'ver_pedidos.html' con los pedidos
    return render(request, 'cuentas/ver_pedidos.html', {'pedidos': pedidos})

@login_required
def actualizar_carrito(request, item_id):
    # Obtiene el ítem de producto correspondiente al ID
    item = get_object_or_404(ProductoItem, id=item_id)
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de ítem de producto con los datos enviados
        form = ProductoItemForm(request.POST, instance=item)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en el ítem
            form.save()
            messages.success(request, 'Cantidad actualizada con éxito.')
            return redirect('ver_carrito')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario con los datos del ítem
        form = ProductoItemForm(instance=item)
    # Renderiza la plantilla 'actualizar_carrito.html' con el formulario de ítem de producto
    return render(request, 'cuentas/actualizar_carrito.html', {'form': form})

@login_required
def eliminar_del_carrito(request, item_id):
    # Obtiene el ítem de producto correspondiente al ID
    item = get_object_or_404(ProductoItem, id=item_id)
    # Elimina el ítem del carrito
    item.delete()
    messages.success(request, 'Producto eliminado del carrito con éxito.')
    return redirect('ver_carrito')

@login_required
def crear_producto(request):
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de producto con los datos enviados
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Si el formulario es válido, guarda el nuevo producto
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('tienda')
        else:
            messages.error(request, 'Error al crear el producto. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario vacío
        form = ProductoForm()
    # Renderiza la plantilla 'crear_producto.html' con el formulario de producto
    return render(request, 'cuentas/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    # Obtiene el producto correspondiente al ID
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        # Si el método de la solicitud es POST, crea un formulario de producto con los datos enviados
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            # Si el formulario es válido, guarda los cambios en el producto
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('tienda')
        else:
            messages.error(request, 'Error al actualizar el producto. Por favor, corrige los errores.')
    else:
        # Si el método de la solicitud no es POST, muestra un formulario con los datos del producto
        form = ProductoForm(instance=producto)
    # Renderiza la plantilla 'editar_producto.html' con el formulario de producto
    return render(request, 'cuentas/editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    # Obtiene el producto correspondiente al ID
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        # Si el método de la solicitud es POST, elimina el producto
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect('tienda')
    # Renderiza la plantilla 'confirmar_eliminar.html' para confirmar la eliminación
    return render(request, 'cuentas/confirmar_eliminar.html', {'producto': producto})
