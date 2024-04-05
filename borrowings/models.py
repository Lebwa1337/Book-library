from django.db import models
from django.db.models import UniqueConstraint

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique_date",
                fields=[
                    "borrow_date",
                    "expected_return_date",
                    "actual_return_date"
                ],
            )
        ]

    def __str__(self):
        return self.book
