# Generated by Django 4.2 on 2024-04-18 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("borrowings", "0004_alter_payment_session_url_alter_payment_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="borrowings",
                to="books.book",
            ),
        ),
        migrations.AlterField(
            model_name="borrowing",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="borrowings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="borrowing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="borrowings.borrowing",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="session_id",
            field=models.CharField(max_length=255),
        ),
    ]
