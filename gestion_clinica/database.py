import psycopg2
from django.core.management.base import CommandError
from psycopg2 import sql


POSTGRESQL_ENGINE = 'django.db.backends.postgresql'


def ensure_postgresql_database(database_settings, maintenance_database='postgres'):
    if database_settings['ENGINE'] != POSTGRESQL_ENGINE:
        return False

    database_name = database_settings.get('NAME')
    if not database_name:
        raise CommandError('DB_NAME must be set to create the PostgreSQL database.')
    if database_name == maintenance_database:
        raise CommandError('DB_NAME cannot be the PostgreSQL maintenance database.')

    connection_params = dict(database_settings.get('OPTIONS', {}))
    connection_params.update({
        'dbname': maintenance_database,
        'user': database_settings.get('USER'),
        'password': database_settings.get('PASSWORD'),
        'host': database_settings.get('HOST'),
        'port': database_settings.get('PORT'),
    })
    connection_params.setdefault('connect_timeout', 5)

    try:
        connection = psycopg2.connect(**connection_params)
        try:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT 1 FROM pg_database WHERE datname = %s',
                    (database_name,),
                )
                if cursor.fetchone():
                    return False

                try:
                    cursor.execute(
                        sql.SQL('CREATE DATABASE {}').format(
                            sql.Identifier(database_name)
                        )
                    )
                except psycopg2.errors.DuplicateDatabase:
                    return False
                return True
        finally:
            connection.close()
    except psycopg2.Error as exc:
        raise CommandError(
            f"Could not create or verify PostgreSQL database '{database_name}'. "
            'Check that PostgreSQL is running, the .env credentials are correct, '
            f'and the configured user can create databases. Details: {exc}'
        ) from exc
