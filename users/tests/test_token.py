from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


class TokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass"
        )

    def test_obtain_token(self):
        data = {
            "email": "test@test.com",
            "password": "testpass",
        }
        response = self.client.post(reverse("users:token_obtain_pair"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        data = {
            "email": "test@test.com",
            "password": "testpass",
        }
        response = self.client.post(reverse("users:token_obtain_pair"), data)
        refresh_token = response.data["refresh"]
        response = self.client.post(
            reverse("users:token_refresh"), {"refresh": refresh_token}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
