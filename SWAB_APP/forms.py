# api/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class RefugioForm(forms.ModelForm):
    class Meta:
        model = Refugio
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control'}),
            'logo': forms.FileInput(attrs={'class':'form-control'}),
            'director': forms.Select(attrs={'class':'form-select'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
