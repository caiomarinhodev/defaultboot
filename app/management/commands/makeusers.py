from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Script para gerar users'

    def handle(self, *args, **options):
        superuser_data = {
            'username': 'caio',
            'first_name': 'Caio',
            'email': 'caiomarinho8@gmail.com',
            'password': 'oficinag3'
        }
        try:
            User.objects.create_superuser(username=superuser_data['username'],
                                          email=superuser_data['email'],
                                          password=superuser_data['password'])

        except (Exception,):
            raise CommandError('Erro ao gerar usuario')
        self.stdout.write(self.style.SUCCESS('Successfully user created'))
