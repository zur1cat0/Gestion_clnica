from unittest.mock import MagicMock, patch

from django.core.management.base import CommandError
from django.test import SimpleTestCase
from psycopg2 import OperationalError, sql

from gestion_clinica.database import ensure_postgresql_database
from login.management.commands.runserver import Command as RunserverCommand


class EnsurePostgreSQLDatabaseTests(SimpleTestCase):
    def setUp(self):
        self.database_settings = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'clinica_db',
            'USER': 'postgres',
            'PASSWORD': 'local-password',
            'HOST': 'localhost',
            'PORT': '5432',
        }

    @patch('gestion_clinica.database.psycopg2.connect')
    def test_creates_missing_database(self, connect):
        connection = MagicMock()
        cursor = MagicMock()
        cursor.fetchone.return_value = None
        connection.cursor.return_value.__enter__.return_value = cursor
        connect.return_value = connection

        created = ensure_postgresql_database(self.database_settings)

        self.assertTrue(created)
        self.assertTrue(connection.autocommit)
        self.assertEqual(cursor.execute.call_args_list[0].args, (
            'SELECT 1 FROM pg_database WHERE datname = %s',
            ('clinica_db',),
        ))
        self.assertEqual(
            cursor.execute.call_args_list[1].args[0],
            sql.SQL('CREATE DATABASE {}').format(sql.Identifier('clinica_db')),
        )
        connection.close.assert_called_once()

    @patch('gestion_clinica.database.psycopg2.connect')
    def test_leaves_existing_database_untouched(self, connect):
        connection = MagicMock()
        cursor = MagicMock()
        cursor.fetchone.return_value = (1,)
        connection.cursor.return_value.__enter__.return_value = cursor
        connect.return_value = connection

        created = ensure_postgresql_database(self.database_settings)

        self.assertFalse(created)
        cursor.execute.assert_called_once()
        connection.close.assert_called_once()

    @patch('gestion_clinica.database.psycopg2.connect')
    def test_does_not_connect_for_sqlite(self, connect):
        database_settings = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }

        created = ensure_postgresql_database(database_settings)

        self.assertFalse(created)
        connect.assert_not_called()

    @patch('gestion_clinica.database.psycopg2.connect')
    def test_reports_database_connection_errors(self, connect):
        connect.side_effect = OperationalError('connection failed')

        with self.assertRaises(CommandError):
            ensure_postgresql_database(self.database_settings)

    def test_rejects_the_maintenance_database_as_target(self):
        self.database_settings['NAME'] = 'postgres'

        with self.assertRaises(CommandError):
            ensure_postgresql_database(self.database_settings)

    @patch('login.management.commands.runserver.settings')
    @patch('login.management.commands.runserver.call_command')
    @patch('django.contrib.staticfiles.management.commands.runserver.Command.run')
    def test_runserver_applies_migrations_before_starting(
        self,
        run_staticfiles_server,
        call_command,
        command_settings,
    ):
        command_settings.DATABASES = {
            'default': {'ENGINE': 'django.db.backends.postgresql'},
        }
        options = {'verbosity': 1, 'use_reloader': False}

        RunserverCommand().run(**options)

        call_command.assert_called_once_with(
            'migrate',
            interactive=False,
            verbosity=1,
        )
        run_staticfiles_server.assert_called_once_with(**options)
