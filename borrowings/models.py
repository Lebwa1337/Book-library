import stripe
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    def __str__(self):
        return self.book.title

    @staticmethod
    def validate_dates(borrow_date, expected_return_date):
        if borrow_date > expected_return_date:
            raise ValidationError("Borrow date should be less than expected or actual return date")

    @staticmethod
    def validate_book_amount(book):
        if not book.inventory > 0:
            raise ValidationError("This book is out of stock")

    def clean(self):
        Borrowing.validate_dates(self.borrow_date, self.expected_return_date)
        Borrowing.validate_book_amount(self.book)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Borrowing, self).save(force_insert, force_update, using, update_fields)

    @transaction.atomic
    def create_fine_if_overdue(self):
        if self.actual_return_date > self.expected_return_date:
            days_overdue = (
                    self.actual_return_date - self.expected_return_date
            ).days

            fine_amount = (days_overdue * self.book.daily_fee * 2) * 100

            price = stripe.Price.create(
                product='prod_PuIXD7rHUrikDl',
                unit_amount=int(fine_amount),
                currency="usd",
            )

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=("http://localhost:8000/api/"
                             "payments/success/"),
                cancel_url="http://localhost:8000/api/payments/cancel/"
            )
            Payment.objects.create(
                borrowing=self,
                session_url=checkout_session.url,
                session_id=checkout_session.id,
                money_to_pay=fine_amount / 100,
            )


class Payment(models.Model):
    """Payment model."""
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", _("Payment")
        FINE = "FINE", _("Fine")
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    type = models.CharField(
        max_length=10,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT,
    )
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")
    session_url = models.URLField(max_length=1000)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=5, decimal_places=2)
