from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="введите описание товара"
    )

    def __str__(self):
        return (
            self.name
        )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="введите описание товара", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="catalog/product",
        verbose_name="Изображение(превью)",
        blank=True,
        null=True,
        help_text="добавить изображение товара",
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория", blank=True, null=True,
                                 help_text="выберите катег")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="введите цену товара",
    )
    data_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания(записи в БД)"
    )
    data_update = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения(записи в БД)"
    )

    def __str__(self):
        return (
            self.name
        )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = [
            "name",
            "price",
            "data_create",
            "data_update",
            "category",
            "description",
        ]
