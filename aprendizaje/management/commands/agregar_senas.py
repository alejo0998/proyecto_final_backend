from ast import operator
from django.core.management.base import BaseCommand
import csv
from aprendizaje.models import Sena

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('aprendizaje_url.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in sorted(reader, reverse=False, key='nombre'):
                categoria = row['Categoria']
                nombre = row['Nombre'].replace('_', ' ')
                url = row['URL']
                if len(categoria)<=2:
                    Sena.objects.create(
                        categoria = categoria,
                        nombre = nombre,
                        url = url
                    )
