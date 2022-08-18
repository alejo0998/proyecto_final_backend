from rest_framework import serializers
from aprendizaje.models import Sena, UsuarioSena

class SenaSerializer(serializers.ModelSerializer):
    realizado = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Sena
        fields = ['id', 'nombre', 'url', 'categoria', 'realizado']

    def get_realizado(self, obj):
        senas = UsuarioSena.objects.filter(sena_realizada = obj, usuario=self.context.get('user'))
        return senas.count() > 0

class UsuarioSenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSena
        fields = ['usuario', 'sena_realizada', 'fecha',]