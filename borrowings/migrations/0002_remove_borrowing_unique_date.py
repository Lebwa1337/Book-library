# Generated by Django 4.2 on 2024-04-06 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="borrowing",
            name="unique_date",
        ),
    ]