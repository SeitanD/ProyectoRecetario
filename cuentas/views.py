from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .models import Receta, Comentario, Profile, Valoracion ,MensajeContacto
from .forms import RecetaForm, ComentarioForm, UserRegistroForm, UserUpdateForm,ContactForm, ValoracionForm


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
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')
            return redirect('index')
        else:
            messages.error(request, 'Error al registrarse. Por favor, corrige los errores.')
    else:
        form = UserRegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})

# Vista para mostrar el blog
def blog(request):
    recetas = Receta.objects.all()
    context = {
        'recetas': recetas,
        'comentario_form': ComentarioForm(),
        'valoracion_form': ValoracionForm(),
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

# Vista para agregar valoración (requiere autenticación)
@login_required
def add_rating(request, receta_id):
    if request.method == 'POST':
        puntuacion = int(request.POST.get('puntuacion'))
        receta = get_object_or_404(Receta, id=receta_id)

        # Crear o actualizar la valoración del usuario
        valoracion, created = Valoracion.objects.update_or_create(
            usuario=request.user, receta=receta,
            defaults={'puntuacion': puntuacion}
        )

        # Recalcular la valoración promedio de la receta
        all_ratings = Valoracion.objects.filter(receta=receta)
        total_rating = sum(r.puntuacion for r in all_ratings)
        average_rating = total_rating / all_ratings.count()

        receta.valoracion = average_rating
        receta.total_valoraciones = all_ratings.count()
        receta.save()

        return JsonResponse({'success': True, 'new_rating': average_rating, 'total_ratings': all_ratings.count()})
    return JsonResponse({'success': False}, status=400)

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