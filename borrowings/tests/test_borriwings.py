from datetime import date, timedelta

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase

from books.models import Book
from borrowings.models import Borrowing


class BorrowingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="testpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.BookCover.HARD,
            inventory=1,
            daily_fee=10.00,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
            book=self.book,
            user=self.user,
        )

    def test_retrieve_borrowing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                "borrowings:borrowing-detail",
                kwargs={"pk": self.borrowing.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing.id)

    def test_return_borrowing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(
                "borrowings:return_borrowing",
            ),
            data={"borrowing_id": self.borrowing.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.assertEqual(self.borrowing.actual_return_date, date.today())
