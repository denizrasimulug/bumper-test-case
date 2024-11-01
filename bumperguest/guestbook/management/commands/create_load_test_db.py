import json
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connections

class Command(BaseCommand):
    help = 'Loads initial data into a custom SQLite database'

    def handle(self, *args, **kwargs):
        custom_db_path = os.path.join(os.getcwd(), 'custom_load_test_data.sqlite3')
        if os.path.exists(custom_db_path):
            os.remove(custom_db_path)  # Remove existing file if it exists

        # Set up the custom database settings
        custom_db_settings = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': custom_db_path,
        }

        # Temporarily set the DATABASES setting
        original_db_settings = settings.DATABASES
        settings.DATABASES['default'] = custom_db_settings

        try:
            # Create the new database and the associated tables
            call_command('migrate')

            # Load data from the JSON file
            call_command('loaddata', 'guestbook/tests/load_test_data.json')

            self.stdout.write(self.style.SUCCESS(f"Data has been successfully loaded into {custom_db_path}."))
        finally:
            # Restore the original database settings
            settings.DATABASES = original_db_settings
            connections.close_all()  # Close all connections to reset the database state
