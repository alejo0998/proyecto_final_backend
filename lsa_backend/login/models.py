from pyexpat import model
from django.db import models

# Create your models here.

class Usuario(models):
    email = models.CharField(max_length=100, null=False, blank=False)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    foto = models.FilePathField()
