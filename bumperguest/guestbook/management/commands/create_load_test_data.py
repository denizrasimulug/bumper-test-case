import json
import random
from django.core.management.base import BaseCommand
from guestbook.models import Guest, Entry  


def random_time():
    return f"2021-01-01T{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}Z"
class Command(BaseCommand):
    help = 'Creates initial data for the Guest and Entry models'
    USER_COUNT = 1000000
    ENTRY_PER_USER = 1000
    def handle(self, *args, **kwargs):
        # Sample data for guests
        guests = [
            {"model": "guestbook.guest", "pk": i + 1, "fields": {"name": f"Guest {i + 1}", "created_at": random_time()}}
            for i in range(self.USER_COUNT)  # Adjust the range as needed
        ]

        # Sample data for entries (5 entries per guest)
        entries = [
            {"model": "guestbook.entry", "pk": i + 1, "fields": {"subject": f"Subject {i % self.USER_COUNT}", "message": f"Message {i % self.USER_COUNT}", "guest": i // self.USER_COUNT + 1, "created_at": random_time()}}
            for i in range(self.ENTRY_PER_USER)  # Adjust the range as needed
        ]

        # Combine all data
        initial_data = guests + entries

        # Write to JSON file
        with open("guestbook/tests/load_test_data.json", "w") as f:
            json.dump(initial_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS("initial_data.json created successfully."))
