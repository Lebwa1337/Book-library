# Generated by Django 4.2 on 2024-04-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0003_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_url",
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[("PENDING", "Pending"), ("PAID", "Paid")],
                default="PENDING",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="type",
            field=models.CharField(
                choices=[("PAYMENT", "Payment"), ("FINE", "Fine")],
                default="PAYMENT",
                max_length=10,
            ),
        ),
    ]
