from django.test import TestCase, tag
from django.urls import reverse
from guestbook.models import Guest, Entry
from guestbook.utils.ulid import random_ulid
import time
from ulid import ULID


@tag("load-test")
class GetUserDataLoadTestCase(TestCase):
    def setUp(self):
        pass

    def _populate_db(self, user_count, entry_per_user):
        # Create a large number of users and entries for load testing
        guests = [Guest(name=f"User {i}") for i in range(user_count)]
        Guest.objects.bulk_create(guests)
        print("Created users")
        entries = []
        i = 0
        for guest in Guest.objects.all():
            i += 1
            for j in range(entry_per_user):
                entries.append(
                    Entry(
                        subject=f"Subject {j}",
                        message=f"Message {j}",
                        guest=guest,
                        ulid=f"{random_ulid()}",
                    )
                )
                if len(entries) > user_count * entry_per_user / 5:
                    Entry.objects.bulk_create(entries)
                    entries = []
                    print(f"Created entries for {i} users")

        if len(entries) > 0:
            Entry.objects.bulk_create(entries)

    def _run_load(self, user_count):
        start_time = time.time()
        print("Starting request")
        response = self.client.get(reverse("user-data-view"))
        end_time = time.time()
        print("Got response in ", end_time - start_time)

        self.assertEqual(response.status_code, 200)
        users = response.json()["users"]
        self.assertEqual(len(users), user_count)  # Check that 1000 users are returned
        self.assertTrue(
            end_time - start_time < 5
        )  # Ensure the request completes within 5 seconds
        print("Load Test completed in ", end_time - start_time)

    def test_high_guest_count(self):
        user_count = 10000
        entry_per_user = 5
        print(
            f"Running load test for {user_count} users and {entry_per_user} entries per user"
        )
        self._populate_db(user_count, entry_per_user)
        self._run_load(user_count)

    def test_high_entry_count(self):
        user_count = 100
        entry_per_user = 10000
        print(
            f"Running load test for {user_count} users and {entry_per_user} entries per user"
        )
        self._populate_db(user_count, entry_per_user)
        self._run_load(user_count)
