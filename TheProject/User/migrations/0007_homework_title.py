# Generated by Django 4.2.3 on 2023-09-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0006_alter_homework_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="homework",
            name="title",
            field=models.CharField(default=0, max_length=300, verbose_name="Title"),
            preserve_default=False,
        ),
    ]
