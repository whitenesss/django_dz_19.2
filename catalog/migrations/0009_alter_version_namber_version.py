# Generated by Django 5.0.4 on 2024-06-07 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="version",
            name="namber_version",
            field=models.IntegerField(
                help_text="введите версию товара", unique=True, verbose_name="Версия"
            ),
        ),
    ]