from rest_framework import serializers
from aprendizaje.models import Sena, UsuarioSena

class SenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sena
        fields = ['id', 'nombre', 'url', 'categoria',]

class UsuarioSenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSena
        fields = ['usuario', 'sena_realizada', 'fecha',]