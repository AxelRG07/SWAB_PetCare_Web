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
from django.db import transaction
from .decorators import grupo_requerido

class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class RefugioView(viewsets.ModelViewSet):
    serializer_class = RefugioSerializer
    queryset = Refugio.objects.all()


class MascotaView(viewsets.ModelViewSet):
    serializer_class = MascotaSerializer
    queryset = Mascota.objects.all()


@grupo_requerido('Administrador')
def registrar_usuario(request):
    if request.method == 'POST':
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 == pass2:
            try:
                # Usamos atomic para asegurar que se crea el usuario Y se asigna el grupo
                with transaction.atomic():
                    usuario = CustomUser.objects.create_user(
                        first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name'),
                        username=request.POST.get('username'),
                        email=request.POST.get('email'),
                        password=pass1,
                        tipo=''
                    )
                    
                    tipo_seleccionado = request.POST.get('tipo')
                    
                    if tipo_seleccionado == 'admin':
                        grupo = Group.objects.get(name='Administrador')
                    elif tipo_seleccionado == 'director':
                        grupo = Group.objects.get(name='Director')
                    else:
                        grupo = Group.objects.get(name='Adoptante')
                    
                    usuario.groups.add(grupo)
                    
                    return redirect('modulo_usuarios')
                
            except Group.DoesNotExist:
                return render(request, 'registrar_usuario.html', {'error': 'El rol seleccionado no existe en el sistema'})
            
            except IntegrityError:
                return render(request, 'registrar_usuario.html', {
                    'error': 'El nombre de usuario o correo ya existe.',
                    'old_data': request.POST 
                })
        else:
            return render(request, 'registrar_usuario.html', {
                'error': 'Las contraseñas no coinciden',
                'old_data': request.POST
            })

    return render(request, 'registrar_usuario.html')


@grupo_requerido('Administrador')
def registrar_refugio(request):
    if request.method == 'POST':
        form = RefugioForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('modulo_refugios')
        else:
            return render(request, 'registrar_refugio.html', {
                'form': form, 
                'error': 'Por favor corrige los errores señalados abajo.'
            })
    else:
        form = RefugioForm()

    return render(request, 'registrar_refugio.html', {
        'form': form,
    })


@grupo_requerido('Director')
def registrar_mascota(request, id_refugio):
    refugio = Refugio.objects.get_object_or_404(id=id_refugio)

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.refugio = refugio
            mascota.save()
            return redirect(f'/detalles/refugio/{id_refugio}/')
        else:
            return render(request, 'registrar_mascota.html', {
                'form': form,
                'refugio': refugio,
                'error': 'Datos incorrectos, revisa los campos.'
            })
    else:
        return render(request, 'registrar_mascota.html', {
            'form': MascotaForm(),
            'refugio': refugio,
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


@grupo_requerido('Administrador')
def modulo_usuarios(request):
    return render(request, 'modulo_usuarios.html', {'u': request.user})


@grupo_requerido('Administrador')
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
