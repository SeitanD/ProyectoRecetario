from django.shortcuts import render, redirect, get_object_or_404  # Importa funciones para renderizar plantillas, redirigir y obtener objetos o devolver 404
from django.contrib.auth.decorators import login_required  # Importa el decorador para requerir inicio de sesión
from django.contrib import messages  # Importa el módulo de mensajes para mostrar mensajes de éxito o error
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash  # Importa funciones de autenticación y manejo de sesiones
from django.contrib.auth.models import User  # Importa el modelo User de Django
from .models import Receta, Comentario, Profile  # Importa los modelos definidos en models.py
from .forms import RecetaForm, ComentarioForm, UserRegistroForm, UserUpdateForm  # Importa los formularios definidos en forms.py

# Vista para la página principal
def index(request):
    return render(request, 'cuentas/index.html')  # Renderiza la plantilla index.html

# Vista para la página de aperitivos
def aperitivos(request):
    return render(request, 'cuentas/aperitivos.html')  # Renderiza la plantilla aperitivos.html

# Vista para la página de comida
def comida(request):
    return render(request, 'cuentas/comida.html')  # Renderiza la plantilla comida.html

# Vista para la página de batidos
def batidos(request):
    return render(request, 'cuentas/batidos.html')  # Renderiza la plantilla batidos.html

# Vista para la página de contacto
def contacto(request):
    return render(request, 'cuentas/contacto.html')  # Renderiza la plantilla contacto.html

# Vista para la página de inicio de sesión
def login_view(request):
    return render(request, 'cuentas/login.html')  # Renderiza la plantilla login.html

# Vista para el registro de nuevos usuarios
def registro(request):
    if request.method == 'POST':  # Comprueba si la solicitud es POST
        form = UserRegistroForm(request.POST)  # Crea una instancia del formulario con los datos POST
        if form.is_valid():  # Comprueba si el formulario es válido
            user = form.save()  # Guarda el nuevo usuario
            login(request, user)  # Inicia sesión con el nuevo usuario
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')  # Muestra un mensaje de éxito
            return redirect('index')  # Redirige a la página principal
    else:
        form = UserRegistroForm()  # Crea una instancia vacía del formulario
    return render(request, 'cuentas/registro.html', {'form': form})  # Renderiza la plantilla registro.html con el formulario

# Vista para el blog que muestra recetas y permite crear recetas y comentarios
@login_required  # Requiere que el usuario esté autenticado
def blog(request):
    recetas = Receta.objects.all()  # Obtiene todas las recetas
    form = RecetaForm()  # Crea una instancia vacía del formulario de recetas

    if request.method == "POST":  # Comprueba si la solicitud es POST
        if 'crear_receta' in request.POST:  # Comprueba si el formulario es para crear una receta
            form = RecetaForm(request.POST, request.FILES)  # Crea una instancia del formulario con los datos POST y archivos
            if form.is_valid():  # Comprueba si el formulario es válido
                receta = form.save(commit=False)  # Guarda la receta pero no la guarda en la base de datos aún
                receta.autor = request.user  # Establece el autor de la receta como el usuario actual
                receta.save()  # Guarda la receta en la base de datos
                messages.success(request, '¡Receta creada con éxito!')  # Muestra un mensaje de éxito
                return redirect('blog')  # Redirige a la página del blog
            else:
                messages.error(request, 'Error al crear la receta. Por favor, corrige los errores.')  # Muestra un mensaje de error

        elif 'comentar' in request.POST:  # Comprueba si el formulario es para agregar un comentario
            receta_id = request.POST.get('receta_id')  # Obtiene el ID de la receta del formulario
            receta = get_object_or_404(Receta, id=receta_id)  # Obtiene la receta o devuelve un error 404 si no existe
            comentario_form = ComentarioForm(request.POST)  # Crea una instancia del formulario de comentarios con los datos POST
            if comentario_form.is_valid():  # Comprueba si el formulario es válido
                comentario = comentario_form.save(commit=False)  # Guarda el comentario pero no lo guarda en la base de datos aún
                comentario.receta = receta  # Establece la receta del comentario
                comentario.autor = request.user  # Establece el autor del comentario como el usuario actual
                comentario.save()  # Guarda el comentario en la base de datos
                messages.success(request, '¡Comentario agregado con éxito!')  # Muestra un mensaje de éxito
                return redirect('blog')  # Redirige a la página del blog
            else:
                messages.error(request, 'Error al agregar el comentario. Por favor, corrige los errores.')  # Muestra un mensaje de error

    context = {
        'recetas': recetas,  # Pasa las recetas al contexto
        'form': form,  # Pasa el formulario de recetas al contexto
        'comentario_form': ComentarioForm(),  # Pasa un formulario de comentarios vacío al contexto
    }
    return render(request, 'cuentas/blog.html', context)  # Renderiza la plantilla blog.html con el contexto

