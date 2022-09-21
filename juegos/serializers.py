from rest_framework import serializers

from aprendizaje.models import Sena, VideoSena

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sena
        fields = ['id', 'nombre', 'url', 'categoria']


class SignarSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSena
        fields = '__all__'