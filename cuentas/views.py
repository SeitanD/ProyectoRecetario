from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from .models import Receta, Comentario, Profile, Valoracion, MensajeContacto, Categoria, Carrito, CarritoItem, Producto
from .forms import RecetaForm, ComentarioForm, UserRegistroForm, UserUpdateForm, ContactForm, ValoracionForm, CategoriaForm, CarritoItemForm, ProductoForm
from django.db import models
from django.views.decorators.csrf import csrf_exempt

# Vista para la página principal
def index(request):
    return render(request, 'cuentas/index.html')

# Vista para la página de aperitivos
def aperitivos(request):
    return render(request, 'cuentas/aperitivos.html')

# Vista para la página de comida
def comida(request):
    return render(request, 'cuentas/comida.html')

# Vista para la página de batidos
def batidos(request):
    return render(request, 'cuentas/batidos.html')

# Vista para la página de inicio de sesión
def login_view(request):
    return render(request, 'cuentas/login.html')

# Vista para el registro de nuevos usuarios
def registro(request):
    if request.method == 'POST':
        form = UserRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')
            return redirect('index')
        else:
            messages.error(request, 'Error al registrarse. Por favor, corrige los errores.')
    else:
        form = UserRegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})

def blog(request):
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        recetas = Receta.objects.filter(categoria_id=categoria_id)
    else:
        recetas = Receta.objects.all()
    categorias = Categoria.objects.all()
    comentario_form = ComentarioForm()
    
    context = {
        'recetas': recetas,
        'categorias': categorias,
        'comentario_form': comentario_form
    }
    
    return render(request, 'cuentas/blog.html', context)

# Vista para publicar recetas (requiere autenticación)
@login_required
def publicar_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.autor = request.user
            receta.save()
            messages.success(request, '¡Receta creada con éxito!')
            return redirect('blog')
        else:
            messages.error(request, 'Error al crear la receta. Por favor, corrige los errores.')
    else:
        form = RecetaForm()
    return render(request, 'cuentas/publicar_receta.html', {'form': form})

# Vista para agregar comentario (requiere autenticación)
@login_required
def add_comment(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.receta = receta
            comentario.autor = request.user
            comentario.save()
            messages.success(request, '¡Comentario agregado con éxito!')
        else:
            messages.error(request, 'Error al agregar el comentario. Por favor, corrige los errores.')
    return redirect('blog')

@login_required
def add_rating(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == 'POST':
        form = ValoracionForm(request.POST)
        if form.is_valid():
            puntuacion = form.cleaned_data['puntuacion']
            valoracion, created = Valoracion.objects.update_or_create(
                receta=receta,
                usuario=request.user,
                defaults={'puntuacion': puntuacion},
            )
            nueva_valoracion = receta.valoraciones.aggregate(models.Avg('puntuacion'))['puntuacion__avg']
            total_valoraciones = receta.valoraciones.count()
            receta.valoracion = nueva_valoracion
            receta.total_valoraciones = total_valoraciones
            receta.save()
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
    receta = get_object_or_404(Receta, id=receta_id)
    valoraciones = Valoracion.objects.filter(receta=receta)
    return render(request, 'cuentas/listar_valoraciones.html', {'receta': receta, 'valoraciones': valoraciones})

# Vista para eliminar una valoración
@login_required
def eliminar_valoracion(request, valoracion_id):
    valoracion = get_object_or_404(Valoracion, id=valoracion_id)
    if valoracion.usuario == request.user:
        valoracion.delete()
        messages.success(request, 'Valoración eliminada con éxito.')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta valoración.')
    return redirect('blog')

# Vista para eliminar una receta
@login_required
def eliminar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == "POST" and receta.autor == request.user:
        receta.delete()
        messages.success(request, 'Receta eliminada con éxito.')
    return redirect('blog')

# Vista para eliminar un comentario
@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == "POST" and comentario.autor == request.user:
        comentario.delete()
        messages.success(request, 'Comentario eliminado con éxito.')
    return redirect('blog')

# Vista para agregar una receta a los favoritos
@login_required
def add_to_favorites(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    profile = request.user.profile
    if receta not in profile.favoritos.all():
        profile.favoritos.add(receta)
        messages.success(request, '¡Receta añadida a tus favoritos!')
    else:
        messages.info(request, 'Esta receta ya está en tus favoritos.')
    return redirect('blog')

# Vista para eliminar una receta de los favoritos
@login_required
def eliminar_favorito(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    request.user.profile.favoritos.remove(receta)
    messages.success(request, 'Receta eliminada de tus favoritos.')
    return redirect('perfil')

# Vista para mostrar el perfil del usuario
@login_required
def perfil(request):
    profile = request.user.profile
    recetas_favoritas = profile.favoritos.all()
    return render(request, 'cuentas/perfil.html', {'user': request.user, 'recetas_favoritas': recetas_favoritas})

# Vista para editar una receta
@login_required
def editar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if receta.autor != request.user:
        return redirect('blog')
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receta editada con éxito.')
            return redirect('blog')
        else:
            messages.error(request, 'Error al editar la receta. Por favor, corrige los errores.')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'cuentas/editar_receta.html', {'form': form})

# Vista para editar un comentario
@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.autor != request.user:
        return redirect('blog')
    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comentario editado con éxito.')
            return redirect('blog')
        else:
            messages.error(request, 'Error al editar el comentario. Por favor, corrige los errores.')
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'cuentas/editar_comentario.html', {'form': form})

# Vista para actualizar el perfil del usuario
@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, corrige los errores.')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'cuentas/actualizar_perfil.html', {'form': form})

# Vista para eliminar la cuenta del usuario
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada con éxito.')
        return redirect('index')
    return render(request, 'cuentas/eliminar_cuenta.html')

# Vista para cerrar sesión
def custom_logout_view(request):
    logout(request)
    return redirect('login')

# Vista para manejar mensajes de contacto
@csrf_exempt
def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'error', 'errors': form.errors})
    else:
        form = ContactForm()
    return render(request, 'cuentas/contacto.html', {'form': form})

