from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Receta, Comentario, Profile
from .forms import RecetaForm, ComentarioForm, UserRegistroForm,UserUpdateForm
from django.contrib.auth import login, authenticate ,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


def index(request):
    return render(request, 'cuentas/index.html')

def aperitivos(request):
    return render(request, 'cuentas/aperitivos.html')

def comida(request):
    return render(request, 'cuentas/comida.html')

def batidos(request):
    return render(request, 'cuentas/batidos.html')

def contacto(request):
    return render(request, 'cuentas/contacto.html')

def login_view(request):
    return render(request, 'cuentas/login.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'cuentas/registro.html', {'form': form})

def blog(request):
    recetas = Receta.objects.all()
    form = RecetaForm()

    if request.method == "POST":
        if 'crear_receta' in request.POST:
            form = RecetaForm(request.POST, request.FILES)
            if form.is_valid():
                receta = form.save(commit=False)
                receta.autor = request.user
                receta.save()
                return redirect('blog')

        elif 'comentar' in request.POST:
            receta_id = request.POST.get('receta_id')
            receta = get_object_or_404(Receta, id=receta_id)
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.receta = receta
                comentario.autor = request.user
                comentario.save()
                return redirect('blog')

    context = {
        'recetas': recetas,
        'form': form,
        'comentario_form': ComentarioForm(),
    }
    return render(request, 'cuentas/blog.html', context)

@login_required
def eliminar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == "POST" and receta.autor == request.user:
        receta.delete()
        return redirect('blog')

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == "POST" and comentario.autor == request.user:
        comentario.delete()
        return redirect('blog')

@login_required
def add_to_favorites(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    request.user.profile.favoritos.add(receta)
    messages.success(request, '¡Receta añadida a tus favoritos!')
    return redirect('blog')

@login_required
def eliminar_favorito(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    request.user.profile.favoritos.remove(receta)
    return redirect('perfil')

def register(request):
    if request.method == 'POST':
        form = UserRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})

@login_required
def add_comment(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if request.method == "POST":
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.receta = receta
            comentario.autor = request.user
            comentario.save()
    return redirect('blog')

@login_required
def perfil(request):
    return render(request, 'cuentas/perfil.html', {'user': request.user})

@login_required
def editar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    if receta.autor != request.user:
        return redirect('blog')
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'cuentas/editar_receta.html', {'form': form})

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.autor != request.user:
        return redirect('blog')
    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'cuentas/editar_comentario.html', {'form': form})

@login_required
def eliminar_favorito(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    request.user.profile.favoritos.remove(receta)
    messages.success(request, 'Receta eliminada de tus favoritos.')
    return redirect('perfil')

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Corrige los errores a continuación.')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'cuentas/actualizar_perfil.html', {'form': form})

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada con éxito.')
        return redirect('index')
    return render(request, 'cuentas/eliminar_cuenta.html')