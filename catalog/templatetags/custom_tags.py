from django import template

register = template.Library()

@register.filter
def get_products_for_category(category, product_list):
    return [product for product in product_list if product.category == category and product.is_active]
