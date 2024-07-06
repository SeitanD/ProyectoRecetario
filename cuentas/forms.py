from django import forms
from .models import Receta, Comentario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'imagen']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

class UserRegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    email_confirm = forms.EmailField(required=True, label="Confirmar correo electrónico")

    class Meta:
        model = User
        fields = ["username", "email", "email_confirm", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email_confirm = cleaned_data.get("email_confirm")
        if email != email_confirm:
            self.add_error("email_confirm", "Los correos electrónicos no coinciden.")
        return cleaned_data
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user