from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = '执行 makemigrations，migrate 和 runserver 命令'

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
        call_command('runserver')