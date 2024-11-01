from django.test import TestCase, tag
from django.urls import reverse
from ..models import Guest, Entry
import time


@tag("load-test")
class GetUserDataLoadTestCase(TestCase):
    USER_COUNT = 10000
    ENTRY_PER_USER = 5

    def setUp(self):
        # Create a large number of users and entries for load testing
        guests = [Guest(name=f"User {i}") for i in range(self.USER_COUNT)]
        Guest.objects.bulk_create(guests)
        print("Created users")
        entries = []
        i = 0
        for guest in Guest.objects.all():
            i += 1
            for j in range(self.ENTRY_PER_USER):
                entries.append(
                    Entry(subject=f"Subject {j}", message=f"Message {j}", guest=guest)
                )
                if len(entries) == self.USER_COUNT*self.ENTRY_PER_USER/10:
                    Entry.objects.bulk_create(entries)
                    entries = []
                    print(f"Created entries for {i} users")

        if entries:
            Entry.objects.bulk_create(entries)

    def test_get_user_data_load(self):
        start_time = time.time()
        response = self.client.get(reverse("user-data-view"))
        end_time = time.time()

        self.assertEqual(response.status_code, 200)
        users = response.json()["users"]
        self.assertEqual(
            len(users), self.USER_COUNT
        )  # Check that 1000 users are returned
        self.assertTrue(
            end_time - start_time < 3
        )  # Ensure the request completes within 5 seconds
        print("Load Test completed in ", end_time - start_time)