# Vista para eliminar una receta
@login_required  # Requiere que el usuario esté autenticado
def eliminar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)  # Obtiene la receta o devuelve un error 404 si no existe
    if request.method == "POST" and receta.autor == request.user:  # Comprueba si la solicitud es POST y el usuario es el autor de la receta
        receta.delete()  # Elimina la receta
        messages.success(request, 'Receta eliminada con éxito.')  # Muestra un mensaje de éxito
        return redirect('blog')  # Redirige a la página del blog

# Vista para eliminar un comentario
@login_required  # Requiere que el usuario esté autenticado
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)  # Obtiene el comentario o devuelve un error 404 si no existe
    if request.method == "POST" and comentario.autor == request.user:  # Comprueba si la solicitud es POST y el usuario es el autor del comentario
        comentario.delete()  # Elimina el comentario
        messages.success(request, 'Comentario eliminado con éxito.')  # Muestra un mensaje de éxito
        return redirect('blog')  # Redirige a la página del blog

# Vista para agregar una receta a los favoritos
@login_required  # Requiere que el usuario esté autenticado
def add_to_favorites(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)  # Obtiene la receta o devuelve un error 404 si no existe
    profile = request.user.profile  # Obtiene el perfil del usuario actual
    if receta not in profile.favoritos.all():  # Comprueba si la receta no está en la lista de favoritos
        profile.favoritos.add(receta)  # Añade la receta a la lista de favoritos
        messages.success(request, '¡Receta añadida a tus favoritos!')  # Muestra un mensaje de éxito
    else:
        messages.info(request, 'Esta receta ya está en tus favoritos.')  # Muestra un mensaje informativo
    return redirect('blog')  # Redirige a la página del blog

# Vista para eliminar una receta de los favoritos
@login_required  # Requiere que el usuario esté autenticado
def eliminar_favorito(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)  # Obtiene la receta o devuelve un error 404 si no existe
    request.user.profile.favoritos.remove(receta)  # Elimina la receta de la lista de favoritos del usuario
    messages.success(request, 'Receta eliminada de tus favoritos.')  # Muestra un mensaje de éxito
    return redirect('perfil')  # Redirige a la página del perfil

# Vista para registrar un nuevo usuario (duplicada, se puede eliminar una)
def registro(request):
    if request.method == 'POST':  # Comprueba si la solicitud es POST
        form = UserRegistroForm(request.POST)  # Crea una instancia del formulario con los datos POST
        if form.is_valid():  # Comprueba si el formulario es válido
            user = form.save()  # Guarda el nuevo usuario
            login(request, user)  # Inicia sesión con el nuevo usuario
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')  # Muestra un mensaje de éxito
            return redirect('index')  # Redirige a la página principal
        else:
            messages.error(request, 'Error al registrarse. Por favor, corrige los errores.')  # Muestra un mensaje de error
    else:
        form = UserRegistroForm()  # Crea una instancia vacía del formulario
    return render(request, 'cuentas/registro.html', {'form': form})  # Renderiza la plantilla registro.html con el formulario

# Vista para agregar un comentario a una receta
@login_required  # Requiere que el usuario esté autenticado
def add_comment(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)  # Obtiene la receta o devuelve un error 404 si no existe
    if request.method == "POST":  # Comprueba si la solicitud es POST
        comentario_form = ComentarioForm(request.POST)  # Crea una instancia del formulario de comentarios con los datos POST
        if comentario_form.is_valid():  # Comprueba si el formulario es válido
            comentario = comentario_form.save(commit=False)  # Guarda el comentario pero no lo guarda en la base de datos aún
            comentario.receta = receta  # Establece la receta del comentario
            comentario.autor = request.user  # Establece el autor del comentario como el usuario actual
            comentario.save()  # Guarda el comentario en la base de datos
            messages.success(request, '¡Comentario agregado con éxito!')  # Muestra un mensaje de éxito
        else:
            messages.error(request, 'Error al agregar el comentario. Por favor, corrige los errores.')  # Muestra un mensaje de error
    return redirect('blog')  # Redirige a la página del blog

