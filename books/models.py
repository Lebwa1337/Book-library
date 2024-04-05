from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    class BookCover(models.TextChoices):
        SOFT = "SF", _("Soft")
        HARD = "HD", _("Hard")
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    cover = models.CharField(
        max_length=2,
        choices=BookCover.choices
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
