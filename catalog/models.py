from django.db import models, connection

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="введите наименование категории",
    )
    description = models.TextField(
        help_text="введите описание категории", verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    owner = models.ForeignKey(User, verbose_name="Автор", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')

    def __str__(self):
        return f'{self.name}'


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
                                 help_text="выберите категорию")
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
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    owner = models.ForeignKey(User, verbose_name="Автор", blank=True, null=True, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

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
        permissions = (
            ('can_unpublish_product', 'Can unpublish product'),
            ('change_product_description', 'Can change product description'),
            ('change_product_category', 'Can change product category'),
        )


class Blog(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Наименование",
        help_text="введите наименование блога",
    )
    slug =models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="человекопонятный URL",
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name="Описание", help_text="введите описание блога", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="catalog/blog",
        verbose_name="Изображение(превью)",
        blank=True,
        null=True,
    )
    data_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания(записи в БД)"
    )
    data_update = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения(записи в БД)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.title


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Товар",blank=True, null=True,)
    namber_version = models.IntegerField(verbose_name="Версия", help_text="введите версию товара",unique=True)
    name_version = models.CharField(max_length=150, verbose_name="Имя версии", help_text="введите название версии")
    is_activ_version = models.BooleanField(verbose_name="Актуальная", help_text="укажите актуальность версии")

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

    def __str__(self):
        return self.name_version

