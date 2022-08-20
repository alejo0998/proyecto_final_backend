from random import gauss
from django.core.management.base import BaseCommand
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class Command(BaseCommand):
    def handle(self, *args, **options):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        gauth.Authorize()
        gdrive = GoogleDrive(gauth)
        archivos = gdrive.ListFile().GetList()
        cantidad_archivos = 0
        for archivo in archivos:
            print('Nombre {}'.format(archivo['title']))
            print('Link archivo {}'.format(archivo['embedLink']))
            cantidad_archivos += 1

        print(cantidad_archivos)