from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    foto_perfil = models.FileField(null=True, blank=True)

