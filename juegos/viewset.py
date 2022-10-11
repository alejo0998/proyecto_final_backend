import gc
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db import transaction
from aprendizaje.models import Sena, VideoSena
from aprendizaje.viewset import obtener_categoria
from rest_framework.response import Response
import random
from juegos.serializers import JuegoSerializer, SignarSerializer

class SignarViewset(viewsets.ModelViewSet):
    queryset = VideoSena.objects.all()
    serializer_class = SignarSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    @api_view(['POST'])
    def recibir_video(request):
        id = request.POST.get('idSign')
        video = request.FILES.get('video')
        if request._auth and id:
            try:
                sena_tipo = Sena.objects.get(id=id)
                sena_response = {
                        'id': sena_tipo.id,
                        'name': sena_tipo.nombre,
                    }
                return Response(sena_response, 201)
            except Exception as e:
                return Response('Error {}'.format(e), 401)
        return Response('Falta enviar video o seña', 401)


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
