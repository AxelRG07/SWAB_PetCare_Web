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

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'especie': forms.Select(attrs={'class':'form-select'}),
            'edad': forms.NumberInput(attrs={'class':'form-control'}),
            'sexo': forms.Select(attrs={'class':'form-select'}),
            'tamaño': forms.Select(attrs={'class':'form-select'}),
            'estado_salud': forms.Select(attrs={'class':'form-select'}),
            'foto': forms.FileInput(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-select'}),
            'refugio': forms.Select(attrs={'class':'form-select'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
