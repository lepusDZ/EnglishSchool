# Generated by Django 4.2.3 on 2023-09-12 21:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0005_homework"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homework",
            name="description",
            field=models.TextField(verbose_name="Description"),
        ),
    ]
