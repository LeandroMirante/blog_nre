# Generated by Django 4.1.5 on 2023-01-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="birth_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
