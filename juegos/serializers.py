from rest_framework import serializers

from aprendizaje.models import Sena

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sena
        fields = ['id', 'nombre', 'url', 'categoria']