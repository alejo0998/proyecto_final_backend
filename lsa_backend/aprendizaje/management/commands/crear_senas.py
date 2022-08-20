from random import gauss
from django.core.management.base import BaseCommand
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        gauth.Authorize()
        gdrive = GoogleDrive(gauth)
        archivos = gdrive.ListFile().GetList()
        cantidad_archivos = 0
        with open('/home/aprendizaje_url.csv', 'w', newline='') as csvfile:
            fieldnames = ['Categoria', 'Nombre', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for archivo in archivos:
                nombre = archivo['title'].split('-')
                if archivo['title'].endswith('.mp4') and len(nombre)>1:
                    writer.writerow({
                        'Categoria': nombre[0],
                        'Nombre': nombre[1].split('.')[0],
                        'URL': archivo['embedLink']
                    })
                    print('Nombre {}'.format(archivo['title']))
                    print('Link archivo {}'.format(archivo['embedLink']))
                    cantidad_archivos += 1

            print(cantidad_archivos)