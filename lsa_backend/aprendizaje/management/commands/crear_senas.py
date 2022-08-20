from django.core.management.base import BaseCommand

class Comando(BaseCommand):
    def handle(self, *args, **options):
        import pdb; pdb.set_trace()
        return super().handle(*args, **options)