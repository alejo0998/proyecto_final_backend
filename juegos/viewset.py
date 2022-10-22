import gc
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db import transaction
from aprendizaje.models import Sena, UsuarioSena, VideoSena
from aprendizaje.viewset import obtener_categoria
from rest_framework.response import Response
import random
from juegos.serializers import JuegoSerializer, SignarSerializer

def senas_vistas(lista_senas, categoria):
    senas_categoria = Sena.objects.filter(categoria=categoria)
    for sena in senas_categoria:
        if not(sena in lista_senas):
            return None
    return categoria

class CategoriasDisponibles(viewsets.ModelViewSet):
    queryset = VideoSena.objects.all()
    serializer_class = SignarSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    @api_view(['GET'])
    def get_categorias_disponibles(request):
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
        response = list()
        for cat in CATEGORIAS:
            lista_id = UsuarioSena.objects.filter(usuario=request.user, sena_realizada__categoria=cat[0]).values_list('sena_realizada')
            lista_sena = []
            for id in lista_id:
                lista_sena.append(Sena.objects.get(id=id[0]))
            categoria = senas_vistas(lista_sena, cat[0])
            if categoria:
                respuesta = {
                    'id': cat[0],
                    'name': cat[1],
                    'enabled': True
                }
                response.append(respuesta)
            else:
                respuesta = {
                    'id': cat[0],
                    'name': cat[1],
                    'enabled': False
                }
                response.append(respuesta)

        return Response(response, 200)

         

class JuegoViewset(viewsets.ModelViewSet):
    queryset = Sena.objects.all()
    serializer_class = JuegoSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    @api_view(['GET'])
    def get_juegos(request):
        categoria = request.GET.get('categoryName')
        posibles_juegos = ['escribi', 'adivina']
        response = []
        if request._auth and categoria:
            int_categoria = obtener_categoria(categoria)
            senas = []
            posibles_senas = list(Sena.objects.filter(categoria=int_categoria))
            for int in range(10):
                sena = random.choice(posibles_senas)
                posibles_senas.remove(sena)
                senas.append(sena)
            for sena in senas:
                sena_response = {
                                'id': sena.id,
                                'name': sena.nombre,
                                'urlVideo': sena.url
                }
                tipo_juego = random.choice(posibles_juegos)
                if tipo_juego == 'adivina':
                    senas_opciones = list(Sena.objects.filter(categoria=int_categoria))
                    senas_options = []
                    for int in range(4):
                        sena_random = random.choice(senas_opciones)
                        senas_opciones.remove(sena_random)
                        senas_options.append(sena_random)
                    if not(sena in senas_options):
                        senas_options.pop(0)
                        senas_options.insert(random.randint(0,3),sena)
                    opcion_sena = []
                    for opcion in senas_options:
                        op = {
                            'text': opcion.nombre,
                            'correct': opcion.nombre==sena.nombre
                        }
                        opcion_sena.append(op)
                    respuesta = {
                            'name': 'Adiviná la seña',
                            'type': 'GUESS_THE_SIGN',
                            'sign':sena_response,
                            'options': opcion_sena                        
                    }
                elif tipo_juego == 'escribi':
                    respuesta = {
                            'name': 'Escribi la seña',
                            'type': 'WRITE_THE_SIGN',
                            'sign':sena_response,
                            'options':[
                                {
                                    'text':sena.nombre,
                                    'correct':True
                                }
                            ]
                    }
                response.append(respuesta)
            return Response(response, 201)
        return Response('No envio token de inicio de sesion o la categoria', 400)

    @transaction.atomic
    @api_view(['GET'])
    def get_juegos_v2(request):
        categoria = request.GET.get('categoryName')
        posibles_juegos = ['escribi', 'adivina']
        response = []
        if request._auth:
            int_categoria = obtener_categoria(categoria)
            senas = []
            posibles_senas_signa = list()
            posibles_senas = list()
            if int_categoria != None:
                senas_categoria = list(Sena.objects.filter(categoria=int_categoria))
                for posible in senas_categoria:
                    if posible.permite_signa:
                        posibles_senas_signa.append(posible)
                    else:
                        posibles_senas.append(posible)
            else:
                lista_id = UsuarioSena.objects.filter(usuario=request.user).values_list('sena_realizada')
                for id in lista_id:
                    sena = Sena.objects.get(id=id[0])
                    if not(sena in posibles_senas):
                        if sena.permite_signa:
                            posibles_senas_signa.append(sena)
                        else:
                            posibles_senas.append(sena)
            cantidad_senas = 2 if len(posibles_senas_signa)>=2 else len(posibles_senas_signa)
            for i in range(10-cantidad_senas):
                sena = random.choice(posibles_senas)
                posibles_senas.remove(sena)
                senas.append(sena)
            for i in range(cantidad_senas):
                sena = random.choice(posibles_senas_signa)
                posibles_senas_signa.remove(sena)
                senas.append(sena)
            random.shuffle(senas)
            for sena in senas:
                sena_response = {
                                'id': sena.id,
                                'name': sena.nombre,
                                'urlVideo': sena.url
                }
                if sena.permite_signa:
                    respuesta = {
                            'name': 'Signá la palabra',
                            'description':'Juego de signa la palabra',
                            'type': 'SIGN_THE_WORD',
                            'position': sena.posicion_array_ia,
                            'category': sena.categoria,
                            'sign':sena_response,
                            'options':[
                                {
                                    'text':sena.nombre,
                                    'correct':True
                                }
                            ]
                    }
                else:
                    tipo_juego = random.choice(posibles_juegos)
                    if tipo_juego == 'adivina':
                        senas_opciones = list(Sena.objects.filter(categoria=sena.categoria))
                        senas_options = []
                        for int in range(4):
                            sena_random = random.choice(senas_opciones)
                            senas_opciones.remove(sena_random)
                            senas_options.append(sena_random)
                        if not(sena in senas_options):
                            senas_options.pop(0)
                            senas_options.insert(random.randint(0,3),sena)
                        opcion_sena = []
                        for opcion in senas_options:
                            op = {
                                'text': opcion.nombre,
                                'correct': opcion.nombre==sena.nombre
                            }
                            opcion_sena.append(op)
                        respuesta = {
                                'name': 'Adiviná la seña',
                                'type': 'GUESS_THE_SIGN',
                                'sign':sena_response,
                                'options': opcion_sena                        
                        }
                    elif tipo_juego == 'escribi':
                        respuesta = {
                                'name': 'Escribi la seña',
                                'type': 'WRITE_THE_SIGN',
                                'sign':sena_response,
                                'options':[
                                    {
                                        'text':sena.nombre,
                                        'correct':True
                                    }
                                ]
                        }
                response.append(respuesta)
            return Response(response, 201)
        return Response('No envio token de inicio de sesion o la categoria', 400)
