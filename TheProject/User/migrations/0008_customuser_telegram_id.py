# Generated by Django 4.2.3 on 2023-10-07 05:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0007_homework_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="telegram_id",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="telegram id"
            ),
        ),
    ]