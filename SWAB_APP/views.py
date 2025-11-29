from idlelib.rpc import request_queue

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .serializer import CustomUserSerializer, RefugioSerializer, MascotaSerializer
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate, decorators


# Create your views here.
class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class RefugioView(viewsets.ModelViewSet):
    serializer_class = RefugioSerializer
    queryset = Refugio.objects.all()


class MascotaView(viewsets.ModelViewSet):
    serializer_class = MascotaSerializer
    queryset = Mascota.objects.all()


@login_required(login_url='signin')
def registrar_usuario(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = CustomUser.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1'],
                    tipo=request.POST['tipo']
                )
                usuario.save()
                return redirect('modulo_usuarios')
            except IntegrityError:
                return render(request, 'registrar_usuario.html', {
                    'error': 'error al registrar usuario',
                })
        return render(request, 'registrar_usuario.html', {
            'error': 'Las contraseñas no coinciden',
        })

    return render(request, 'registrar_usuario.html')


@login_required(login_url='signin')
def registrar_refugio(request):
    if request.method == 'GET':
        return render(request, 'registrar_refugio.html', {
            'form': RefugioForm(),
        })
    else:
        try:
            form = RefugioForm(request.POST, request.FILES)
            form.save()
            return redirect('modulo_refugios')
        except ValueError:
            return render(request, 'registrar_refugio.html', {
                'form': RefugioForm(),
                'error': 'Datos incorrectos',
            })


@login_required(login_url='signin')
def registrar_mascota(request, id_refugio):
    if request.method == 'GET':
        refugio = Refugio.objects.get(id=id_refugio)
        return render(request, 'registrar_mascota.html', {
            'form': MascotaForm(),
            'refugio': refugio,
        })
    else:
        try:
            form = MascotaForm(request.POST, request.FILES)
            form.refugio = Refugio.objects.get(id=id_refugio)
            form.save()
            return redirect(f'/detalles/refugio/{id_refugio}/')
        except ValueError:
            return render(request, 'registrar_mascota.html', {
                'form': MascotaForm(),
                'error': 'Datos incorrectos',
            })


def signup_view(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = CustomUser.objects.create_user(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                usuario.save()
                login(request, usuario)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'error': 'error al registrar usuario',
                })
        return render(request, 'signup.html', {
            'error': 'Las contraseñas no coinciden',
        })
    return render(request, 'signup.html')


def signin_view(request):
    if request.method == 'POST':
        user = authenticate(
            request=request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is None:
            return render(request, 'signin.html', {
                'error': 'usuario y/o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('index')
    else:
        form = CustomLoginForm()
    return render(request, 'signin.html', {'form': form})


@login_required(login_url='signin')
def signout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    return render(request, 'index.html', {
        'user': request.user
    })


@login_required(login_url='signin')
def modulo_usuarios(request):
    user = request.user
    if user.tipo == 'admin':
        return render(request, 'modulo_usuarios.html', {
            'u': request.user
        })

    return redirect('index')


@login_required(login_url='signin')
def detalles_usuario(request, id_usuario):
    if request.method == 'GET':
        usuario = get_object_or_404(CustomUser, id=id_usuario)

        return render(request, 'detalle_usuario.html', {
            'usuario': usuario,
        })


def modulo_refugios(request):
    refugios = Refugio.objects.all()
    return render(request, 'modulo_refugios.html', {
        'user': request.user,
        'refugios': refugios,
    })


def detalles_refugio(request, id_refugio):
    if request.method == 'GET':
        refugio = get_object_or_404(Refugio, id=id_refugio)
        mascotas = Mascota.objects.filter(refugio=refugio)
        form = RefugioForm(instance=refugio)
        return render(request, 'detalle_refugio.html', {
            'refugio': refugio,
            'usuario': request.user,
            'form': form,
            'mascotas': mascotas,
        })


def detalles_mascota(request, id_mascota):
    if request.method == 'GET':
        mascota = get_object_or_404(Mascota, id=id_mascota)
        form = MascotaForm(instance=mascota)
        return render(request, 'detalle_mascota.html', {
            'usuario': request.user,
            'form': form,
            'mascota': mascota,
        })


def filtrar_usuarios(request):
    tipo = request.GET.get('tipo')
    if not tipo:
        return JsonResponse({'error': 'No se proporcionó tipo'}, status=400)

    usuarios = CustomUser.objects.filter(tipo=tipo).values('id', 'first_name', 'last_name', 'email', 'tipo')
    return JsonResponse(list(usuarios), safe=False)


def filtrar_refugios(request):
    id_usuario = request.GET.get('id_usuario')
    if not id_usuario:
        return JsonResponse({'error': 'No se proporcionó usuario'}, status=400)

    try:
        refugio = Refugio.objects.get(director_id=id_usuario)
        data = {
            'id': refugio.id,
            'nombre': refugio.nombre,
            'direccion': refugio.direccion,
        }
        return JsonResponse(data, safe=False)

    except Refugio.DoesNotExist:
        return JsonResponse({'mensaje': 'No se encontró refugio asociado'}, status=404)
