from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group


# Create your models here.
class CustomUser(AbstractUser):
    TIPOS_USUARIO = [
        ('admin', 'Administrador'),
        ('director', 'Director'),
        ('adoptante', 'Adoptante'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='adoptante')

    def __str__(self):
        return f"{self.first_name} ({self.tipo})"


class Refugio(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    director = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refugios')

    def __str__(self):
        return f"{self.nombre} - Dirigido por {self.director.username}"

class Mascota(models.Model):
    ESTADO_CHOICES = (
        ('disponible', 'Disponible'),
        ('adoptado', 'Adoptado'),
    )

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10)
    tamaño = models.CharField(max_length=20)
    estado_salud = models.TextField()
    foto = models.ImageField(upload_to='mascotas/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    refugio = models.ForeignKey(Refugio, on_delete=models.CASCADE, related_name='mascotas')

    def __str__(self):
        return self.nombre + " - " + self.especie


class Adopcion(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    )
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    adoptante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adopciones')
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_adopcion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
