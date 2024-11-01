from django.test import TestCase
from django.urls import reverse
from ..models import Guest, Entry

class GetEntriesTestCase(TestCase):
    def setUp(self):
        # Create sample users and entries for testing
        self.user1 = Guest.objects.create(name='User 1')
        self.user2 = Guest.objects.create(name='User 2')

        Entry.objects.create(subject='Subject 1', message='Message 1', guest=self.user1)
        Entry.objects.create(subject='Subject 2', message='Message 2', guest=self.user2)
        Entry.objects.create(subject='Subject 3', message='Message 3', guest=self.user1)
        Entry.objects.create(subject='Subject 4', message='Message 4', guest=self.user2)
        Entry.objects.create(subject='Subject 5', message='Message 5', guest=self.user1)

    def test_get_entries_success(self):
        response = self.client.get(reverse('entry-view') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('entries', response.json())
        self.assertEqual(response.json()['count'], 5)
        self.assertEqual(len(response.json()['entries']), 3)  # Check the number of entries returned

    def test_get_entries_empty(self):
        # Clear the database and test for empty response
        Entry.objects.all().delete()
        response = self.client.get(reverse('entry-view') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        self.assertEqual(len(response.json()['entries']), 0)

    def test_get_entries_invalid_page(self):
        response = self.client.get(reverse('entry-view')+ '?page=100')  # Invalid page number
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())  # Assuming your request_data.is_valid() will fail for invalid page

    def test_get_entries_pagination(self):
        response = self.client.get(reverse('entry-view') + '?page=2')  # Get the second page
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['entries']), 2)  # Second page should have 2 entries
        self.assertEqual(response.json()['current_page_number'], 2)
