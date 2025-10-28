from idlelib.rpc import request_queue

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .serializer import CustomUserSerializer, RefugioSerializer
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate

# Create your views here.
class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class RefugioView(viewsets.ModelViewSet):
    serializer_class = RefugioSerializer
    queryset = Refugio.objects.all()

def registrar_usuario(request):
    return render(request, 'registrar_usuario.html')

def registrar_refugio(request):
    return render(request, 'registrar_refugio.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signin')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomLoginForm()
    return render(request, 'signin.html', {'form': form})


def signout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html', {
        'user': request.user
    })

def modulo_usuarios(request):
    return render(request, 'modulo_usuarios.html')

def detalles_usuario(request, id_usuario):
    if request.method == 'GET':
        usuario = get_object_or_404(CustomUser, id=id_usuario)

        return render(request, 'detalle_usuario.html', {
            'usuario': usuario,
        })