from django.shortcuts import render
from rest_framework import viewsets
from .serializer import CustomUserSerializer
from .models import *

# Create your views here.
class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


def registrar_usuario(request):
    return render(request, 'registrar_usuario.html')