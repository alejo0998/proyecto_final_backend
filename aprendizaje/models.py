from django.db import models
from django.utils.translation import gettext_lazy as _
from login.models import Usuario
from django.contrib import admin
# Create your models here.

class Sena(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=254)
    class Categoria(models.TextChoices):
        ABECEDARIO = '1', _('Abecedario')
        COLORES = '2', _('Colores')
        COMIDAS = '3', _('Comidas')
        GEOGRAFIA = '4', _('Geografia')
        MODALES = '5', _('Modales')
        NUMEROS = '6', _('Numeros')
        PERSONAS = '7', _('Personas')
        PREGUNTAS = '8', _('Preguntas')
        VERBOS = '9', _('Verbos')
        
    categoria = models.CharField(
        max_length=2,
        choices=Categoria.choices,
        default=Categoria.ABECEDARIO
        )
    
    def __str__(self):
        return self.nombre


class UsuarioSena(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sena_realizada = models.ForeignKey(Sena, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)

admin.site.register(Sena)
admin.site.register(UsuarioSena)