from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Script para deletar Template Base'

    def handle(self, *args, **options):
        try:
            User.objects.all().delete()
        except (Exception,):
            raise CommandError('Erro ao deletar Models')
        self.stdout.write(self.style.SUCCESS('Successfully deleted'))