# Vista para mostrar el perfil del usuario
@login_required  # Requiere que el usuario esté autenticado
def perfil(request):
    profile = request.user.profile  # Obtiene el perfil del usuario actual
    recetas_favoritas = profile.favoritos.all()  # Obtiene todas las recetas favoritas del usuario
    return render(request, 'cuentas/perfil.html', {'user': request.user, 'recetas_favoritas': recetas_favoritas})  # Renderiza la plantilla perfil.html con el usuario y sus recetas favoritas

# Vista para editar una receta
@login_required  # Requiere que el usuario esté autenticado
def editar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)  # Obtiene la receta o devuelve un error 404 si no existe
    if receta.autor != request.user:  # Comprueba si el usuario actual no es el autor de la receta
        return redirect('blog')  # Redirige a la página del blog
    if request.method == "POST":  # Comprueba si la solicitud es POST
        form = RecetaForm(request.POST, request.FILES, instance=receta)  # Crea una instancia del formulario con los datos POST y archivos
        if form.is_valid():  # Comprueba si el formulario es válido
            form.save()  # Guarda los cambios en la receta
            messages.success(request, 'Receta editada con éxito.')  # Muestra un mensaje de éxito
            return redirect('blog')  # Redirige a la página del blog
        else:
            messages.error(request, 'Error al editar la receta. Por favor, corrige los errores.')  # Muestra un mensaje de error
    else:
        form = RecetaForm(instance=receta)  # Crea una instancia del formulario con la receta existente
    return render(request, 'cuentas/editar_receta.html', {'form': form})  # Renderiza la plantilla editar_receta.html con el formulario

# Vista para editar un comentario
@login_required  # Requiere que el usuario esté autenticado
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)  # Obtiene el comentario o devuelve un error 404 si no existe
    if comentario.autor != request.user:  # Comprueba si el usuario actual no es el autor del comentario
        return redirect('blog')  # Redirige a la página del blog
    if request.method == "POST":  # Comprueba si la solicitud es POST
        form = ComentarioForm(request.POST, instance=comentario)  # Crea una instancia del formulario con los datos POST
        if form.is_valid():  # Comprueba si el formulario es válido
            form.save()  # Guarda los cambios en el comentario
            messages.success(request, 'Comentario editado con éxito.')  # Muestra un mensaje de éxito
            return redirect('blog')  # Redirige a la página del blog
        else:
            messages.error(request, 'Error al editar el comentario. Por favor, corrige los errores.')  # Muestra un mensaje de error
    else:
        form = ComentarioForm(instance=comentario)  # Crea una instancia del formulario con el comentario existente
    return render(request, 'cuentas/editar_comentario.html', {'form': form})  # Renderiza la plantilla editar_comentario.html con el formulario

# Vista para actualizar el perfil del usuario
@login_required  # Requiere que el usuario esté autenticado
def actualizar_perfil(request):
    if request.method == 'POST':  # Comprueba si la solicitud es POST
        form = UserUpdateForm(request.POST, instance=request.user)  # Crea una instancia del formulario con los datos POST y el usuario actual
        if form.is_valid():  # Comprueba si el formulario es válido
            form.save()  # Guarda los cambios en el perfil del usuario
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')  # Muestra un mensaje de éxito
            return redirect('perfil')  # Redirige a la página del perfil
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, corrige los errores.')  # Muestra un mensaje de error
    else:
        form = UserUpdateForm(instance=request.user)  # Crea una instancia del formulario con el usuario actual
    return render(request, 'cuentas/actualizar_perfil.html', {'form': form})  # Renderiza la plantilla actualizar_perfil.html con el formulario

# Vista para eliminar la cuenta del usuario
@login_required  # Requiere que el usuario esté autenticado
def eliminar_cuenta(request):
    if request.method == 'POST':  # Comprueba si la solicitud es POST
        user = request.user  # Obtiene el usuario actual
        user.delete()  # Elimina el usuario
        messages.success(request, 'Tu cuenta ha sido eliminada con éxito.')  # Muestra un mensaje de éxito
        return redirect('index')  # Redirige a la página principal
    return render(request, 'cuentas/eliminar_cuenta.html')  # Renderiza la plantilla eliminar_cuenta.html

# Vista para cerrar sesión
def custom_logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de inicio de sesión
