from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.db import transaction
from aprendizaje.models import Sena
from aprendizaje.viewset import obtener_categoria
from rest_framework.response import Response
import random
from juegos.serializers import JuegoSerializer

class JuegoViewset(viewsets.ModelViewSet):
    queryset = Sena.objects.all()
    serializer_class = JuegoSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    @api_view(['GET'])
    def get_juegos(request):
        categoria = request.GET.get('categoryName')
        posibles_juegos = ['escribi']
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


