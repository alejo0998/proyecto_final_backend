from crypt import methods
from rest_framework import viewsets
from aprendizaje.serializers import SenaSerializer, UsuarioSenaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import Sena, UsuarioSena
from rest_framework.response import Response
from rest_framework.request import Request

class SenaViewset(viewsets.ModelViewSet):
    queryset = Sena.objects.all()
    serializer_class = SenaSerializer
    permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    def get_senas_categoria(request): #Me devuelve todas las senas segun una categoria
        if request.GET.get('categoria'):
            queryset = Sena.objects.filter(categoria = request.GET.get('categoria'))
            serializer = SenaSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        return Response('No se envio la categoria')

class UsuarioSenaViewset(viewsets.ModelViewSet):
    queryset = UsuarioSena.objects.all()
    serializer_class = UsuarioSenaSerializer
    permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    def get_senas_usuario(request): #Me devuelve las senas que vio un usuario
        if request._auth:
            queryset = UsuarioSena.objects.filter(usuario=request._auth.user)
            serializer = UsuarioSenaSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, 200)
        return Response('No se envio el token', 401)

    @api_view(['POST'])
    def post_sena_usuario(request): #Actualiza una sena que vio un usuario
        id = request.POST.get('id_sena')
        if request._auth and id:
            try:
                sena_realizada = Sena.objects.get(id=id)
                UsuarioSena.objects.create(
                    usuario = request._auth.user,
                    sena_realizada = sena_realizada
                )
                return Response('Seña usuario creada', 201)
            except Exception:
                return Response('No existe el usuario o la seña',401)
        else:
            return Response('Faltan parametros',401)


