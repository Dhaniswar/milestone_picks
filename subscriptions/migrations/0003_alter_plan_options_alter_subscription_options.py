# Generated by Django 5.1.6 on 2025-03-18 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0002_subscription"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="plan",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterModelOptions(
            name="subscription",
            options={"ordering": ["-id"]},
        ),
    ]