# Vista para listar mensajes de contacto
@login_required
def listar_mensajes_contacto(request):
    mensajes = MensajeContacto.objects.all()
    return render(request, 'cuentas/listar_mensajes_contacto.html', {'mensajes': mensajes})

# Vista para eliminar mensaje de contacto
@login_required
def eliminar_mensaje_contacto(request, mensaje_id):
    mensaje = get_object_or_404(MensajeContacto, id=mensaje_id)
    if request.method == "POST":
        mensaje.delete()
        messages.success(request, 'Mensaje de contacto eliminado con éxito.')
    return redirect('listar_mensajes_contacto')

@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'cuentas/listar_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada con éxito.')
            return redirect('listar_categorias')
        else:
            messages.error(request, 'Error al crear la categoría. Por favor, corrige los errores.')
    else:
        form = CategoriaForm()
    return render(request, 'cuentas/crear_categoria.html', {'form': form})

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría actualizada exitosamente!')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'cuentas/editar_categoria.html', {'form': form})

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    messages.success(request, '¡Categoría eliminada exitosamente!')
    return redirect('listar_categorias')

@login_required
def tienda(request):
    productos = Producto.objects.all()
    return render(request, 'cuentas/tienda.html', {'productos': productos})

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'cuentas/ver_carrito.html', {'carrito': carrito})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        item.cantidad += 1
        item.save()
    messages.success(request, 'Producto agregado al carrito con éxito.')
    return redirect('ver_carrito')

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if request.method == 'POST':
        form = CarritoItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cantidad actualizada con éxito.')
            return redirect('ver_carrito')
    else:
        form = CarritoItemForm(instance=item)
    return render(request, 'cuentas/actualizar_carrito.html', {'form': form})

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito con éxito.')
    return redirect('ver_carrito')

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('tienda')
        else:
            messages.error(request, 'Error al crear el producto. Por favor, corrige los errores.')
    else:
        form = ProductoForm()
    return render(request, 'cuentas/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito.')
            return redirect('tienda')
        else:
            messages.error(request, 'Error al actualizar el producto. Por favor, corrige los errores.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'cuentas/editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado con éxito.')
        return redirect('tienda')
    return render(request, 'cuentas/confirmar_eliminar.html', {'producto': producto})
