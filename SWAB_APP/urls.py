from django.urls import path, include
from rest_framework import routers
from .views import *

# api versioning
router = routers.DefaultRouter()
router.register(r'customUsers', CustomUserView, 'customUsers')
router.register(r'refugios', RefugioView, 'refugios')
router.register(r'mascotas', MascotaView, 'mascotas')

urlpatterns = [
    path('', index, name='index'),
    path('api/v1/', include(router.urls)),
    path('registrar/usuario/', registrar_usuario, name='registrar_usuario'),
    path('registrar/refugio/', registrar_refugio, name='registrar_refugio'),
    path('registrar/mascota/<int:id_refugio>', registrar_mascota, name='registrar_mascota'),
    path('filtrar_usuarios/', filtrar_usuarios, name='filtrar_usuarios'),
    path('filtrar_refugios/', filtrar_refugios, name='filtrar_refugios'),
    path('detalles/usuario/<int:id_usuario>/', detalles_usuario, name='detalles_usuario'),
    path('detalles/refugio/<int:id_refugio>/', detalles_refugio, name='detalles_refugio'),
    path('detalles/mascota/<int:id_mascota>/', detalles_mascota, name='detalles_mascota'),
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('signout/', signout_view, name='signout'),
    path('modulo/usuarios', modulo_usuarios, name='modulo_usuarios'),
    path('modulo/refugios', modulo_refugios, name='modulo_refugios'),

]
