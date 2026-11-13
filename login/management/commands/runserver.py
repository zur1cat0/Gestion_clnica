from django.conf import settings
from django.core.management import call_command
from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

from gestion_clinica.database import POSTGRESQL_ENGINE


class Command(RunserverCommand):
    def run(self, **options):
        if settings.DATABASES['default']['ENGINE'] == POSTGRESQL_ENGINE:
            call_command(
                'migrate',
                interactive=False,
                verbosity=options.get('verbosity', 1),
            )
        return super().run(**options)
