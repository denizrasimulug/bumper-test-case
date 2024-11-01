from django.test import TestCase, tag
from django.urls import reverse
from ..models import Guest, Entry

@tag("integration-test")
class GetUserDataTestCase(TestCase):
    def setUp(self):
        # Create sample users and entries for testing
        self.user1 = Guest.objects.create(name="User 1")
        self.user2 = Guest.objects.create(name="User 2")

        # Create entries for user1
        Entry.objects.create(subject="Subject 1", message="Message 1", guest=self.user1)
        Entry.objects.create(subject="Subject 2", message="Message 2", guest=self.user1)
        # Create entries for user2
        Entry.objects.create(subject="Subject 3", message="Message 3", guest=self.user2)
        Entry.objects.create(subject="Subject 4", message="Message 4", guest=self.user2)
        Entry.objects.create(subject="Subject 5", message="Message 5", guest=self.user2)

    def test_get_user_data_success(self):
        response = self.client.get(reverse("user-data-view"))
        self.assertEqual(response.status_code, 200)

        users = response.json()["users"]
        self.assertEqual(len(users), 2)  # Check that two users are returned
        self.assertEqual(users[0]["username"], self.user2.name)
        self.assertEqual(users[1]["username"], self.user1.name)

    def test_get_user_data_latest_entry(self):
        # Modify the latest entry for user1
        latest_entry = Entry.objects.create(
            subject="Latest Subject", message="Latest Message", guest=self.user1
        )

        response = self.client.get(reverse("user-data-view"))
        self.assertEqual(response.status_code, 200)

        users = response.json()["users"]
        self.assertEqual(
            users[0]["last_entry"], f"{latest_entry.subject} | {latest_entry.message}"
        )

    def test_get_user_data_no_entries(self):
        # Clear all entries
        Entry.objects.all().delete()

        response = self.client.get(reverse("user-data-view"))
        self.assertEqual(response.status_code, 200)

        users = response.json()["users"]
        self.assertEqual(
            len(users), 0
        )  # Check that no users are returned if no entries exist
