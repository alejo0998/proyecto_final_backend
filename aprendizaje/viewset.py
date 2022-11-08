from crypt import methods
from rest_framework import viewsets
from aprendizaje.serializers import SenaSerializer, UsuarioSenaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import Sena, UsuarioSena
from rest_framework.response import Response
import json


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def obtener_categoria(categoria):
    if categoria is None:
        return categoria
    CATEGORIAS= [
        ('1', 'Abecedario'),
        ('2', 'Colores'),
        ('3', 'Comidas'),
        ('4', 'Geografia'),
        ('5', 'Modales'),
        ('6', 'Numeros'),
        ('7', 'Personas'),
        ('8', 'Preguntas'),
        ('9', 'Verbos'),
    ]
    categoria = categoria.upper()
    for cat in CATEGORIAS:
        if normalize(categoria) == normalize(cat[1].upper()):
            return cat[0]

class SenaViewset(viewsets.ModelViewSet):
    queryset = Sena.objects.all()
    serializer_class = SenaSerializer
    permission_classes = [IsAuthenticated]

    @api_view(['GET'])
    def get_senas_categoria(request): #Me devuelve todas las senas segun una categoria
        if request.GET.get('category'):
            categoria = obtener_categoria(request.GET.get('category'))
            queryset = Sena.objects.filter(categoria=categoria).order_by('nombre')
            if categoria == '6':
                queryset = Sena.objects.filter(categoria=categoria).order_by('orden')

            serializer = SenaSerializer(queryset, many=True, context={'request': request,
                                                                      'user': request._auth.user})
            return Response(serializer.data)
        return Response('No se envio la categoria')

    @api_view(['GET'])
    def get_id_senas_categoria(request):
        json_data = json.loads(request.body)
        id = json_data.get('categoria')
        qs = Sena.objects.filter(categoria=id)
        for q in qs:
            UsuarioSena.objects.create(
                usuario = request.user,
                sena_realizada=q
            )
        return Response(qs.values_list('id'), 200)

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
        json_data = json.loads(request.body)
        id = json_data.get('idSign')
        if id is None:
            id = request.POST.get('idSign')
        if request._auth and id:
            try:
                sena_realizada = Sena.objects.get(id=id)
                
                sena, bool = UsuarioSena.objects.get_or_create(
                    usuario = request._auth.user,
                    sena_realizada = sena_realizada
                )
                if bool:
                    return Response('Seña usuario creada', 201)
                return Response('Seña usuario anteriormente creada', 201)
            except Exception:
                return Response('No existe el usuario o la seña',401)
        else:
            return Response('Faltan parametros',401)


