# Generated by Django 5.0.4 on 2024-05-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_category_is_active_product_is_active_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="введите наименование блога",
                        max_length=50,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="человекопонятный URL",
                        max_length=15,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="введите описание блога",
                        null=True,
                        verbose_name="Описание",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="catalog/blog",
                        verbose_name="Изображение(превью)",
                    ),
                ),
                (
                    "data_create",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания(записи в БД)"
                    ),
                ),
                (
                    "data_update",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Дата последнего изменения(записи в БД)",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активен"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Опубликован"),
                ),
            ],
            options={
                "verbose_name": "Блог",
                "verbose_name_plural": "Блоги",
            },
        ),
    ]