from django.test import TestCase, Client, tag
from django.urls import reverse
from ..models import Guest, Entry
import json


@tag("integration-test")
class CreateEntryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("entry-view")  # Ensure the URL name matches your routing

    def test_create_entry_success(self):
        # Prepare data for the request
        data = {
            "name": "John Doe",
            "subject": "My First Entry",
            "message": "Hello, this is my first message!",
        }

        # Send a POST request to the create entry endpoint
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Assert the response data
        response_data = response.json()
        self.assertEqual(response_data["subject"], data["subject"])
        self.assertEqual(response_data["message"], data["message"])
        self.assertEqual(response_data["guest_name"], data["name"])

        # Assert the entry was created in the database
        entry = Entry.objects.get(id=response_data["id"])
        self.assertIsNotNone(entry)
        self.assertEqual(entry.subject, data["subject"])
        self.assertEqual(entry.message, data["message"])

        # Assert the guest was created
        guest = Guest.objects.get(name=data["name"])
        self.assertIsNotNone(guest)
        self.assertEqual(guest.name, data["name"])

    def test_create_entry_with_existing_user(self):
        # Create an existing user
        existing_guest = Guest.objects.create(name="Jane Doe")
        data = {
            "name": existing_guest.name,
            "subject": "Another Entry",
            "message": "This message is from an existing user.",
        }

        # Send a POST request
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 201)

        # Assert the response data
        response_data = response.json()
        self.assertEqual(response_data["subject"], data["subject"])
        self.assertEqual(response_data["message"], data["message"])
        self.assertEqual(response_data["guest_name"], existing_guest.name)

        # Assert the entry was created in the database
        entry = Entry.objects.get(id=response_data["id"])
        self.assertIsNotNone(entry)
        self.assertEqual(entry.subject, data["subject"])
        self.assertEqual(entry.message, data["message"])

        # Ensure the existing guest is not duplicated
        guest = Guest.objects.filter(name=existing_guest.name).count()
        self.assertEqual(guest, 1)  # There should be only one guest with this name
