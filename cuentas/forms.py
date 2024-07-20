from django import forms
from .models import Receta, Categoria, Comentario, MensajeContacto, ProductoItem, Producto, Valoracion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# Formulario para el modelo Receta
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'ingredientes', 'preparacion', 'imagen', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredientes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preparacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para el modelo Comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

# Formulario de registro de usuario, extiende UserCreationForm
class UserRegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    email_confirm = forms.EmailField(required=True, label="Confirmar correo electrónico")

    class Meta:
        model = User
        fields = ["username", "email", "email_confirm", "password1", "password2"]

    # Validación personalizada para asegurar que los correos electrónicos coinciden
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email_confirm = cleaned_data.get("email_confirm")
        if email != email_confirm:
            self.add_error("email_confirm", "Los correos electrónicos no coinciden.")
        return cleaned_data

# Formulario para actualizar los datos del usuario
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    # Validación personalizada para asegurar que las contraseñas coinciden
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    # Sobrescribir el método save para manejar la actualización de la contraseña
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

# Formulario para el modelo MensajeContacto
class ContactForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'telefono', 'asunto', 'mensaje']

# Formulario para el modelo Valoracion
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

# Formulario para el modelo Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

# Formulario para el modelo ProductoItem
class ProductoItemForm(forms.ModelForm):
    class Meta:
        model = ProductoItem
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para el modelo Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
