from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Run migrations and create a superuser if not exists.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking database connection...')
        try:
            connection = connections['default']
            connection.ensure_connection()
        except OperationalError as e:
            self.stderr.write(f'Database connection failed: {e}')
            return

        self.stdout.write('Running migrations...')
        from django.core.management import call_command
        call_command('migrate')

        self.stdout.write('Checking for existing superuser...')
        if not User.objects.filter(username='admin_user').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser('admin_user', 'admin@example.com', 'adminpass12345')
            self.stdout.write('Superuser created successfully.')
        else:
            self.stdout.write('Superuser already exists.')