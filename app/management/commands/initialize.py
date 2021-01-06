from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Script para inicializar'

    def handle(self, *args, **options):
        try:
            pass
        except (Exception,):
            raise CommandError('Erro ao inicializar Models')
        self.stdout.write(self.style.SUCCESS('Successfully created'))
