from django.conf import settings
from django.core.management.commands.migrate import Command as MigrateCommand

from gestion_clinica.database import ensure_postgresql_database


class Command(MigrateCommand):
    def handle(self, *args, **options):
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            ensure_postgresql_database(
                settings.DATABASES['default'],
                settings.DB_MAINTENANCE_DB,
            )
        return super().handle(*args, **options)
