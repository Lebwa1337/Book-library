from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from users.serializers import UserSerializer


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@test.com",
            "password": "testpass",
        }
        self.superuser_data = {
            "email": "admin@admin.com",
            "password": "adminpass",
        }
        self.updated_user_data = {
            "email": "updated@test.com",
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(**self.superuser_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.superuser_data["email"])
        self.assertTrue(user.check_password(self.superuser_data["password"]))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_serialize_user(self):
        user = User.objects.create_user(**self.user_data)
        serializer = UserSerializer(user)
        expected_data = {
            "id": user.id,
            "email": self.user_data["email"],
            "is_staff": False,
        }
        self.assertEqual(serializer.data, expected_data)
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_deserialize_user(self):
        serializer = UserSerializer(data=self.user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_create_user_view(self):
        response = self.client.post(reverse("users:register"), self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data["email"])

    def test_manage_user_view(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user)
        response = self.client.get(reverse("users:me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"id": user.id,
             "email": self.user_data["email"],
             "is_staff": False},
        )

    def test_register_existing_user(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(reverse("users:register"), self.user_data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_view(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user)
        response = self.client.patch(
            reverse("users:me"),
            self.updated_user_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["email"],
            self.updated_user_data["email"]
        )
