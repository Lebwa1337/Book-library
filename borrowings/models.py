from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book

    @staticmethod
    def validate_dates(borrow_date, expected_return_date):
        if borrow_date > expected_return_date:
            raise ValidationError("Borrow date should be less than expected or actual return date")

    def clean(self):
        Borrowing.validate_dates(self.borrow_date, self.expected_return_date)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Borrowing, self).save(force_insert, force_update, using, update_fields)
