import os
import stripe
from datetime import timedelta
from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from dotenv import load_dotenv


from borrowings.models import Payment, Borrowing
from books.models import Book
from users.models import User
from utilities.stripe_helper import stripe_helper

load_dotenv()


class PaymentViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="testpass"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="testpass"
        )

        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HD",
            inventory=1,
            daily_fee=10.00,
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user,
        )
        self.payment = Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            type=Payment.PaymentType.PAYMENT,
            borrowing=self.borrowing,
            session_url="https://checkout.stripe.com/c/pay"
                        "/cs_test_a1DaagwBTiPBM7ce6T2wQEQLzTqUHH98j3VYvWhIKiO7GNl0D0"
                        "#fidkdWxOD2Hic%2FcXdwYHgl",
            session_id="cs_test_a1DaagwBTiPBM7ce6T2wQEQLzTqUHH98j3VYrl0D0",
            money_to_pay=10.00,
        )

    def test_list_payments(self):
        response = self.client.get(reverse("borrowings:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment(self):
        response = self.client.get(
            reverse("borrowings:payment-detail", kwargs={"pk": self.payment.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

    def test_list_payments_admin(self):
        response = self.client.get(reverse("borrowings:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("borrowings:payment-detail", kwargs={"pk": self.payment.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)


class PaymentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email="testuser@test.com",
            password="12345"
        )

        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.BookCover.HARD,
            inventory=10,
            daily_fee=1.00
        )

        borrow_date = timezone.now().date()
        expected_return_date = borrow_date + timedelta(days=10)
        self.borrowing = Borrowing.objects.create(
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
            book=book,
            user=user
        )

    def test_create_payment_session(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        payment = stripe_helper(self.borrowing)
        self.assertEqual(payment.money_to_pay, 10.00)
        self.assertIsNotNone(payment.session_url)
        self.assertIsNotNone(payment.session_id)
