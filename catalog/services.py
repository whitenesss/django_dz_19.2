from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_product_from_cache():
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = "category_list"

    categoryes = cache.get(key)

    if categoryes is not None:
        return categoryes
    categoryes = Category.objects.all()

    cache.set(key, categoryes)

    return categoryes
