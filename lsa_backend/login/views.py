import re
from .models import Usuario
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db import transaction
# Create your views here.

@transaction.atomic
@api_view(['POST'])
def login(request):
    post = request.POST
    email = post.get('email')
    token = post.get('token')
    if email and token:
        if not(es_correo_valido(email)):
            return Response('Formato invalido de email', 200)
        username = email.split('@')[0]
        usuario, created = Usuario.objects.get_or_create(email=email, username=username)
        try:
            if created:
                nombre = post.get('nombre')
                apellido = post.get('apellido')
                usuario.email = email
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.save()
                token = Token.objects.create(user = usuario, key = token)
                respuesta  = {
                    'usuario': username,
                    'creado': True,
                    'token': token.key
                }
                return Response(respuesta, 201)
        except Exception:
            return Response('Error TOKEN REPETIDO', 400)
        if not(created):
            token_usuario = Token.objects.filter(user = usuario)
            if token_usuario:
                token_usuario[0].delete()
            token = Token.objects.create(user = usuario, key = token)
            respuesta  = {
                    'usuario': username,
                    'creado': False,
                    'token': token.key
                }
            return Response(respuesta, 200)
    return Response('No envio email o token de google', 400)

def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None