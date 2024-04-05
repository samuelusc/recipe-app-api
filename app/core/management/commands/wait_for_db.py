"""
Django command to wait for the database to be available
"""
# import  necessary modules
import time
from psycopg2 import OperationalError as Psycopg20Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for database is available.
    This Command is useful in the situations
    when containerized environments where the
    web application might start before the database is ready.
    """

    def handle(self, *args, **options):
        """
        The main entry point for the command.
        It continuously checks if the database is available and waits
        for it if it's not yet ready.
        """

        # Notify the user that the command is waiting for the database
        self.stdout.write('Waiting for database...')
        # Flag to track if the database is up
        db_up = False

        # Continue checking the database status until it's up
        while db_up is False:
            # Check database connectivity; will throw an error if not available
            try:
                self.check(databases=['default'])
                db_up = True

            # If an error is raised, the database is not available
            # Notify the user and wait for 1 second before retrying
            except (Psycopg20Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # Notify the user the database is
        self.stdout.write(self.style.SUCCESS('Database available!'))
