from django.urls import path, include
from rest_framework import routers
from .views import *

#api versioning
router = routers.DefaultRouter()
router.register(r'customUsers', CustomUserView, 'customUsers')
router.register(r'refugios', RefugioView, 'refugios')

urlpatterns = [
    path('', index, name='index'),
    path('api/v1/', include(router.urls)),
    path('registrar/usuario/', registrar_usuario, name='registrar_usuario'),

    path('detalles/usuario/<int:id_usuario>/', detalles_usuario, name='detalles_usuario'),
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('signout/', signout_view, name='signout'),
    path('modulo_usuarios', modulo_usuarios, name='modulo_usuarios'),
]