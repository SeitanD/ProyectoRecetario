from django import forms  # Importa el módulo de formularios de Django
from .models import Receta, Comentario, Valoracion  # Importa los modelos Receta, Comentario y Valoracion del archivo models.py
from django.contrib.auth.models import User  # Importa el modelo User del módulo de autenticación de Django
from django.contrib.auth.forms import UserCreationForm  # Importa el formulario de creación de usuarios
from django.core.exceptions import ValidationError  # Importa la excepción ValidationError para validaciones personalizadas

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'ingredientes', 'preparacion', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredientes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preparacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):  # Define un formulario basado en el modelo Comentario
    class Meta:
        model = Comentario  # Especifica que este formulario se basa en el modelo Comentario
        fields = ['texto']  # Incluye el campo 'texto' en el formulario

class UserRegistroForm(UserCreationForm):  # Define un formulario para registrar nuevos usuarios basado en UserCreationForm
    email = forms.EmailField(required=True, label="Correo electrónico")  # Añade un campo de correo electrónico requerido
    email_confirm = forms.EmailField(required=True, label="Confirmar correo electrónico")  # Añade un campo para confirmar el correo electrónico

    class Meta:
        model = User  # Especifica que este formulario se basa en el modelo User
        fields = ["username", "email", "email_confirm", "password1", "password2"]  # Incluye los campos necesarios en el formulario

    def clean(self):  # Método para limpiar y validar los datos del formulario
        cleaned_data = super().clean()  # Llama al método clean del formulario base
        email = cleaned_data.get("email")  # Obtiene el valor del campo email
        email_confirm = cleaned_data.get("email_confirm")  # Obtiene el valor del campo email_confirm
        if email != email_confirm:  # Comprueba si los correos electrónicos coinciden
            self.add_error("email_confirm", "Los correos electrónicos no coinciden.")  # Añade un error si no coinciden
        return cleaned_data  # Devuelve los datos limpiados

class UserUpdateForm(forms.ModelForm):  # Define un formulario para actualizar usuarios basado en ModelForm
    email = forms.EmailField()  # Añade un campo de correo electrónico
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Añade un campo de contraseña opcional
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)  # Añade un campo para confirmar la contraseña opcional

    class Meta:
        model = User  # Especifica que este formulario se basa en el modelo User
        fields = ['username', 'email', 'password', 'confirm_password']  # Incluye los campos necesarios en el formulario

    def clean(self):  # Método para limpiar y validar los datos del formulario
        cleaned_data = super().clean()  # Llama al método clean del formulario base
        password = cleaned_data.get('password')  # Obtiene el valor del campo password
        confirm_password = cleaned_data.get('confirm_password')  # Obtiene el valor del campo confirm_password

        if password and password != confirm_password:  # Comprueba si las contraseñas coinciden
            raise ValidationError("Las contraseñas no coinciden.")  # Lanza un error de validación si no coinciden
        
        return cleaned_data  # Devuelve los datos limpiados

    def save(self, commit=True):  # Método para guardar el formulario
        user = super().save(commit=False)  # Llama al método save del formulario base sin confirmar el guardado
        password = self.cleaned_data.get('password')  # Obtiene el valor del campo password
        if password:  # Si hay una contraseña
            user.set_password(password)  # Establece la contraseña del usuario
        if commit:  # Si commit es True
            user.save()  # Guarda el usuario en la base de datos
        return user  # Devuelve el usuario guardado

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntuacion']
        widgets = {
            'puntuacion': forms.RadioSelect(choices=[
                (1, '1 estrella'),
                (2, '2 estrellas'),
                (3, '3 estrellas'),
                (4, '4 estrellas'),
                (5, '5 estrellas'),
            ])
        }
