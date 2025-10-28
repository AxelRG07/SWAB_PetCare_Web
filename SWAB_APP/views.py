from django.shortcuts import render
from rest_framework import viewsets
from .serializer import CustomUserSerializer
from .models import *

# Create your views here.
class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()